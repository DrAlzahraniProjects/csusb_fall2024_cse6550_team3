# create_vector_store.py
import os
import logging
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import FAISS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to load or create a FAISS vector store and save locally
def load_or_create_vector_store(documents, collection_name, persist_directory):
    embedding_function = GPT4AllEmbeddings()
    
    # Path to save the FAISS index
    index_file_path = os.path.join(persist_directory, collection_name)

    # Check if the FAISS index exists
    if os.path.exists(index_file_path):
        logger.info(f"Loading existing FAISS vector store from {index_file_path}")
        return FAISS.load_local(index_file_path, embedding_function)
    
    else:
        logger.info(f"Creating new FAISS vector store in {persist_directory}")
        vector_store = FAISS.from_documents(documents, embedding_function)
        
        # Save the FAISS index locally
        os.makedirs(persist_directory, exist_ok=True)
        vector_store.save_local(index_file_path)
        
        return vector_store

if __name__ == "__main__":
    # Replace with actual documents and paths
    documents = []  # Load documents here
    collection_name = "example_collection"
    persist_directory = "./faiss_vectorstore"

    vector_store = load_or_create_vector_store(documents, collection_name, persist_directory)
