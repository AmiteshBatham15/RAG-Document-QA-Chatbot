
# RAG Document Q&A Chatbot

A Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions about their contents.

## Features

- Upload PDF documents through a Gradio interface
- Extract and split PDF text into chunks
- Generate embeddings using Hugging Face Sentence Transformers
- Store document embeddings in ChromaDB
- Retrieve relevant document chunks for user questions
- Generate answers using Google Gemini
- Display document source references

## Tech Stack

- Python
- Gradio
- LangChain
- ChromaDB
- Hugging Face Sentence Transformers
- Google Gemini API

## Setup Instructions

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd RAG-Document-QA-Chatbot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project root and add:

```env
GOOGLE_API_KEY=your_api_key_here
```

Replace the placeholder with your own Google Gemini API key. Never commit the real key.

### 5. Run the application

```bash
python app.py
```

Open the local URL displayed in the terminal.

## Security

- Keep `.env` out of version control.
- Do not upload private documents or copyrighted PDFs without permission.
- Keep generated databases and virtual environments out of the repository.
