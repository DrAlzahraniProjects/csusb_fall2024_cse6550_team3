import os
import time
import asyncio
from typing import List, Dict
from langchain_mistralai import ChatMistralAI
from nemoguardrails import RailsConfig
from nemoguardrails.streaming import StreamingHandler
from nemoguardrails.llm.providers import register_llm_provider
from nemoguardrails.integrations.langchain.runnable_rails import RunnableRails
from .prompts import get_prompt, rewrite_prompt, sanitize_question, validate_question, replace_text
from .citations import get_citations, format_citations
from .document_loading import load_documents_from_directory, load_or_create_faiss_vector_store, similarity_search

# Import and load environment variables
from dotenv import load_dotenv
load_dotenv(override=True)

config = RailsConfig.from_path("/app/backend/guardrails.yml")

UNANSWERABLE_MSG = """
    I'm a chatbot that answers questions about SWEBOK (Software Engineering Body of Knowledge).
    Your question appears to be about something else.
    Could you ask a question related to software engineering fundamentals, requirements, design, construction, testing, maintenance, configuration management, engineering management, processes, models, or quality?
    """

###################
# LOAD EMBEDDINGS #
###################

def load_faiss_vector_store(document_path: str, persist_directory: str) -> any:
    """Loads the FAISS vector store or creates a new one if it doesn't exist."""
    documents = load_documents_from_directory(document_path)
    return load_or_create_faiss_vector_store(documents, persist_directory)

# Load documents and the embeddings from the FAISS vector store
document_path = os.getenv("CORPUS_SOURCE")
persist_directory = os.path.join(document_path, "faiss_indexes")
faiss_store = load_faiss_vector_store(document_path, persist_directory)


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

def load_llm_api(model_name: str, max_tokens: int) -> ChatMistralAI:
    """Load and configure the Mistral AI LLM"""
    api_key = get_api_key()
    return ChatMistralAI(
        model=model_name,
        mistral_api_key=api_key,
        temperature=0,
        max_tokens=max_tokens,
    )
MODEL_NAME = "open-mistral-7b"
llm = load_llm_api(MODEL_NAME, 256)
rewrite_llm = load_llm_api(MODEL_NAME, 40)
register_llm_provider("mistral", ChatMistralAI)
guardrails = RunnableRails(config, input_key="question", output_key="answer")

def fetch_relevant_documents(question: str) -> str:
    """Retrieve relevant documents from the vector store based on the question"""
    top_k = 2  # Number of relevant documents to be returned
    distance_threshold = 400 # Set lower values for stricter filtering
    similar_docs = similarity_search(question, faiss_store, top_k, distance_threshold)
    # print("Scores:", [score for _, score in similar_docs])
    low_distance_docs = [[doc, score] for doc, score in similar_docs if score < 320]
    relevant_docs = low_distance_docs[:2] if len(low_distance_docs) != 0 else similar_docs[:1]
    relevant_docs = [doc_pair[0] for doc_pair in relevant_docs]
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    # print("Relevant docs", relevant_docs)
    # print("Context", context)
    return relevant_docs, context

def rewrite_question(question):
    rewrite_template = rewrite_prompt()
    rewrite_message = rewrite_template.format_messages(text=question)
    new_question = rewrite_llm.invoke(rewrite_message).content.strip()
    relevant_docs, context = fetch_relevant_documents(new_question)
    # print("Rewritten", new_question)
    if relevant_docs:
        time.sleep(1) # Avoids getting rate limited by the mistral api
        return new_question, relevant_docs, context
    else:
        return None, None, None

def chat_completion(question: str) -> tuple[str, str]:
    """Generate a response to a given question using simple RAG approach, yielding the full response after invocation"""
    # print(f"Running prompt: {question}")
    
    # Validate question
    is_valid = validate_question(question)
    if not is_valid:
        yield (UNANSWERABLE_MSG, "N/A")
        return
    
    # Fetch relevant documents
    relevant_docs, context = fetch_relevant_documents(question)
    if not relevant_docs:
        # print("Replacing abbreviations in question")
        question = replace_text(question)
        relevant_docs, context = fetch_relevant_documents(question)
        # print("New question", question)
        if not relevant_docs:
            # print("Question is being santized...")
            question = sanitize_question(question)
            relevant_docs, context = fetch_relevant_documents(question)
            # print("New question", question)
            if not relevant_docs:
                # print("Question is being rewritten...")
                question, relevant_docs, context = rewrite_question(question)
                if question is None:
                    yield (UNANSWERABLE_MSG, MODEL_NAME)
                    return

    # Prepare prompt and input
    formatted_input = f"<question>{question}</question>\n\n<context>{context}<context>"
    input_dict = {"input": formatted_input}
    # Invoke LLM with Guardrails
    try:
        invoke_response = guardrails.invoke(input_dict)
        if not invoke_response or "output" not in invoke_response:
            raise ValueError(f"Unexpected response structure: {invoke_response}")
        
        answer = invoke_response.get("output", "")
        # print(f"Generated answer: {answer}")
        yield (answer, MODEL_NAME)

        # Handle citations if available
        if relevant_docs:
            response = invoke_response.get("output", "")
            if response:
                page_numbers = get_citations(relevant_docs)
                if page_numbers:
                    citations = format_citations(page_numbers, response)
                    if citations:
                        yield (citations, MODEL_NAME)
    except Exception as e:
        print(f"Error during invocation: {e}")
        raise