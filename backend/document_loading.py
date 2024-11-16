import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader

EMBEDDING_MODEL_NAME = "Alibaba-NLP/gte-large-en-v1.5"  # Embedding model (https://huggingface.co/Alibaba-NLP/gte-large-en-v1.5)
model_kwargs = {'trust_remote_code': True}
EMBEDDING_FUNCTION = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME, model_kwargs=model_kwargs)

def load_documents_from_directory(
	document_path: str, 
	chunk_size: int = 2048, 
	chunk_overlap: int = 200
):
	"""
	Load PDF documents from a directory and split them into chunks.
	Args:
		document_path (str): Path to the directory containing PDF files.
		chunk_size (int): Size of each text chunk (default: 2048).
		chunk_overlap (int): Overlap between chunks (default: 200).
	Returns:
		List of document chunks.
	"""
	print(f"Loading documents from {document_path}...")
	# Load PDF documents from the specified directory
	documents = PyPDFDirectoryLoader(document_path).load_and_split()
	# Create a text splitter using tiktoken encoder
	text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
	# Split the documents into chunks
	return text_splitter.split_documents(documents)


def load_or_create_faiss_vector_store(
	documents,
	persist_directory,
	collection_name="collection"
):
	"""
	Load an existing FAISS vector store or create a new one if it doesn't exist.
	Args:
			documents: List of documents to be indexed.
			collection_name (str): Name of the collection.
			persist_directory (str): Directory to save/load the FAISS index.
	Returns:
			FAISS vector store object.
	"""
	index_path = os.path.join(persist_directory, f'{collection_name}')
	if os.path.exists(index_path):
		# Load existing FAISS index
		print(f"Loading existing FAISS vector store from {index_path}...\n")
		faiss_store = FAISS.load_local(
			index_path, 
			embeddings=EMBEDDING_FUNCTION, 
			allow_dangerous_deserialization=True
		)
	else:
		# Create new FAISS index
		print(f"Creating new FAISS vector store in {index_path}...\n")
		faiss_store = FAISS.from_documents(
			documents, 
			embedding=EMBEDDING_FUNCTION
		)
		faiss_store.save_local(index_path)
	return faiss_store

def similarity_search(
	question,
	vector_store,
	k,
	distance_threshold = 340 # Set lower values for stricter filtering
):
	"""
	Get top k most similar documents using FAISS vector store.
	Args:
		question: The user question
		vector_store: FAISS vector store
		k: Number of documents to return
		distance_threshold: Maximum distance score to include document
	Returns:
		list[Document]: Top k most similar documents
	"""
	retrieved_docs = vector_store.similarity_search_with_score(question, k=k)
	filtered_docs = [doc for doc, score in retrieved_docs if score <= distance_threshold]
	# [print(score) for doc, score in retrieved_docs if score <= distance_threshold]
	return filtered_docs

def get_hybrid_retriever(documents, vector_store, k):
	"""
	Create a hybrid retriever combining BM25 and vector search.
	Args:
		documents: List of documents for BM25 retriever.
		vector_store: FAISS vector store for vector retriever.
		k (int): Number of documents to retrieve.
	Returns:
		EnsembleRetriever object combining BM25 and vector search.
	"""
	# Create BM25 retriever
	bm25_retriever = BM25Retriever.from_documents(
		documents, 
		k = 0
	)
	# Create vector retriever
	vector_retriever = vector_store.as_retriever(
		search_type="similarity",
		search_kwargs={
			'k': k,
		}
	)
	# Combine retrievers with specified weights
	fusion_retriever = EnsembleRetriever(
		retrievers=[bm25_retriever, vector_retriever],
		weights=[0.2, 0.8]
	)
	return fusion_retriever