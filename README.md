# Legal Summarizer 

![OpenAI](https://img.shields.io/badge/Openai-74aa9c?style=for-the-badge&logo=openai&logoColor=white) ![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-1.27.2-FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white)


Leveraging LLM to summarize clauses from legal documents.

![overview](https://github.com/d1pankarmedhi/legal_summarizer/assets/136924835/c37e6dcd-f560-446c-a50b-dd166bce46a6)
---


- [Legal Summarizer](#legal-summarizer)
  - [:yawning\_face: Hard to understand contract agreements](#yawning_face-hard-to-understand-contract-agreements)
  - [:mechanical\_arm: Tackling this challenge with LLMs](#mechanical_arm-tackling-this-challenge-with-llms)
  - [:postal\_horn: RAG makes it easy](#postal_horn-rag-makes-it-easy)
  - [:toolbox: Getting started](#toolbox-getting-started)

## :yawning_face: Hard to understand contract agreements

Legal documents often contains complex terminologies that are not used in everyday language. These terms can be confusing and may require domain knowledge to understand the meanings. 

These documents use highly technical and precise language, which can be challenging for non-legal professionals to grasp. They tend to have long sentences or paragraph, making it challenging for the public to content and extract key points. 

Legal documents incorporate references to statutes, regulations, clauses, and other legal citations, assuming a deep understanding of the legal system. The absence of straightforward language in these documents can make the content feel distant and unrelatable.

These documents are typically written to avoid any risks so their cautious and conservative wording results in complex sentences, amiming to counter every conceivable scenario and misinterpreting these documents can have serious consequences. This is the reason, why most of the time general public/readers avoid engaging into any scene that involves handling legal contacts/agreements by themselves. 

## :mechanical_arm: Tackling this challenge with LLMs



## :postal_horn: RAG makes it easy






## :toolbox: Getting started

Create a virtual-env and install the necessary requirements
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

