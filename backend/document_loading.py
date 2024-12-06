import os
import re
import json
import numpy as np
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
	chunk_size: int = 200, 
	chunk_overlap: int = 50
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
	distance_threshold = 400 # Set lower values for stricter filtering
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
	filtered_docs = [[doc, score] for doc, score in retrieved_docs if score <= distance_threshold]
	return filtered_docs

def clean_text(text: str) -> str:
  """Remove any special characters from text"""
  return ''.join(char for char in text if char.isalpha() or char.isspace() or char.isnumeric() or char in '.,!?\'";:()')

def cosine_similarity(v1, v2):
    v1, v2 = np.array(v1), np.array(v2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def get_tag(question: str) -> str:
  """Get the tag for a given question using similarity search"""
  max_similarity = 0.70
  best_match = None
  QUESTIONS = None
  try:
    with open(f"/app/data/swebok/common.json", 'r') as f:
      QUESTIONS = json.load(f)
    query_embedding = EMBEDDING_FUNCTION.embed_documents([question])[0]
    for item in QUESTIONS:
      similarity = cosine_similarity(query_embedding, item["embedding"])
      # print(f'q: {item["question"]}, score: {similarity}')
      if similarity > max_similarity:
        max_similarity = similarity
        best_match = item["tag"]
  except:
    pass
  return best_match

def get_content(tag: str, question: str) -> tuple[str, str]:
  """Get appropriate content based on the tag"""
  CONTENTS = None
  try:
    with open(f"/app/data/swebok/contents.json", 'r') as f:
      CONTENTS = json.load(f)
  except:
    return None, None
 
  if tag == "number": return question, CONTENTS["chapter_count"]
  elif tag == "title": return f"What is the title of this book?", CONTENTS["title"]
  elif tag == "author": return f"Who is the author? {CONTENTS['author']}", CONTENTS["author"]
  elif tag == "summary_chapter":
    # Extract chapter number from question
    chapter_match = re.search(r'chapter\s*0?(\d+)', question.lower())
    if not chapter_match:
      return f"{question} is invalid", "The specified chapter does not exist. Select a chapter from 1 to 18"
    if chapter_match:
      chapter_num = chapter_match.group(1)
      for chapter in CONTENTS["chapters"]:
        if chapter["chapter"] == chapter_num.zfill(2):
          sections = "\n- " + "\n- ".join(chapter["sections"])
          context = f"Chapter {chapter_num}: {chapter['title']}\nSections:{sections}"
          return f"Summarize chapter {chapter_num}: {chapter['title']}", context
      return f"Chapter {chapter_num}", "The specified chapter does not exist in the contents."

  elif tag == "appendix":
      appendices_text = []
      for appendix in CONTENTS["appendices"]:
          appendices_text.append(f"Appendix {appendix['chapter']}: {appendix['title']}")
      return "What are the appendices of SWEBOK?", "\n".join(appendices_text)

  elif tag == "summary_complete":
      chapters_text = []
      for chapter in CONTENTS["chapters"]:
          chapters_text.append(f"Chapter {chapter['chapter']}: {chapter['title']}")
      context = "Software Engineering Body of Knowledge (SWEBOK) summary:\n" + "\n".join(chapters_text)
      return question, context
  
  return None

def match_question(question: str) -> str:
  tag = get_tag(question)
  if tag is not None:
    return get_content(tag, question)
  else:
    return None, None