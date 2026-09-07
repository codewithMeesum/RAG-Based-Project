import os

import numpy as np
import streamlit as st
from groq import Groq
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


st.set_page_config(
    page_title="PDF RAG Assistant",
    page_icon="📄"
)

st.title("📄 PDF RAG Assistant")
st.write("Upload a PDF and ask questions about its content.")


# -----------------------------
# Get Groq API key
# -----------------------------
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error(
        "GROQ_API_KEY is missing. Add it in "
        "Streamlit Cloud → Settings → Secrets."
    )
    st.stop()

client = Groq(api_key=api_key)


# -----------------------------
# Load embedding model
# -----------------------------
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


embedding_model = load_embedding_model()


# -----------------------------
# Extract text from PDF
# -----------------------------
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# -----------------------------
# Create chunks
# -----------------------------
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


# -----------------------------
# Create embeddings
# -----------------------------
def create_embeddings(chunks):
    embeddings = embedding_model.encode(
        chunks,
        convert_to_numpy=True
    ).astype("float32")

    # Normalize embeddings for cosine similarity
    norms = np.linalg.norm(
        embeddings,
        axis=1,
        keepdims=True
    )

    embeddings = embeddings / np.maximum(norms, 1e-12)

    return embeddings


# -----------------------------
# Search relevant chunks
# -----------------------------
def search_chunks(question, chunks, embeddings, top_k=4):
    question_embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True
    ).astype("float32")

    question_norm = np.linalg.norm(
        question_embedding,
        axis=1,
        keepdims=True
    )

    question_embedding = (
        question_embedding
        / np.maximum(question_norm, 1e-12)
    )

    # Calculate cosine similarity
    scores = np.dot(
        embeddings,
        question_embedding[0]
    )

    top_k = min(top_k, len(chunks))

    best_positions = np.argsort(scores)[-top_k:][::-1]

    results = []

    for position in best_positions:
        results.append(
            (
                chunks[position],
                float(scores[position])
            )
        )

    return results


# -----------------------------
# Generate answer with Groq
# -----------------------------
def generate_answer(question, retrieved_chunks):
    context = "\n\n---\n\n".join(
        chunk for chunk, _ in retrieved_chunks
    )

    prompt = f"""
Use only the context below to answer the question.

If the answer is not in the context, say:
"I couldn't find that information in the uploaded PDF."

Context:
{context}

Question:
{question}

Give a clear and concise answer.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a PDF question-answering assistant. "
                    "Answer using only the supplied PDF context."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_completion_tokens=700
    )

    return response.choices[0].message.content


# -----------------------------
# Upload PDF
# -----------------------------
pdf_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)


if pdf_file:

    # Extract text
    with st.spinner("Reading PDF..."):
        text = extract_text_from_pdf(pdf_file)

    if not text.strip():
        st.error(
            "No readable text was found in this PDF. "
            "Scanned/image-only PDFs need OCR."
        )
        st.stop()

    # Chunk + embeddings
    with st.spinner("Creating chunks and embeddings..."):
        chunks = create_chunks(text)
        embeddings = create_embeddings(chunks)

    st.success(
        f"PDF processed successfully: {len(chunks)} chunks created."
    )

    # Ask question
    question = st.text_input(
        "Ask a question about the PDF"
    )

    if question:

        # Retrieve relevant chunks
        with st.spinner("Searching the PDF..."):
            retrieved_chunks = search_chunks(
                question,
                chunks,
                embeddings,
                top_k=4
            )

        # Generate answer
        with st.spinner("Generating answer..."):
            answer = generate_answer(
                question,
                retrieved_chunks
            )

        st.subheader("Answer")

        st.write(answer)

        # Show retrieved context
        with st.expander("Retrieved context"):

            for i, (chunk, score) in enumerate(
                retrieved_chunks,
                start=1
            ):

                st.write(
                    f"**Chunk {i} — similarity: {score:.3f}**"
                )

                st.write(chunk)

                st.write("---")
