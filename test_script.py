import os
from langchain.vectorstores import Milvus
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
import streamlit as st
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Provide detailed and well-formatted responses based on the context and also mention the page number from which the information is taken."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

llm = ChatOllama(model_name='mistral')  # Or another model
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)
def load_documents_from_directory(document_path: str):
    loader = PyPDFDirectoryLoader(document_path)
    documents = loader.load()
    for doc in documents:
        doc.metadata["file_name"] = os.path.basename(doc.metadata.get("source", "unknown"))
        doc.metadata["page_number"] = doc.metadata.get("page", "unknown")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)
    split_docs = text_splitter.split_documents(documents)
    return split_docs

def load_or_create_vector_store(documents, collection_name):
    embedding_function = GPT4AllEmbeddings()
    milvus_url = "localhost"
    milvus_port = "19530"
    vector_store = Milvus(
        embedding_function=embedding_function,
        collection_name=collection_name,
        connection_args={"host": milvus_url, "port": milvus_port}
    )
    if vector_store.check_existing_collection():
        print(f"Loading existing vector store from collection '{collection_name}' in Milvus.")
        return vector_store
    else:
        print(f"Creating new vector store in collection '{collection_name}' in Milvus.")
        vector_store = Milvus.from_documents(
            documents=documents,
            embedding=embedding_function,
            collection_name=collection_name,
            connection_args={"host": milvus_url, "port": milvus_port}
        )
        return vector_store

document_path = 'test-data'
collection_name = 'resume'

documents = load_documents_from_directory(document_path)

# Initialize vector store
vector_store = load_or_create_vector_store(documents, collection_name)

# Initialize retrievers
bm25_retriever = BM25Retriever.from_documents(documents)
milvus_retriever = vector_store.as_retriever(search_kwargs={"k": 10})

fusion_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, milvus_retriever],
    weights=[0.3, 0.7]
)

# Initialize compressor


question = st.chat_input("Type your question here ")

retrieved_docs = fusion_retriever.get_relevant_documents(question)

# Step 4: Initialize the CrossEncoderReranker
cross_encoder = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
reranker = CrossEncoderReranker(model=cross_encoder, top_n=5)




