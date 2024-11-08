import os
from langchain_mistralai import ChatMistralAI
from .document_loading import (
    load_documents_from_directory, 
    load_or_create_faiss_vector_store,
    similarity_search,
)
from .prompts import prompt
from .citations import get_citations, format_citations

# Import and load environment variables
from dotenv import load_dotenv
load_dotenv(override=True)

###################
# LOAD EMBEDDINGS #
###################

document_path = os.getenv("CORPUS_SOURCE")
persist_directory = os.path.join(document_path, "faiss_indexes")
documents = load_documents_from_directory(document_path)
faiss_store = load_or_create_faiss_vector_store(documents, persist_directory)

###################
# MODEL INFERENCE #
###################

api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in .env")

def load_llm_api(model_name):
    """
    Load and configure the Mistral AI LLM.
    Returns:
        ChatMistralAI: Configured LLM instance.
    """
    return ChatMistralAI(
        model=model_name,
        mistral_api_key=api_key,
        temperature=0.2,
        max_tokens=256,
        top_p=0.4,
    )

MODEL_NAME = "open-mistral-7b"
llm = load_llm_api(MODEL_NAME)

def chat_completion(question):
    """
    Generate a response to a given question using an LLM to determine relevance,
    then conditionally provide citations if the content is relevant.
    """
    print(f"Running prompt: {question}")
    
    # Initial LLM response check for relevance
    initial_response = llm.query(question)  # You need to define or adjust this method based on your LLM's capabilities
    
    # If LLM determines the content is relevant, then fetch documents and format citations
    if initial_response['relevance'] > 0.5:
        relevant_docs = similarity_search(question, faiss_store, 10)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        messages = prompt.format_messages(input=question, context=context)

        full_response = {"answer": initial_response['text'], "context": relevant_docs}
        for chunk in llm.stream(messages):
            full_response["answer"] += chunk.content
            yield (chunk.content, MODEL_NAME)

        page_numbers = get_citations(relevant_docs)
        if page_numbers:
            citations = format_citations(page_numbers)
            yield (citations, MODEL_NAME)
    else:
        # Handle case where LLM does not find relevant content in the textbook
        yield (initial_response['text'], MODEL_NAME)

