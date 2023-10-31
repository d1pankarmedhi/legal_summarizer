import re
import weaviate
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
import uuid
import pandas as pd
import streamlit as st
from typing import List
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.llms import AzureOpenAI, OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS, Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
import pytesseract
import pypdfium2 as pdfium

load_dotenv()

WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")


##### Text Extraction ######
def extract_from_pdf(file: bytes) -> str:
    data = ""
    pdf_reader = PdfReader(file)
    for page in pdf_reader.pages:
        data += page.extract_text()
    return data

# def extract_from_pdf(file: str) -> str:
#     data = ""
#     pdf_reader = PdfReader(file)
#     for page in pdf_reader.pages:
#         data += page.extract_text()
#     return data

def extract_from_scanned_pdf(file):
    text = ""
    pdf = pdfium.PdfDocument(file)
    n_pages = len(pdf)
    for page_number in range(n_pages):
        page = pdf.get_page(page_number)
        bitmap = page.render(
            scale=1,
            rotation=0,
        )
        img = bitmap.to_pil()
        text += pytesseract.image_to_string(img, config=r"--oem 3 --psm 6")
    return text


### Text Processing ###
def classify_text(text: str):
    if text.isupper():
        return "heading"
    else:
        return "body"


def tag_documents(data: str) -> list:
    tagged_documents = []
    current_heading = None
    current_paragraph = ""

    for line in data.split("\n"):
        line = line.strip()

        if not line:
            continue
        text_class = classify_text(line)

        if text_class == "heading":
            if current_heading is not None:
                tagged_documents.append(
                    {"heading": current_heading, "body": current_paragraph.strip()}
                )

            current_heading = line
            current_paragraph = ""
        else:
            current_paragraph += " " + line

    if current_heading is not None:
        tagged_documents.append(
            {"heading": current_heading, "body": current_paragraph.strip()}
        )

    # split body into documents
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n\n", "\n\n", "\n", " "],
        chunk_size=1000,
        chunk_overlap=30,
    )
    for data in tagged_documents:
        documents = text_splitter.create_documents([data["body"]])
        data["documents"] = documents

    return tagged_documents


### Connect to Weaviate ###
def generate_class_name(class_name: str = None):
    id = uuid.uuid4()
    name = "Class_"
    if class_name is None:
        name = "Class_" + str(id.int)
    else:
        name += class_name

    return name


def connect_to_weaviate(api_key: str, url: str):
    client = weaviate.Client(
        auth_client_secret=weaviate.AuthApiKey(api_key),
        url=url,
    )
    return client

### Create weaviate schema ###
def create_class_obj(client, class_name: str):
    try:
        properties = [
            {
                "name": "content",
                "dataType": ["text"],
            },
            {
                "name": "tag",
                "dataType": ["text"],
            },
        ]
        class_obj = {
            "class": class_name,
            "properties": properties,
        }

        client.schema.create_class(class_obj)

    except Exception as e:
        print(e)

### Add documents to weavaite ###
def add_documents(client, class_name: str, tagged_documents: list):
    try:
        data_objs = []
        for i, d in enumerate(tagged_documents):
            for doc in d["documents"]:
                data_objs.append(
                    {
                        "content": doc.page_content,
                        "tag": d["heading"],
                    },
                )

        client.batch.configure(batch_size=100)
        with client.batch as batch:
            for data_obj in data_objs:
                batch.add_data_object(data_obj, class_name)

    except Exception as e:
        print(e)


def delete_class(client, class_name: str):
    try:
        client.schema.delete_class(class_name)
    except Exception as e:
        print(e)


### Initialize LLM ###
def load_model():
    llm = ChatOpenAI()
    return llm





# find the number of tokens
def token_nums(llm, data: str):
    return llm.get_num_tokens(data)


