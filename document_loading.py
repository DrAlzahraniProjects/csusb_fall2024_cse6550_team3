from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.retrievers import BM25Retriever, EnsembleRetriever
import faiss
import os
model_kwargs = {'trust_remote_code': True}

EMBEDDING_MODEL_NAME = "Alibaba-NLP/gte-large-en-v1.5"  # HuggingFace embedding model
EMBEDDING_FUNCTION = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME,model_kwargs = model_kwargs)



# Function to load and split PDF documents from a directory
def load_documents_from_directory(document_path: str, chunk_size: int = 2048, chunk_overlap: int = 200):
    # logger.info(f"Loading documents from {document_path}...")
    print(f"Loading documents from {document_path}...")
    documents = PyPDFDirectoryLoader(document_path).load_and_split()
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(documents)
def load_or_create_faiss_vector_store(documents, collection_name, persist_directory):
    index_path = os.path.join(persist_directory, f'{collection_name}_faiss_index')

    if os.path.exists(index_path):
        print(f"Loading existing FAISS vector store from {index_path}")
        faiss_store = FAISS.load_local(index_path, embeddings=EMBEDDING_FUNCTION,allow_dangerous_deserialization=True)
    else:
        print(f"Creating new FAISS vector store in {index_path}")
        faiss_store = FAISS.from_documents(documents, embedding=EMBEDDING_FUNCTION)
        faiss_store.save_local(index_path)

    return faiss_store

def get_hybrid_retriever(documents, vector_store,k):
    bm25_retriever = BM25Retriever.from_documents(documents, search_kwargs={'k': k})
    chroma_retriever = vector_store.as_retriever(search_kwargs={'k': k})
    fusion_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, chroma_retriever],
        weights=[0.6, 0.4]
    )
    return fusion_retriever



