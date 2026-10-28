
import os
import re
import time
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY is missing. Check your .env file.")


def build_vector_store(pdf_paths):
    documents = []

    # Load each uploaded PDF.
    for pdf_path in pdf_paths:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()

        for page in pages:
            page.metadata["source"] = os.path.basename(pdf_path)

        documents.extend(pages)

    if not documents:
        raise ValueError("No readable PDF content was found.")

    # Split document pages into smaller chunks.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
    )

    chunks = text_splitter.split_documents(documents)

    print(f"DEBUG: Loaded {len(documents)} pages.", flush=True)
    print(f"DEBUG: Created {len(chunks)} chunks.", flush=True)

    # Load the local embedding model.
    print("DEBUG: Loading local embedding model...", flush=True)
    start = time.perf_counter()

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print(
        f"DEBUG: Embedding model ready in "
        f"{time.perf_counter() - start:.2f} seconds.",
        flush=True,
    )

    # Store chunks and their embeddings in Chroma.
    print("DEBUG: Creating Chroma vector store...", flush=True)
    start = time.perf_counter()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    print(
        f"DEBUG: Vector store created in "
        f"{time.perf_counter() - start:.2f} seconds.",
        flush=True,
    )

    return vector_store


def answer_question(question, vector_store):
    if not question or not question.strip():
        return "Please enter a question.", []

    print("DEBUG: Starting document retrieval...", flush=True)
    start = time.perf_counter()

    # Detect an explicitly requested physical PDF page.
    page_match = re.search(
        r"\b(?:pdf\s+)?page\s+(\d+)\b",
        question,
        re.IGNORECASE,
    )

    try:
        if page_match:
            requested_page = int(page_match.group(1))

            if requested_page < 1:
                return "PDF page numbers start at 1.", []

            # PyPDFLoader stores page indexes starting at zero.
            page_index = requested_page - 1

            print(
                f"DEBUG: Restricting retrieval to PDF page "
                f"{requested_page}.",
                flush=True,
            )

            retrieved_docs = vector_store.similarity_search(
                question,
                k=10,
                filter={
    "$or": [
        {"page": {"$eq": page_index}},
        {"page": {"$eq": page_index + 1}}
    ]
} ,
)

        else:
            # No page specified: search across all uploaded PDFs.
            retrieved_docs = vector_store.similarity_search(
                question,
                k=4,
            )

    except Exception as error:
        print(f"DEBUG: Retrieval failed: {error}", flush=True)
        return f"Error retrieving document content: {error}", []

    print(
        f"DEBUG: Retrieval completed in "
        f"{time.perf_counter() - start:.2f} seconds.",
        flush=True,
    )

    if not retrieved_docs:
        if page_match:
            return (
                f"I couldn't find relevant content on PDF page "
                f"{int(page_match.group(1))}.",
                [],
            )

        return "I couldn't find relevant information in the PDFs.", []

    # Build context with human-readable physical PDF page numbers.
    context = "\n\n".join(
        f"Source: {doc.metadata.get('source', 'Unknown')}, "
        f"PDF Page: {doc.metadata.get('page', 0) + 1}\n"
        f"{doc.page_content}"
        for doc in retrieved_docs
    )

    prompt = f"""
You are a document question-answering assistant.

Answer using only the context provided below.
If the context does not contain the answer, say you could not find it
in the uploaded documents. Do not invent facts.

When the question requests a specific PDF page, answer using only
the retrieved content from that page.

Context:
{context}

Question:
{question}
"""

    # Generate an answer using Gemini.
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0.2,
        timeout=120,
        max_retries=2,
    )

    print("DEBUG: Sending question to Gemini...", flush=True)
    start = time.perf_counter()

    try:
        response = llm.invoke(prompt)
    except Exception as error:
        print(f"DEBUG: Gemini request failed: {error}", flush=True)
        return f"Error contacting Gemini: {error}", []

    print(
        f"DEBUG: Gemini responded in "
        f"{time.perf_counter() - start:.2f} seconds.",
        flush=True,
    )

    # Normalize the response into a string.
    answer = response.content

    if isinstance(answer, list):
        answer = "\n".join(
            item.get("text", str(item))
            if isinstance(item, dict)
            else str(item)
            for item in answer
        )
    elif not isinstance(answer, str):
        answer = str(answer)

    # Return source information for the UI.
    sources = [
        {
            "source": doc.metadata.get("source", "Unknown"),
            "page": doc.metadata.get("page", 0) + 1,
            "content": doc.page_content,
        }
        for doc in retrieved_docs
    ]

    return answer, sources
