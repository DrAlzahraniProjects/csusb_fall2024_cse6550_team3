# load_documents_to_vector_store.py
import os
import logging
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from create_vector_store import load_or_create_vector_store  # Assuming this is in the same directory as script 1

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to load and split PDF documents from a directory
def load_documents_from_directory(document_path: str):
    logger.info(f"Loading documents from {document_path}...")
    documents = PyPDFDirectoryLoader(document_path).load_and_split()
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=2048, chunk_overlap=200)
    return text_splitter.split_documents(documents)

if __name__ == "__main__":
    # Path to the directory containing the PDF documents
    document_path = './docs'
    
    # Load and split documents
    documents = load_documents_from_directory(document_path)
    
    # Load or create vector store
    collection_name = "example_collection"
    persist_directory = "./faiss_vectorstore"

    # Load or create vector store using the documents loaded
    vector_store = load_or_create_vector_store(documents, collection_name, persist_directory)
