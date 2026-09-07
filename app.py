import os
import streamlit as st
import numpy as np
import faiss
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from groq import Groq

st.set_page_config(page_title="PDF RAG Assistant", page_icon="📄")

st.title("📄 PDF RAG Assistant")
st.write("Upload a PDF and ask questions about its content.")

# Streamlit Cloud: add GROQ_API_KEY in Settings > Secrets
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is not set. Add it in Streamlit Cloud → Settings → Secrets.")
    st.stop()

client = Groq(api_key=api_key)

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

embedding_model = load_embedding_model()


def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def create_chunks(text, chunk_size=800, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

    return chunks


def create_vector_database(chunks):
    embeddings = embedding_model.encode(
        chunks,
        convert_to_numpy=True
    ).astype("float32")

    faiss.normalize_L2(embeddings)

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    return index


def search_chunks(question, chunks, index, top_k=4):
    question_embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True
    ).astype("float32")

    faiss.normalize_L2(question_embedding)

    scores, positions = index.search(question_embedding, top_k)

    results = []

    for position, score in zip(positions[0], scores[0]):
        if position != -1:
            results.append((chunks[position], float(score)))

    return results


def generate_answer(question, retrieved_chunks):
    context = "\n\n---\n\n".join(
        chunk for chunk, _ in retrieved_chunks
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a PDF question-answering assistant. "
                    "Answer using only the provided context. "
                    "If the answer is not in the context, say: "
                    "\"I couldn't find that information in the uploaded PDF.\""
                )
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}"
            }
        ],
        temperature=0.2,
        max_completion_tokens=700
    )

    return response.choices[0].message.content


pdf_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if pdf_file:
    with st.spinner("Reading PDF..."):
        text = extract_text_from_pdf(pdf_file)

    if not text.strip():
        st.error("No readable text was found in this PDF.")
        st.stop()

    with st.spinner("Creating chunks and embeddings..."):
        chunks = create_chunks(text)
        index = create_vector_database(chunks)

    st.success(f"PDF processed successfully: {len(chunks)} chunks created.")

    question = st.text_input("Ask a question about the PDF")

    if question:
        with st.spinner("Searching the PDF..."):
            retrieved_chunks = search_chunks(
                question,
                chunks,
                index,
                top_k=4
            )

        with st.spinner("Generating answer..."):
            answer = generate_answer(
                question,
                retrieved_chunks
            )

        st.subheader("Answer")
        st.write(answer)

        with st.expander("Retrieved context"):
            for i, (chunk, score) in enumerate(retrieved_chunks, start=1):
                st.write(f"**Chunk {i} — similarity: {score:.3f}**")
                st.write(chunk)
                st.write("---")
