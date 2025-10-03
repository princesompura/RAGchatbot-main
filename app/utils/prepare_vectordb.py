from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from utils.ocr import perform_ocr, text_to_pdf
import os
import sqlite3

def _looks_empty(pdf_path: str) -> bool:
    """True if page 1 has no selectable text."""
    try:
        first_page = PdfReader(pdf_path).pages[0].extract_text()
        return not first_page or len(first_page.strip()) == 0
    except Exception:
        return True

def extract_pdf_text(pdfs):
    """
    Return a list[Document] for every PDF.
    If the PDF has no selectable text, run OCR, dump it into
    docs/<name>_ocr.pdf, then load that new PDF.
    """
    docs = []
    for pdf in pdfs:
        pdf_path = os.path.join("docs", pdf)

        # 1️⃣ try normal extraction
        native = PyPDFLoader(pdf_path).load()

        # 2️⃣ if empty → OCR
        if not native or _looks_empty(pdf_path):
            print(f"OCR fallback for {pdf}")
            text = perform_ocr(pdf_path)
            if text.strip():
                ocr_pdf = pdf_path.replace(".pdf", "_ocr.pdf")
                text_to_pdf(text, ocr_pdf)
                native = PyPDFLoader(ocr_pdf).load()

        docs.extend(native)
    return docs

def get_text_chunks(docs):
    """
    Split text into chunks

    Parameters:
    - docs (list): List of text documents

    Returns:
    - chunks: List of text chunks
    """
    # Chunk size is configured to be an approximation to the model limit of 2048 tokens
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=8000, chunk_overlap=800, separators=["\n\n", "\n", " ", ""])
    chunks = text_splitter.split_documents(docs)
    return chunks

def get_vectorstore(pdfs, from_session_state=False):
    """
    Create or retrieve a vectorstore from PDF documents

    Parameters:
    - pdfs (list): List of PDF documents
    - from_session_state (bool, optional): Flag indicating whether to load from session state. Defaults to False

    Returns:
    - vectordb or None: The created or retrieved vectorstore. Returns None if loading from session state and the database does not exist
    """
    load_dotenv()
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    if from_session_state and os.path.exists("Vector_DB - Documents"):
        # Retrieve vectorstore from existing one
        vectordb = Chroma(persist_directory="Vector_DB - Documents", embedding_function=embedding)
        return vectordb
    elif not from_session_state:
        docs = extract_pdf_text(pdfs)
        chunks = get_text_chunks(docs)
        # Create vectorstore from chunks and saves it to the folder Vector_DB - Documents
        vectordb = Chroma.from_documents(documents=chunks, embedding=embedding, persist_directory="Vector_DB - Documents")
        return vectordb
    return None