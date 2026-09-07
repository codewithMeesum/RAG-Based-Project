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
