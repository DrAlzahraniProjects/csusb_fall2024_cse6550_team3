# interface.py
import os
from langchain_mistralai import ChatMistralAI
from .document_loading import load_documents_from_directory, load_or_create_faiss_vector_store, similarity_search
from .citations import get_citations, format_citations
from .prompts import prompt

# Load environment variables
from dotenv import load_dotenv
load_dotenv(override=True)

document_path = os.getenv("CORPUS_SOURCE")
persist_directory = os.path.join(document_path, "faiss_indexes")
documents = load_documents_from_directory(document_path)
faiss_store = load_or_create_faiss_vector_store(documents, persist_directory)

api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in .env")

def load_llm_api(model_name):
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
    Use LLM to check answer relevance and conditionally format responses with citations.
    """
    print(f"Running prompt: {question}")
    relevant_docs = similarity_search(question, faiss_store, 10)
    context = "\n\n".join([doc['text'] for doc in relevant_docs])
    response = llm.generate_answer(question, context)  # This should be a method to handle LLM response generation

    if relevant_docs and response.relevance_score > 0.5:  # Assuming LLM responses include a relevance score
        page_numbers = get_citations(relevant_docs)
        citations = format_citations(page_numbers)
        response_text = f"{response.text} {citations}"
    else:
        response_text = response.text

    return response_text

def main():
    """
    Main function to run the Streamlit interface.
    """
    if "view" in st.query_params and st.query_params["view"] == "pdf":
        serve_pdf()  # Ensure this function is defined elsewhere in your project
    else:
        if prompt := st.text_input("Ask your question?"):
            response = chat_completion(prompt)
            st.markdown(f"<div class='response'>{response}</div>", unsafe_allow_html=True)

