# 📄 RAG-Based PDF Assistant

<p align="center">
  <b>Upload a PDF → Ask Questions → Get AI-Powered Answers</b>
</p>

<p align="center">
  <a href="https://rag-based-project.streamlit.app/">
    <img src="https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit-red?style=for-the-badge" />
  </a>
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/Groq-LLM-orange?style=for-the-badge" />
</p>

---

## 🚀 Live Demo

### 👉 [Open the RAG-Based PDF Assistant](https://rag-based-project.streamlit.app/)

Upload a PDF, ask questions about its content, and get answers generated using retrieved information from the document.

---

## 🧠 What is this?

This project is a simple **Retrieval-Augmented Generation (RAG)** application.

Instead of sending the complete PDF directly to the language model, the application:

> **Extracts → Chunks → Embeds → Retrieves → Generates**

The system finds the most relevant parts of the uploaded PDF and provides them as context to the LLM before generating the final answer.

---

## 🔥 How It Works

```text
                 📄 Upload PDF
                       │
                       ▼
              ┌─────────────────┐
              │  Extract Text   │
              └─────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    Chunking     │
              │ Split document  │
              │ into small parts│
              └─────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   Embeddings    │
              │ Text → Vectors  │
              └─────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Similarity Search│
              │ Find relevant   │
              │ PDF chunks      │
              └─────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    Groq LLM     │
              │ Generate Answer  │
              └─────────────────┘
                       │
                       ▼
                    ✅ Answer
✨ Features
📄 Upload a PDF directly from the browser
🔍 Search the PDF using semantic similarity
🧠 Generate embeddings from document chunks
🤖 Generate answers using a Groq-hosted LLM
📚 Retrieve the most relevant document sections
🔎 View the retrieved context used to generate the answer
⚡ Simple and lightweight Streamlit interface
🛠️ Tech Stack
Technology	Purpose
🐍 Python	Core application logic
🎈 Streamlit	Web application interface
📄 PyPDF	Extract text from PDF files
🧠 Sentence Transformers	Generate text embeddings
🔢 NumPy	Vector similarity calculations
⚡ Groq API	LLM inference
🔍 Understanding "Retrieved Context"

After asking a question, the application shows a section called:

Retrieved context

This contains the actual pieces of text retrieved from the uploaded PDF that are considered relevant to your question.

For example:

Question
   ↓
Convert question to embedding
   ↓
Compare with PDF embeddings
   ↓
Find most relevant chunks
   ↓
Send those chunks to the LLM
   ↓
Generate final answer

You may see:

Chunk 1 — similarity: 0.204
Chunk 2 — similarity: 0.203

The similarity score represents how closely the chunk matches the question according to the vector similarity calculation.

📚 RAG Pipeline Concepts
1️⃣ Chunking

A large document is divided into smaller sections called chunks.

Large PDF
   ↓
Chunk 1
Chunk 2
Chunk 3
...
2️⃣ Tokenization

Text is broken into smaller units called tokens.

Tokens may be words, parts of words, or symbols.

The embedding model handles tokenization internally.

3️⃣ Embeddings

Text is converted into numerical vectors that represent semantic information.

Text → Numerical Vector
4️⃣ Retrieval

The application compares the user's question with document embeddings and retrieves the most relevant chunks.

5️⃣ Generation

The retrieved context is sent to the Groq language model, which generates the final answer.

🧩 Project Structure
rag-based-project/
│
├── app.py
├── requirements.txt
└── README.md
💻 Run Locally
1. Clone the repository
git clone https://github.com/YOUR_USERNAME/rag-based-project.git
cd rag-based-project
2. Install dependencies
pip install -r requirements.txt
3. Configure your Groq API key

Create:

.streamlit/
└── secrets.toml

Add:

GROQ_API_KEY = "your_groq_api_key"
4. Run the application
streamlit run app.py
☁️ Deploy on Streamlit Cloud
Push app.py, requirements.txt, and README.md to GitHub.
Open Streamlit Community Cloud.
Select your GitHub repository.
Set app.py as the main application file.
Deploy the application.
Go to Settings → Secrets.
Add:
GROQ_API_KEY = "your_groq_api_key"
🔐 Security
Never expose your API key

❌ Do not put your real API key inside:

api_key = "gsk_..."

❌ Do not upload API keys to GitHub.

✅ Use Streamlit Secrets:

GROQ_API_KEY = "your_groq_api_key"
⚠️ Current Limitations
Works best with text-based PDFs
Scanned/image-only PDFs are not OCR processed
Current chunking uses a simple character-based approach
Retrieval quality depends on extracted text and embeddings
PDF/vector processing is performed during the current app session
🔮 Future Improvements

Possible improvements include:

🧩 Semantic chunking
🔎 Better retrieval and reranking
💾 Persistent vector databases
📚 Multiple PDF support
💬 Chat history
📌 Page-level source citations
🖼️ OCR for scanned PDFs
⚡ Streaming responses
🗂️ Better document metadata handling
🎯 Project Goal

The goal of this project is to demonstrate the fundamentals of a Retrieval-Augmented Generation system in a simple and understandable way.

Core idea:
Document
   ↓
Retrieval
   ↓
Relevant Context
   ↓
LLM
   ↓
Answer
📸 Try It Yourself
Example workflow

1. Upload a PDF

⬇️

2. Ask a question

"What is the main topic discussed in this document?"

⬇️

3. Retrieve relevant information

⬇️

4. Generate an answer

⬇️

5. Inspect the retrieved context

👨‍💻 Author
Meesum Mukhtar

🚀 Live Project:
https://rag-based-project.streamlit.app/

⭐ Support

If you found this project useful, consider giving the repository a ⭐ Star.

<p align="center"> Built with 🧠 RAG + ⚡ Groq + 🎈 Streamlit </p> ```
