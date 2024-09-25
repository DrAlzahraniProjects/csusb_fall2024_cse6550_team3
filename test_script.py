import os
import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_community.chat_models import ChatOllama
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from redis import Redis
from cachetools import TTLCache
from concurrent.futures import ThreadPoolExecutor
from langchain.retrievers.multi_query import MultiQueryRetriever
# Set the title of the app
st.set_page_config(page_title="Hybrid Retrieval Chatbot", layout="wide")
st.title("Hybrid Retrieval Chatbot")

# Initialize session state if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Define necessary variables
main_storage = "storage-db"
document_path = 'data'
collection_name = 'text-book'
storage_directory = main_storage + 'textbook'

# Define system and prompt templates
system_prompt = (
    "You are an assistant specializing in answering questions based solely on the provided context. "
    "Use the following pieces of retrieved context to answer the question accurately. "
    "Do not use external information. "
    "If the context does not contain enough information, say 'I don't know'. "
    "Always include the file name and page number in your answer when providing information from the context. "
    "\n\n{context}"
)

# Create a prompt template for chat
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# Load the language model
llm = ChatOllama(model='llama3.1')

# Create a question-answer chain using LLM and prompt
question_answer_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)

# Function to load and split PDF documents from a directory
def load_documents_from_directory(document_path: str):
    documents = PyPDFDirectoryLoader(document_path).load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2048, chunk_overlap=200)
    return text_splitter.split_documents(documents)

# Function to load or create a vector store
def load_or_create_vector_store(documents, collection_name, persist_directory):
    embedding_function = GPT4AllEmbeddings()
    if os.path.exists(persist_directory) and len(os.listdir(persist_directory)) > 0:
        return Chroma(persist_directory=persist_directory, embedding_function=embedding_function, collection_name=collection_name)
    else:
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=embedding_function,
            persist_directory=persist_directory,
            collection_name=collection_name
        )
        vector_store.persist()
        return vector_store

# Prepare context from retrieved documents
def prepare_context(reranked_docs):
    context = ""
    for doc in reranked_docs:
        file_name = doc.metadata.get("file_name", "Unknown")
        page_number = doc.metadata.get("page_number", "Unknown")
        page_content = doc.page_content
        context += f"File: {file_name}, Page: {page_number}\n{page_content}\n\n"
    return context

# Main handler for the question
def handle_question(question, document_path, collection_name, storage_directory):
    # Check if vector store exists
    if os.path.exists(storage_directory) and len(os.listdir(storage_directory)) > 0:
        # Load existing vector store
        vector_store = load_or_create_vector_store([], collection_name, storage_directory)
        documents = load_documents_from_directory(document_path)
    else:
        # Load documents and create new vector store
        documents = load_documents_from_directory(document_path)
        vector_store = load_or_create_vector_store(documents, collection_name, storage_directory)

    # Initialize BM25 retriever and chroma retriever
    bm25_retriever = BM25Retriever.from_documents(documents, k=10)
    chroma_retriever = vector_store.as_retriever(search_kwargs={'k': 10, 'score_threshold': 0.4})

    # Ensemble retriever with BM25 and Chroma
    fusion_retriever = EnsembleRetriever(retrievers=[bm25_retriever, chroma_retriever], weights=[0.5, 0.5])

    # Retrieve and rerank the documents
    reranked_docs = fusion_retriever.get_relevant_documents(question)

    # Prepare context for LLM
    context = prepare_context(reranked_docs)

    # Get the final answer and pass the context to LLM
    result = question_answer_chain.run(input=question, context=context)

    # Ensure the model only provides answers based on the retrieved context
    if "I don't know" in result:
        return {"answer": "The context provided does not contain sufficient information to answer this question."}

    return {"answer": result}

# Function to handle user input
def handle_user_input_request(user_input):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    # Call the RAG function to get the bot's response
    result = handle_question(user_input, document_path, collection_name, storage_directory)
    bot_response = result['answer']
    st.session_state.chat_history.append({"role": "bot", "content": bot_response})

# Display chat history
for message in st.session_state.chat_history:
    if message['role'] == 'user':
        st.markdown(
            f"<div style='text-align: right; color: blue;'>{message['content']}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div style='text-align: left; color: green;'>{message['content']}</div>",
            unsafe_allow_html=True,
        )

# User input
user_input = st.text_input("Enter your question here")

if user_input:
    handle_user_input_request(user_input)
