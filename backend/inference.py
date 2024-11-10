import os
from .document_loading import load_documents_from_directory, load_or_create_faiss_vector_store, similarity_search
from .prompts import prompt
from .citations import get_citations, format_citations
from langchain_mistralai import ChatMistralAI
from nemoguardrails import RailsConfig
from nemoguardrails.integration.langchain.runnable_rails import RunnableRails
config = RailsConfig.from_path("guardrails.yml")
guardrails = RunnableRails(config)

# Load environment variables
from dotenv import load_dotenv
load_dotenv(override=True)

###################
# LOAD EMBEDDINGS #
###################

# Load documents and FAISS vector store
document_path = os.getenv("CORPUS_SOURCE", "data/default/textbook")
persist_directory = "data/default/faiss_indexes"
top_k = 15

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
    Generate a response to a given question using simple RAG approach, streaming parts of the response as they are generated.
    Args:
      question (str): The user question to be answered.
    Yields:
      tuple[str, str]: The generated response chunk and model name.
    """
    print(f"Running prompt: {question}")
  
    # Get relevant documents from the FAISS store
    relevant_docs = similarity_search(question, faiss_store, 10)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    messages = prompt.format_messages(input=question,context=context)
  
    # Stream response from LLM
    full_response = {"answer": "", "context": relevant_docs}
    llm_with_guardrails = guardrails | llm
    for chunk in llm_with_guardrails.stream(messages):
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
