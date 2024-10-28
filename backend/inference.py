import os
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_mistralai import ChatMistralAI
from guardrails import Guard
from .document_loading import (
    load_documents_from_directory, 
    load_or_create_faiss_vector_store,
    get_hybrid_retriever
)
from .prompts import prompt
from .citations import get_answer_with_source

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
faiss_store = load_or_create_faiss_vector_store(documents, "pdf_collection", persist_directory)
retriever = get_hybrid_retriever(documents=documents, vector_store=faiss_store, k=top_k)

###################
# MODEL INFERENCE #
###################

api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in .env")

def load_llm_api(model_name):
    """Load and configure Mistral AI LLM."""
    return ChatMistralAI(
        model=model_name,
        mistral_api_key=api_key,
        temperature=0.2,
        max_tokens=256,
        top_p=0.4,
    )

MODEL_NAME = "open-mistral-7b"
llm = load_llm_api(MODEL_NAME)

# Load guardrails configuration
GUARDRAILS_CONFIG_PATH = "guardrails_config.xml"
guard = Guard.from_rail(GUARDRAILS_CONFIG_PATH)

def chat_completion(question):
  """
  Generate a response to a given question using the RAG (Retrieval-Augmented Generation) chain,
  streaming parts of the response as they are generated.

  Args:
    question (str): The user question to be answered.

  Yields:
    str: The generated response in chunks.
  """
  print(f"Running prompt: {question}")
  question_answer_chain = create_stuff_documents_chain(llm, prompt)
  rag_chain = create_retrieval_chain(retriever, question_answer_chain)

  # Stream response from LLM
  full_response = {"answer": "", "context": []}
  for chunk in rag_chain.stream({"input": question}):
    if "answer" in chunk:
      full_response["answer"] += chunk["answer"]
      yield (chunk["answer"], MODEL_NAME)
    if "context" in chunk:
      full_response["context"].extend(chunk["context"])

  # After streaming is complete, use the full response to extract citations
  final_answer = get_answer_with_source(full_response)
  # Yield any remaining part of the answer with citations
  remaining_answer = final_answer[len(full_response["answer"]):]
  if remaining_answer:
    yield (remaining_answer, MODEL_NAME)