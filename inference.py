import os
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from llama_cpp import Llama
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
from huggingface_hub import login, hf_hub_download
hf_token = os.getenv('HF_TOKEN')
if hf_token:
	login(token=hf_token)
else:
    print("HF_TOKEN not found in .env\n")


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
	k = 5
)


###################
# MODEL INFERENCE #
###################

def load_llm(
	repo_id="TheBloke/Mistral-7B-Instruct-v0.2-GGUF", # Mistral 7B Instruct
	filename="mistral-7b-instruct-v0.2.Q4_K_M.gguf", # 4-Bit Quantized
):
	"""
	Load and configure the LLM from Hugging Face.
	Args:
		repo_id (str): The repository ID on Hugging Face.
		filename (str): The filename of the model to download.
	Returns:
		LlamaCpp: Configured LLM instance.
	"""
	# Download the model from hugging face
	print(f'Loading model: {filename}')
	model_path = hf_hub_download(repo_id=repo_id, filename=filename)
	print(f'Model loaded at {model_path}\n')
	# Set up the callback manager for verbose output
	callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
	return LlamaCpp(
		model_path=model_path, # Path to the downloaded model file
		temperature=0.2, # Controls randomness in output. Lower values make output more deterministic
		callback_manager=callback_manager, # Manages callbacks, e.g., for streaming output
		max_tokens=256, # Maximum number of tokens to generate in the response
		top_p=0.4, # Nucleus sampling: only consider tokens with cumulative probability < top_p
		n_ctx=8000, # Context window size (number of tokens the model can consider)
		verbose=False,  # If True, prints additional information during inference
		repeat_penalty=1.15, # Penalizes repetition in generated text. >1 reduces repetition
	)

llm = load_llm()


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

def chat_completion(question):
	"""
	Generate a response to a given question using the RAG (Retrieval-Augmented Generation) chain.
	Args:
		question (str): The user question to be answered.
	Returns:
		str: The generated answer to the question.
	"""
	print(f"Running prompt: {question}")
	question_answer_chain = create_stuff_documents_chain(llm, prompt)
	rag_chain = create_retrieval_chain(retriever, question_answer_chain)
	response = rag_chain.invoke({"input": question})
	return response['answer']