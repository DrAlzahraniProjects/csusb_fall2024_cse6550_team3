import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader

EMBEDDING_MODEL_NAME = "Alibaba-NLP/gte-large-en-v1.5"  # Embedding model
model_kwargs = {'trust_remote_code': True}
EMBEDDING_FUNCTION = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME, model_kwargs=model_kwargs)

def load_documents_from_directory(
    document_path: str,
    chunk_size: int = 200,
    chunk_overlap: int = 50
):
    """
    Load PDF documents from a directory and split them into chunks.
    Args:
        document_path (str): Path to the directory containing PDF files.
        chunk_size (int): Size of each text chunk (default: 512).
        chunk_overlap (int): Overlap between chunks (default: 50).
    Returns:
        List of document chunks.
    """
    print(f"Loading documents from {document_path}...")
    # Load PDF documents from the specified directory
    documents = PyPDFDirectoryLoader(document_path).load_and_split()
    # Create a text splitter using tiktoken encoder
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    # Split the documents into chunks
    return text_splitter.split_documents(documents)


def save_embeddings_per_file(
    document_path: str,
    persist_directory: str,
    chunk_size: int = 200,
    chunk_overlap: int = 50
):
    """
    Save embeddings for each PDF in the same folder as the PDF.
    Args:
        document_path (str): Path to the directory containing PDF files.
        persist_directory (str): Base directory to save embeddings.
        chunk_size (int): Size of each text chunk (default: 512).
        chunk_overlap (int): Overlap between chunks (default: 50).
    """
    print(f"Processing PDFs in {document_path}...")

    # Get list of PDF files
    pdf_files = [f for f in os.listdir(document_path) if f.endswith('.pdf')]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(document_path, pdf_file)
        file_name = os.path.splitext(pdf_file)[0]
        save_path = os.path.join(persist_directory, file_name)

        # Load and split the document
        print(f"Processing {pdf_file}...")
        documents = PyPDFDirectoryLoader(document_path).load_and_split()
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = text_splitter.split_documents(documents)

        # Create FAISS vector store for this document
        faiss_store = FAISS.from_documents(
            documents=chunks,
            embedding=EMBEDDING_FUNCTION
        )

        # Save FAISS index locally
        os.makedirs(save_path, exist_ok=True)
        faiss_store.save_local(save_path)
        print(f"Embeddings saved for {pdf_file} in {save_path}")


# Example Usage
document_path = "data/swebok"  # Path to the folder with PDF files
persist_directory = "data/swebok/faiss_indexes"  # Path to save embeddings
save_embeddings_per_file(document_path, persist_directory)
