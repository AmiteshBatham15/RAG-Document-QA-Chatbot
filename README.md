# RAG Document Q&A Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that allows users to upload documents and ask questions about their content using semantic search and a large language model.

## Features

- 📄 Supports PDF (`.pdf`), Word (`.docx`), and text (`.txt`) documents.
- 🔍 Retrieves relevant document chunks using semantic similarity search.
- 🤖 Generates contextual answers using Google Gemini.
- 🧠 Creates embeddings using Sentence Transformers.
- 🗄️ Stores document embeddings in ChromaDB.
- 💬 Provides an interactive chat interface using Gradio.
- 📚 Displays source references to help users trace answers to uploaded documents.

## Tech Stack

- **Python**: Core application logic
- **Gradio**: User interface
- **LangChain**: Document loading, text splitting, and RAG workflow
- **ChromaDB**: Vector storage and similarity search
- **Hugging Face Sentence Transformers**: Text embeddings
- **Google Gemini API**: Answer generation

## Supported File Formats

| Format         | Extension | Loader         |
| -------------- | --------- | -------------- |
| PDF            | `.pdf`  | PyPDFLoader    |
| Microsoft Word | `.docx` | Docx2txtLoader |
| Plain text     | `.txt`  | TextLoader     |

## Project Workflow

1. Upload one or more supported documents.
2. Extract the document text.
3. Split the text into smaller chunks.
4. Generate embeddings for the chunks.
5. Store embeddings in ChromaDB.
6. Retrieve relevant chunks when a question is submitted.
7. Generate an answer using Google Gemini.
8. Display the answer and available source references.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/AmiteshBatham15/RAG-Document-QA-Chatbot.git
cd RAG-Document-QA-Chatbot
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual repository URL.

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key
```

Replace the placeholder with your own API key. Never commit `.env` or expose your API key publicly.

### 5. Run the application

```bash
python app.py
```

Open the local Gradio URL displayed in the terminal.

## Future Improvements

- Document-wide summarization
- More precise page-level citations
- Improved retrieval across multiple documents
- Persistent vector storage
- Deployment to a cloud platform

## Security

- Keep API keys in environment variables.
- Do not commit `.env`, virtual environments, or private documents.
- Review `.gitignore` before pushing changes to GitHub.
