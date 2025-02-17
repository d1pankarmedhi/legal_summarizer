<div align="center">

# **Legal Summarizer**  

![Pandas](https://img.shields.io/badge/Pandas-1.3.3-150458.svg?style=flat&logo=pandas&logoColor=white)  ![Python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-1.27.2-FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white)

 **Summarizing legal documents made easy using Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs).**  

</div>

---

## **📌 Overview**  
Legal documents are often dense, complex, and difficult for non-lawyers to understand. This project leverages **Information Retrieval** and **Context Augmentation** using **Large Language Models (LLMs)** to simplify and summarize contracts, agreements, and other legal texts.

<div align="center">
  <img src="https://github.com/d1pankarmedhi/legal_summarizer/assets/136924835/4968735b-b3a8-4633-8edd-6b8bed7ba558"/>
  <p><i>Fig: High-level system architecture</i></p>
</div>

---

## **🚨 The Problem: Understanding Legal Documents is Hard**  
- Legal documents use **complex terminologies** that require domain expertise.  
- They contain **long, dense sentences** that make key information difficult to extract.  
- They rely on **statutes, legal citations, and references**, assuming prior knowledge.  
- The **conservative and risk-averse language** results in intricate phrasing.  
- Misinterpretation can lead to **serious consequences**, discouraging individuals from handling contracts themselves.  

---

## **🤖 The Solution: AI-Powered Legal Summarization**  
With the advancements in **Large Language Models (LLMs)**, we can now:  
✅ **Extract key insights** from legal documents  
✅ **Summarize complex clauses** into easy-to-read formats  
✅ **Retrieve relevant information** using **RAG (Retrieval-Augmented Generation)**  
✅ **Improve accessibility** of legal content for non-lawyers  

---

## **📌 How Does It Work?**  
### **🔍 Retrieval-Augmented Generation (RAG)**  
**RAG** enhances the summarization process by first searching for relevant content and then reconstructing it using an LLM.

🔹 **Step 1: Document Retrieval**  
- Uses **BM25 ranking** (keyword-based) or **Semantic Search** (context-based) to fetch relevant parts of legal documents.  

🔹 **Step 2: Context Augmentation**  
- The retrieved text is then passed to an **LLM** to generate a structured and readable summary.  

### **📚 Learn More About RAG**  
🔗 [Exploring the Power of RAG & OpenAI’s Function Calling for Q&A](https://dipankarmedh1.medium.com/exploring-the-power-of-rag-and-openais-function-calling-for-question-answering-d512c45c56b5)  

---

## **🛠 Installation & Setup**  
### **1️⃣ Create a Virtual Environment**
```bash
$ python -m venv venv
$ venv\Scripts\activate  # Windows
$ source venv/bin/activate  # macOS/Linux
```

### **2️⃣ Install Dependencies**
```bash
$ pip install -r requirements.txt
```

### **3️⃣ Run the Application**
```bash
$ streamlit run summarize.py
```

---

## **📜 License**  
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## **💡 Contributing** 
Contributions are welcome! Feel free to submit an issue or a pull request.

---

### **💡 Need Help?**
If you have any questions, feel free to reach out! 🚀



