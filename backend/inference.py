import os
import time
from typing import List, Tuple
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI
from nemoguardrails import RailsConfig
from nemoguardrails.llm.providers import register_llm_provider
from nemoguardrails.integrations.langchain.runnable_rails import RunnableRails
from .citations import handle_citations
from .prompts import (
    get_prompt,
    rewrite_prompt, 
    sanitize_question, 
    validate_question, 
    replace_text
)
from .document_loading import (
    load_documents_from_directory, 
    load_or_create_faiss_vector_store, 
    similarity_search,
    match_question,
    clean_text
)

# Load environment variables
load_dotenv(override=True)

# Configuration for Guardrails
config = RailsConfig.from_path("/app/backend/guardrails.yml")

# Generic responses
CORPUS_LINK = f"<a href=\"https://www.computer.org/education/bodies-of-knowledge/software-engineering\">SWEBOK (Software Engineering Body of Knowledge).</a>"
UNANSWERABLE_MSG = f"<p>I'm a chatbot that only answers questions about {CORPUS_LINK}<br> Your question appears to be about something else. Could you ask a question related to SWEBOK?</p>"

# -------------------------------
# Helper Functions
# -------------------------------

def load_faiss_vector_store(document_path: str, persist_directory: str) -> any:
    """
    Purpose: Load or create a FAISS vector store for document embeddings.
    Input:
        - document_path (str): Path to the directory containing documents.
        - persist_directory (str): Directory where the FAISS index is stored or will be created.
    Output: FAISS vector store object.
    Processing: Loads documents from the directory and builds/loads the FAISS vector store.
    """
    documents = load_documents_from_directory(document_path)
    return load_or_create_faiss_vector_store(documents, persist_directory)

def get_api_key(key_name: str) -> str:
    """
    Purpose: Retrieve the API key for Mistral AI from environment variables.
    Input: None
    Output: MISTRAL_API_KEY as a string.
    Processing: Fetches and validates the API key from the environment variables.
    """
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key or not isinstance(api_key, str) or not api_key.strip():
        raise ValueError("MISTRAL_API_KEY not found or invalid in .env")
    return api_key

# -------------------------------
# Core Functions
# -------------------------------

# Load documents and the embeddings from the FAISS vector store
document_path = os.getenv("CORPUS_SOURCE")
persist_directory = os.path.join(document_path, "faiss_indexes")
faiss_store = load_faiss_vector_store(document_path, persist_directory)

# Initialize the LLM
MODEL_NAME = "mistral-large-2411"
llm = ChatMistralAI(model=MODEL_NAME, mistral_api_key=get_api_key("MISTRAL_API_KEY"), temperature=0, max_tokens=500)
rewrite_llm = ChatMistralAI(model="open-mistral-7b", mistral_api_key=get_api_key("MISTRAL_API_KEY"), temperature=0, max_tokens=40)

# Guardrails
register_llm_provider("mistral", ChatMistralAI)
guardrails = RunnableRails(config, input_key="question", output_key="answer")

def fetch_relevant_documents(question: str) -> Tuple[List[str], str]:
    """
    Purpose: Fetch the most relevant documents for a given question.
    Input:
        - question (str): The user query to process.
    Output:
        - relevant_docs (List[str]): List of relevant documents.
        - context (str): Concatenated content from relevant documents for context.
    Processing: Searches the FAISS vector store for documents similar to the query.
    """
    top_k = 2
    distance_threshold = 400
    similar_docs = similarity_search(question, faiss_store, top_k, distance_threshold)
    # print("similar_docs", similar_docs)
    low_distance_docs = [[doc, score] for doc, score in similar_docs if score < 320]
    relevant_docs = low_distance_docs[:2] if len(low_distance_docs) != 0 else similar_docs[:1]
    relevant_docs = [doc_pair[0] for doc_pair in relevant_docs]
    for doc in relevant_docs:
        doc.page_content = clean_text(doc.page_content)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    return relevant_docs, context

def rewrite_question(question: str) -> Tuple[str, List[str], str]:
    """
    Purpose: Rewrite a user question for improved clarity or relevance.
    Input: question (str): Original user question.
    Output: new_question (str): Rewritten question.
    Processing: Uses a pre-defined template and language model to rewrite the question.
    """
    rewrite_message = rewrite_prompt().format_messages(text=question)
    new_question = rewrite_llm.invoke(rewrite_message).content.strip()
    return new_question

def update_question(question: str) -> Tuple[str, List[str], str]:
    """
    # Purpose: Process and improve question through multiple refinement steps
    # Input: Original user question string
    # Output: Tuple of processed question, relevant documents, and context
    # Processing: Applies text replacement, sanitization, and rewriting as needed
    """
    # Replace any abbreviations or acronyms
    new_question = replace_text(question)
    relevant_docs, context = fetch_relevant_documents(new_question)
    # print("Replaced q: ", new_question)
    if relevant_docs:
        return new_question, relevant_docs, context
    # Sanitize prompt
    new_question = sanitize_question(new_question)
    relevant_docs, context = fetch_relevant_documents(new_question)
    # print("Sanitized q: ", new_question)
    if relevant_docs:
        return new_question, relevant_docs, context
    # Rewrite prompt with an LLM
    new_question = rewrite_question(new_question.lower())
    relevant_docs, context = fetch_relevant_documents(new_question)
    # print("Question rewritten: ", new_question)
    if relevant_docs:
        time.sleep(1) # Avoids getting rate limited by the mistral api
        return new_question, relevant_docs, context
    return None, None, None

def chat_completion(question: str) -> Tuple[str, str]:
    """
    Purpose: Generate a response to a user query using the LLM and relevant citations.
    Input:
        - question (str): User query to process.
    Output:
        - response (str): Generated chatbot response.
        - model_name (str): Name of the model used for the response.
    Processing: Validates the query, retrieves context, and generates a response using the LLM.
    """
    print(f"Running prompt: {question}")
    is_valid = validate_question(question)
    question = question.strip()
    if not is_valid:
        yield (UNANSWERABLE_MSG, "N/A")
        return

    # Check if this question can be found in common questions (eg: summarize chapter)
    new_question, context = match_question(question)
    if new_question is not None and context is not None:
        if "chapter does not exist in the contents" in context:
            yield UNANSWERABLE_MSG, MODEL_NAME
            return
        relevant_docs, new_context = fetch_relevant_documents(new_question)
        if new_context is not None:
            question = new_question
            context += new_context
        

    # Update the user question to get better results
    else:
        relevant_docs, context = fetch_relevant_documents(question)
        if not relevant_docs:
            question, relevant_docs, context = update_question(question)
            if question is None:
                yield UNANSWERABLE_MSG, MODEL_NAME
                return

    # LLM inference using Nemo Guardrails
    messages = get_prompt().format_messages(input=question, context=context)
    # Stream response from LLM
    full_response = {"answer": ""}
    for chunk in llm.stream(messages):
        full_response["answer"] += chunk.content
        yield (chunk.content, MODEL_NAME)

    # Handle citations if available
    if relevant_docs:
        citations = handle_citations(relevant_docs)
        if citations:
            yield citations, MODEL_NAME
            return