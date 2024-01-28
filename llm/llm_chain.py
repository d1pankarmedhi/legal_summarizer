import re 

from langchain.llms import AzureOpenAI, OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS, Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from utils.env_util import EnvironmentVariables

class LLM:
    def __init__(self) -> None:
        EnvironmentVariables()
        self.llm = ChatOpenAI()


    @staticmethod
    def token_nums(llm, data: str):
        return llm.get_num_tokens(data)

    def get_chain(self) -> LLMChain:
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
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain
    


    def summarize(self, relevant_documents: list, query: str, chain, class_name):
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
    


        

        
