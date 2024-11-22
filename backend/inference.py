import os
import time
from typing import List, Dict
from langchain_mistralai import ChatMistralAI
from .prompts import get_prompt, rewrite_prompt
from .citations import get_citations, format_citations
from .document_loading import load_documents_from_directory, load_or_create_faiss_vector_store, similarity_search

# Import and load environment variables
from dotenv import load_dotenv
load_dotenv(override=True)

###################
# LOAD EMBEDDINGS #
###################

def load_faiss_vector_store(document_path: str, persist_directory: str, top_k: int) -> any:
    """Loads the FAISS vector store or creates a new one if it doesn't exist."""
    documents = load_documents_from_directory(document_path)
    return load_or_create_faiss_vector_store(documents, persist_directory)

# Load documents and the embeddings from the FAISS vector store
document_path = os.getenv("CORPUS_SOURCE")
persist_directory = os.path.join(document_path, "faiss_indexes")
top_k = 15  # number of relevant documents to be returned
faiss_store = load_faiss_vector_store(document_path, persist_directory, top_k)


###################
# MODEL INFERENCE #
###################

class APIKeyNotFoundError(Exception):
    """Custom exception raised when API key is not found."""
    pass

def get_api_key() -> str:
    """Retrieves the MISTRAL_API_KEY from environment variables."""
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key or not isinstance(api_key, str) or not api_key.strip():
        raise APIKeyNotFoundError("MISTRAL_API_KEY not found or invalid in .env")
    return api_key

def load_llm_api(model_name: str) -> ChatMistralAI:
    """
    Load and configure the Mistral AI LLM.
    Returns:
        ChatMistralAI: Configured LLM instance.
    """
    api_key = get_api_key()
    return ChatMistralAI(
        model=model_name,
        mistral_api_key=api_key,
        temperature=0.05,
        max_tokens=256,
        top_p=0.4,
    )
MODEL_NAME = "open-mistral-7b"
llm = load_llm_api(MODEL_NAME)

def fetch_relevant_documents(question: str) -> str:
    """
    Retrieve relevant documents from the vector store based on the question.
    Args:
        question (str): User's input question
    Returns:
        str: Concatenated content of relevant documents
    """
    relevant_docs = similarity_search(question, faiss_store, 10)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    return relevant_docs, context

def chat_completion(question: str) -> tuple[str, str]:
    """
    Generate a response to a given question using simple RAG approach, streaming parts of the response as they are generated.
    Args:
        question (str): The user question to be answered.
    Yields:
        tuple[str, str]: The generated response chunk and model name.
    """
    print(f"Running prompt: {question}")
  
    # Get relevant context
    relevant_docs, context = fetch_relevant_documents(question)
    if len(relevant_docs) == 0:
        rewrite_template = rewrite_prompt()
        rewrite_message = rewrite_template.format_messages(text=question)
        question = llm.invoke(rewrite_message).content.strip()
        print(question)
        relevant_docs, context = fetch_relevant_documents(question)
        if len(relevant_docs) == 0 or "NONE" in question:
            yield (
                """
                I'm a chatbot that answers questions about SWEBOK (Software Engineering Body of Knowledge).
                Your question appears to be about something else.
                Could you ask a question related to software engineering fundamentals, requirements, design, construction, testing, maintenance, configuration management, engineering management, processes, models, or quality?
                """
            , MODEL_NAME)
            return
        time.sleep(0.5)

    # Get appropriate prompt
    prompt = get_prompt()
    messages = prompt.format_messages(input=question, context=context)

    # Stream response from LLM
    full_response = {"answer": "", "context": relevant_docs}
    for chunk in llm.stream(messages):
        full_response["answer"] += chunk.content
        yield (chunk.content, MODEL_NAME)

    # After streaming is complete, handle citations
    if relevant_docs:
        page_numbers = get_citations(relevant_docs)
        if page_numbers:
            response = full_response["answer"]
            citations = format_citations(page_numbers, response)
            if citations:
                yield (citations, MODEL_NAME)