### Create LLM chain ###
def get_chain(llm):
    CUSTOM_PROMPT_TEMPLATE = """
    You are a lease clause summarization expert. Your job is to Summarize the lease clauses from the below mentioned Context in a single and short paragraph. The final answer should fullfill the definition and the given guidelines for each clause. 

    If the context has relevant information regarding the clause section, page number, clause number, etc. Please add them at the end of the summary inside '()'.

    If the summarized answer is not relevant to the `{clause}`, just output 'Clause Not Found' as the summary. Don't make your answer on your own. 

    The given Context:{context}

    The Clause is {clause}.

    Answer:"""
    prompt = PromptTemplate(
        template=CUSTOM_PROMPT_TEMPLATE, input_variables=["context", "clause"]
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain

### Weaviate search ###
def bm25_search_weaviate(client, query: str, class_name: str) -> list:
    result = []
    response = (
        client.query.get(class_name, ["content", "tag"])
        .with_bm25(
            query=query,
        )
        .with_limit(4)
        .do()
    )
    for content in response["data"]["Get"][class_name]:
        result.append(content["content"])

    return result


### Summarize ###
def summary(query: str, chain, vectorstore):
    output = ""
    context = []
    for document in vectorstore.similarity_search(query):
        context.append(document.page_content)
    s = chain.run({"context": context, "query": query})
    res = re.sub(r"<.*?>", "", s)
    res = res.replace("\n", " ")

    not_found = re.findall(r"Clause Not Found", res)
    if not_found:
        output = not_found[0]
    else:
        output = res

    code_pattern_match = re.search(r"^(.*?)```", res)
    if code_pattern_match:
        output = code_pattern_match.group(1)

    quote_pattern_match = re.search(r'^(.*?)"""', output)
    if quote_pattern_match:
        output = quote_pattern_match.group(1)

    single_quote_pattern_match = re.search(r"^(.*?)'''", output)
    if single_quote_pattern_match:
        output = single_quote_pattern_match.group(1)

    return output


# def create_vectorstore(_documents: List[str], _embeddings):
#     vectorstore = None
#     if len(_documents) > 16:
#         vectorstore = FAISS.from_documents(_documents[0:16], _embeddings)
#         i = 16
#         while i < len(_documents):
#             if len(_documents) - i <= 16:
#                 vectorstore.add_documents(_documents[i : len(_documents)])
#                 break
#             vectorstore.add_documents(_documents[i : i + 16])
#             i += 16
#     else:
#         vectorstore = FAISS.from_documents(_documents[0 : len(_documents)], _embeddings)
#     return vectorstore


def summarize(relevant_documents: list, query: str, chain, class_name):
    output = ""

    s = chain.run({"context": relevant_documents, "clause": query})
    res = re.sub(r"<.*?>", "", s)
    res = res.replace("\n", " ")

    not_found = re.findall(r"Clause Not Found", res)
    if not_found:
        output = not_found[0]
    else:
        output = res

    code_pattern_match = re.search(r"^(.*?)```", res)
    if code_pattern_match:
        output = code_pattern_match.group(1)

    quote_pattern_match = re.search(r'^(.*?)"""', output)
    if quote_pattern_match:
        output = quote_pattern_match.group(1)

    single_quote_pattern_match = re.search(r"^(.*?)'''", output)
    if single_quote_pattern_match:
        output = single_quote_pattern_match.group(1)

    return output


def main():
    st.set_page_config(page_title="ClauseSense", layout="wide", page_icon="♦")

    st.markdown(
        "<h1 style='text-align: center; font-weight:bold; font-family:comic sans ms; padding-top: 0rem;'> \
            Legal Document Summarization</h1>",
        unsafe_allow_html=True,
    )

    
    clauses = {}
    clause_count = st.sidebar.slider(label="Number of clause", min_value=1, max_value=5)

    
    # st.write(clauses)

    # output_dict = {
    #     "Term": [],
    #     "Services": [],
    #     "General Provision": [],
    #     "Notices": [],
    #     "Signage": [],
    # }

    ## upload document
    file = st.file_uploader(label="Upload your document (pdf)", type="pdf")
    print()
    if file:
        button = st.button("Submit")
        llm = load_model()
        llm_chain = get_chain(llm=llm)

        st.subheader("Enter clauses that you want to summarize 👇")
        cols = st.columns(clause_count)
        for i, x in enumerate(cols):
            clauses[x.text_input(label=f"clause {i+1}", value="", key=i)] = []
        
            
        # st.write(clauses)

    if file and button:
        st.divider()
        with st.spinner("Generating summaries..."):
            # extract text from document
            data = extract_from_scanned_pdf(file)
            tagged_documents = tag_documents(data)

            # generate a class name
            class_name = generate_class_name()

            # connect to weaviate
            client = connect_to_weaviate(
                api_key=WEAVIATE_API_KEY,
                url=WEAVIATE_URL,
            )

            # create class obj
            create_class_obj(client=client, class_name=class_name)
            print(f"{class_name} successfulle created!")

            # add documents
            add_documents(
                client=client, class_name=class_name, tagged_documents=tagged_documents
            )

            for k, v in clauses.items():
                relevant_documents = bm25_search_weaviate(
                    client=client, query=k, class_name=class_name
                )
                print(relevant_documents)
                v.append(
                    summarize(
                        relevant_documents=relevant_documents,
                        query=k,
                        chain=llm_chain,
                        class_name=class_name,
                    )
                )

            # delete the create class
            delete_class(client=client, class_name=class_name)
            print(f"{class_name} successfully deleted!")

        # expander view
        items = list(clauses.items())

        for i, x in enumerate(cols):
            x.subheader(items[i][0])
            text = "".join(items[i][1][0])
            x.text_area("Summary", text, key=i+10, height=400)

if __name__ == "__main__":
    main()
