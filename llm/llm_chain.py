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
    


        

        
