# RAG - ChatBot 🤖

A Retrieval-Augmented Generation (RAG) chatbot built using **Streamlit**, **ChromaDB**, and **local models** (no API limits!). Users can upload PDFs and query them with context-aware responses powered by semantic vector search and open-source language models.

![snapshot of the webapp](image.png)

# LINK

[https://ragchatbot-main-prs.streamlit.app/](https://ragchatbot-main-prs.streamlit.app/)

# Features 🚀

- **Semantic Search** with ChromaDB
- **PDF Parsing** with OCR fallback for scanned documents
- **LLM Integration** using Hugging Face Transformers (local chat model)
- **Embeddings** via SentenceTransformers (local, fast, no API key)
- **Interactive UI** built with Streamlit
- **Context-Aware QA** from custom documents

# Tech Stack 🛠️

| Tool        | Purpose                        |
|-------------|--------------------------------|
| [Streamlit](https://streamlit.io/) | UI and interaction frontend |
| [ChromaDB](https://www.trychroma.com/) | Vector storage and retrieval |
| [sentence-transformers](https://www.sbert.net/) | Local embeddings |
| [transformers](https://huggingface.co/docs/transformers/index) | Local chat LLM |
| [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) | OCR fallback for non-extractable PDFs |
| [pdf2image](https://pypi.org/project/pdf2image/) | PDF page rendering for OCR |
| [PyMuPDF / fitz](https://pymupdf.readthedocs.io/) | Text extraction from PDFs |




## Features

- Upload PDF documents and chat with them using Retrieval-Augmented Generation (RAG)
- ChromaDB for vector storage and semantic search
- Embeddings: `sentence-transformers/all-MiniLM-L6-v2`
- Chat: `distilgpt2` (Hugging Face Transformers)
- OCR fallback for scanned PDFs (Tesseract, Poppler)
- Streamlit UI for upload and chat

## Quickstart

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Install system dependencies (for OCR):
   - On Ubuntu: `sudo apt install poppler-utils tesseract-ocr`
   - On Windows: Download and install [Poppler](http://blog.alivate.com.au/poppler-windows/) and [Tesseract](https://github.com/tesseract-ocr/tesseract)
3. Run the app:
   ```bash
   streamlit run app/app.py
   ```

## Tech Stack

- Python
- Streamlit
- ChromaDB
- LangChain
- Hugging Face Transformers
- SentenceTransformers
- Tesseract OCR
- Poppler

## File Overview

- `app/app.py`: Main Streamlit app
- `app/utils/prepare_vectordb.py`: Document loading, chunking, embedding
- `app/utils/chatbot.py`: Chat logic
- `app/utils/ocr.py`: OCR fallback
- `app/utils/save_docs.py`: Save uploaded docs
- `app/utils/session_state.py`: Session management
- `requirements.txt`: Python dependencies
- `packages.txt`: System dependencies

## Example Usage

1. Upload a PDF
2. Ask questions about its content
3. The chatbot retrieves relevant context and answers using the local model

## Credits

- Built with Streamlit, ChromaDB, LangChain, Hugging Face Transformers, SentenceTransformers
- OCR via Tesseract and Poppler





