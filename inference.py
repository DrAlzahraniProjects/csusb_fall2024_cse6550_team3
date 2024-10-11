import os
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
# from langchain_ollama import ChatOllama
# from langchain_community.llms import LlamaCpp
# from langchain.callbacks.manager import CallbackManager
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from llama_cpp import Llama
from document_loading import (
	load_documents_from_directory, 
	load_or_create_faiss_vector_store,
	get_hybrid_retriever
)

# Import and load environment variables
from dotenv import load_dotenv
load_dotenv(override=True)

######################
# HUGGING FACE LOGIN #
######################
# from huggingface_hub import login, hf_hub_download
# hf_token = os.getenv('HF_TOKEN')
# if hf_token:
# 	login(token=hf_token)
# else:
#     print("HF_TOKEN not found in .env\n")


###################
# LOAD EMBEDDINGS #
###################

# Load documents and the embeddings from the FAISS vector store
document_path = "data/textbook"
documents = load_documents_from_directory(document_path)
faiss_store = load_or_create_faiss_vector_store(documents, "pdf_collection", "faiss_indexes")
retriever = get_hybrid_retriever(
	documents = documents,
	vector_store = faiss_store, 
	k = 15
)


###################
# MODEL INFERENCE #
###################

# Get Mistral API Key from the environment variables
api_key = os.getenv("MISTRAL_API_KEY")
def load_llm_api():
	"""
	Load and configure the Mistral AI LLM.
	Returns:
			ChatMistralAI: Configured LLM instance.
	"""
	if not api_key:
		raise ValueError("MISTRAL_API_KEY not found in .env")

	return ChatMistralAI(
		model="open-mistral-7b",
		mistral_api_key=api_key,
		temperature=0.2,
		max_tokens=256,
		top_p=0.4,
	)
# llm =  ChatOllama(model = 'qwen:0.5b')
llm = load_llm_api()


system_prompt = """
	You are an assistant for question-answering tasks.
	Use the following pieces of retrieved context to answer the question. 
	If you don't know the answer, say that you don't know. 
	Give detailed well formatted concise answers
	\n\n
	{context}
"""

prompt = ChatPromptTemplate.from_messages([
	("system", system_prompt),
	("human", "{input}"),
])

def get_answer_with_source(response):
    # Extract the answer
    answer = response.get('answer', 'No answer found.')

    # Handle multiple contexts in the response (assuming response['context'] is a list)
    sources = []
    
    # Iterate over the list of context documents and collect up to 4 sources
    for doc in response['context'][:3]:  # Limit to the top 4 contexts
        source = doc.metadata.get('source', 'Unknown source')
        page = doc.metadata.get('page', 'Unknown page')
        sources.append(f"(Page: {page})")
    
    # Join the top 4 sources with newlines
    sources_info = "\n".join(sources)

    # Format the final answer with the answer and top 4 source information
    final_answer = f"{answer}\n\n{sources_info}"
    
    return final_answer


def chat_completion(question):
	"""
	Generate a response to a given question using the RAG (Retrieval-Augmented Generation) chain.
	Args:
		question (str): The user question to be answered.
	Returns:
		str: The generated answer to the question.
	"""
	question_answer_chain = create_stuff_documents_chain(llm, prompt)
	rag_chain = create_retrieval_chain(retriever, question_answer_chain)
	response = rag_chain.invoke({"input": question})
	print(f"Running prompt: {question}")
	# print(response['context'])

	final_answer = get_answer_with_source(response)
	
	return final_answer