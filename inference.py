import os
from roman import toRoman
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from document_loading import (
	load_documents_from_directory, 
	load_or_create_faiss_vector_store,
	get_hybrid_retriever
)

# Import and load environment variables
from dotenv import load_dotenv
load_dotenv(override=True)

###################
# LOAD EMBEDDINGS #
###################

# Load documents and the embeddings from the FAISS vector store
document_path = "data/textbook"
documents = load_documents_from_directory(document_path)
faiss_store = load_or_create_faiss_vector_store(documents, "pdf_collection", "faiss_indexes")
top_k = 15 # number of relevant documents to be returned
retriever = get_hybrid_retriever(
	documents = documents,
	vector_store = faiss_store, 
	k = top_k
)


###################
# MODEL INFERENCE #
###################

# Get Mistral API Key from the environment variables
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
	raise ValueError("MISTRAL_API_KEY not found in .env")

MODEL_NAME = "open-mistral-7b"
def load_llm_api():
	"""
	Load and configure the Mistral AI LLM.
	Returns:
		ChatMistralAI: Configured LLM instance.
	"""
	return ChatMistralAI(
		model=MODEL_NAME,
		mistral_api_key=api_key,
		temperature=0.2,
		max_tokens=256,
		top_p=0.4,
	)
llm = load_llm_api()

def get_answer_with_source(response):
  """
  Extract the answer and relevant source information from the response.
  This function processes the response from the RAG chain, extracting the answer
  and up to 3 source references (page numbers) from the context documents.

  Args:
    response (dict): The response dictionary from the RAG chain, containing 'answer' and 'context' keys.
  Returns:
    str: A formatted string containing the answer followed by source information.
  """
  answer = response.get('answer', 'No answer found.') # Extract the answer
  sources = [] # Handle multiple contexts in the response (assuming response['context'] is a list)

  # Iterate over the list of context documents and collect up to top 5 sources
  for doc in response['context'][:5]:
    file_name = os.path.basename("data/textbook/Roger S. Pressman_ Bruce R. Maxim - Software Engineering_ A Practitioner's Approach-McGraw-Hill Education (2019).pdf")
    page = doc.metadata.get('page', 'Unknown page')

    # The documents are zero indexed. So page 1 of the pdf is page 0 in docs
    # Chapter 1 starts at doc 33 (page 34 of the PDF)
    adjusted_page = page - 33 
    if adjusted_page >= 0: # For pages starting from Chapter 1
      link = f'<a href="/team3/?view=pdf&file={file_name}&page={page + 1}" target="_blank">[{adjusted_page + 1}]</a>'
    else: # For pages before Chapter 1
      adjusted_page = "Cover" if page == 0 else toRoman(page)
      link = f'<a href="/team3/?view=pdf&file={file_name}&page={page + 1}" target="_blank">[{adjusted_page}]</a>'
    sources.append(link)

  # Join the top 5 sources with newlines
  sources_info = "\nSources: " + "".join(sources)
  final_answer = f"{answer}\n\n{sources_info}"
  return final_answer


# Prompts
system_prompt = """
You are a chatbot answering questions about "Software Engineering: A Practitioner's Approach" textbook.

1. Always identify yourself as a chatbot, not the textbook.
2. Answer based only on provided context.
3. If unsure, say "I don't have enough information to answer."
4. For unclear questions, ask for clarification.
5. Keep responses under 256 tokens.
6. Don't invent information.
7. Use context only if relevant.
8. To questions about your purpose, say: "I'm a chatbot designed to answer questions about the 'Software Engineering: A Practitioner's Approach' textbook."

Be accurate and concise. Answer only what's asked.
"""

prompt = ChatPromptTemplate.from_messages([
  ("system", system_prompt),
  ("human", "Question: {input}\n\nRelevant Context:\n{context}"),
])


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