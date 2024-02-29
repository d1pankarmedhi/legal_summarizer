# Legal Summarizer

![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) 
![Python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-1.27.2-FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white)

Summarize contracts and legal documents leveraging Information Retrieval and context Augmentation using Large Language Models.

<div align="center">
  <img src="https://github.com/d1pankarmedhi/legal_summarizer/assets/136924835/4968735b-b3a8-4633-8edd-6b8bed7ba558"/>
  <p>Fig: Highlevel design/architecture diagram</p>
</div>

---


- [Legal Summarizer](#legal-summarizer)
  - [:yawning\_face: Hard to understand contract agreements](#yawning_face-hard-to-understand-contract-agreements)
  - [:mechanical\_arm: Tackling this challenge with LLMs](#mechanical_arm-tackling-this-challenge-with-llms)
  - [:postal\_horn: RAG makes it easy](#postal_horn-rag-makes-it-easy)
  - [:toolbox: Getting started](#toolbox-getting-started)

## :yawning_face: Hard to understand contract agreements

Legal documents often contain complex terminologies that are not used in everyday language. These terms can be confusing and may require domain knowledge to understand their meanings. 

These documents use highly technical and precise language, which can be challenging for non-legal professionals to grasp. They tend to have long sentences or paragraphs, making it challenging for the public to content and extract key points. 

Legal documents incorporate references to statutes, regulations, clauses, and other legal citations, assuming a deep understanding of the legal system. The absence of straightforward language in these documents can make the content feel distant and unrelatable.

These documents are typically written to avoid any risks so their cautious and conservative wording results in complex sentences, aiming to counter every conceivable scenario and misinterpreting these documents can have serious consequences. This is the reason, why most of the time general public/readers avoid engaging in any scene that involves handling legal contacts/agreements by themselves. 

## :mechanical_arm: Tackling this challenge with LLMs

With the rise of large language models and organizations like Openai, LLMs have become more accessible than they ever were. These language models laid the foundation of what we call "Augmentation" or reconstructing a piece of context based on its usage and applicability. 

These huge models are so smart that they can produce human-like, sometimes better, results when asked to reconstruct a piece of text as per the instruction. The limitations occur on how well the model handles the input data. This depends on the type of data the model is trained on, or how big the model is. We are in an era where there are models with billions of parameters (both open-source and closed-source). This depends on the user and the problem it wants to solve. 


## :postal_horn: RAG makes it easy

RAG or Retrieval Augmented Generation is used in this project. The idea is to do a search on the documents and produce relevant answers for the search query. 

One can use the BM25 search ranking algorithm which is a keyword-based search algorithm or something called semantic search, that doesn't just rely on keyword search but takes the nearby context into account while producing embeddings for similarity search. 

After the relevant documents are retrieved, the context is then passed through an LLM that is responsible for the reconstruction of the piece of context into a more refined and usable answer.

Read more about RAG and how to use Langchain to build a Q&A system on this blog [Exploring power of RAG and OpenAI's function calling for question answering](https://dipankarmedh1.medium.com/exploring-the-power-of-rag-and-openais-function-calling-for-question-answering-d512c45c56b5)


## :toolbox: Getting started

Create a virtual-env and install the requirements
```bash
$ python -m venn venv
$ venv\Scripts\activate # windows
$ source venv/bin/activate # linux
```

```bash
$ pip install -r requirements.txt 
```

Start the application

```bash 
$ streamlit run summarize.py
```

