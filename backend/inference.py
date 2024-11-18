import os
from typing import List, Dict
from langchain_mistralai import ChatMistralAI
from .prompts import get_prompt
from .citations import get_citations, format_citations
from .document_loading import load_documents_from_directory, load_or_create_faiss_vector_store, similarity_search
from nemoguardrails import RailsConfig, LLMRails
print(RailsConfig.schema())
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
    Generate a response to a given question using Retrieval-Augmented Generation (RAG)
    with Nemo Guardrails, streaming parts of the response as they are generated.
    Args:
        question (str): The user question to be answered.
    Yields:
        tuple[str, str]: The generated response chunk and model name.
    """
    print(f"Running prompt with Guardrails: {question}")
    config = RailsConfig.from_path("config.yaml")  # Assuming you have a config file for Guardrails
    print(config.dict())  # This will print the configuration as a dictionary


    try:
        # Get relevant context (same as your original function)
        relevant_docs, context = fetch_relevant_documents(question)

        # Get the appropriate prompt format (you can keep this the same or modify as needed)
        prompt = get_prompt(has_context=bool(relevant_docs))

        # Pass the relevant context and user question to Guardrails
        config = RailsConfig.from_path("config.yaml")  # Assuming you have a config file for Guardrails
        rails = LLMRails(config)
        
        # Define the message structure with relevant context and user input
        messages = [
            {"role": "context", "content": {"relevant_chunks": context}},
            {"role": "user", "content": question}
        ]

        # Use Guardrails to generate the response
        response = rails.generate(messages=messages)

        # Stream the response as it's generated
        full_response = {"answer": response["content"], "context": relevant_docs}
        yield (full_response["answer"], "Mistral")

        # Handle citations if applicable (if relevant_docs exists)
        if relevant_docs:
            page_numbers = get_citations(relevant_docs)
            if page_numbers:
                response_with_citations = full_response["answer"]
                citations = format_citations(page_numbers, response_with_citations)
                if citations:
                    yield (citations, "Mistral")

    except Exception as e:
        # If an error occurs, use the fallback answer from the YAML
        fallback_answer = config.rails_config.get('guardrails', {}).get('error_handling', {}).get('fallback_answer', 'Sorry, I couldn\'t process your request. Please try again later.')
        yield (fallback_answer, "Mistral")