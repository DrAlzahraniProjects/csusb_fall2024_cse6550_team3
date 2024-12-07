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
	Purpose: Load and split PDF documents from a directory into manageable chunks
	Input:
		- document_path: Path to directory containing PDF files
		- chunk_size: Size of each text chunk
		- chunk_overlap: Number of characters to overlap between chunks
	Output: List of document chunks, where each chunk is a Document object
	Processing:
		1. Loads all PDF files from specified directory
		2. Creates text splitter with tiktoken encoder
		3. Splits documents into overlapping chunks
	"""
	print(f"Loading documents from {document_path}...")
	# Load PDF documents from the specified directory
	documents = PyPDFDirectoryLoader(document_path).load_and_split()
	# Create a text splitter using tiktoken encoder
	text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
	# Split the documents into chunks
	return text_splitter.split_documents(documents)


def load_or_create_faiss_vector_store(
	documents: list,
	persist_directory: str,
	collection_name: str = "collection"
) -> FAISS:
	"""
	Purpose: Create or load a FAISS vector store for document embeddings
	Input:
		- documents: List of document chunks to be indexed
		- persist_directory: Directory path to save/load the FAISS index
		- collection_name: Name of the vector store collection
	Output: FAISS vector store object containing document embeddings
	Processing:
		1. Checks if index exists at specified path
		2. If exists: loads existing index
		3. If not: creates new index from documents and saves it
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
	question: str,
	vector_store: FAISS,
	k: int,
	distance_threshold: float = 400
):
	"""
	Purpose: Find most similar documents to a given question
	Input:
		- question: User query string
		- vector_store: FAISS vector store containing document embeddings
		- k: Number of similar documents to retrieve
		- distance_threshold: Maximum distance score to include document
	Output: List of tuples containing (Document, similarity_score)
	Processing:
		1. Performs similarity search using vector store
		2. Filters results based on distance threshold
		3. Returns filtered documents with their scores
	"""
	retrieved_docs = vector_store.similarity_search_with_score(question, k=k)
	filtered_docs = [[doc, score] for doc, score in retrieved_docs if score <= distance_threshold]
	return filtered_docs

def clean_text(text: str) -> str:
	"""
	Purpose: Clean text by removing unwanted special characters
	Input: text: String to be cleaned
	Output: Cleaned string containing only alphanumeric chars and basic punctuation
	Processing: Filters string to keep only allowed characters
	"""
	return ''.join(char for char in text if char.isalpha() or char.isspace() or char.isnumeric() or char in '.,!?\'";:()')

def cosine_similarity(v1: list, v2: list) -> float:
	"""
	Purpose: Calculate cosine similarity between two vectors
	Input: v1: First vector, v2: Second vector
	Output: Cosine similarity score between 0 and 1
	Processing:
		1. Converts inputs to numpy arrays
		2. Calculates dot product and magnitudes
		3. Returns normalized similarity score
	"""
	v1, v2 = np.array(v1), np.array(v2)
	return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def get_tag(question: str) -> str:
  """
	Purpose: Find the most similar predefined tag for a given question
	Input: question: User query string
	Output: Matching tag string or None if no match found
	Processing:
		1. Loads predefined questions from JSON
		2. Embeds input question
		3. Calculates similarity with stored questions
		4. Returns tag of best match above threshold
  """
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
  """
	Purpose: Retrieve appropriate content based on question tag
	Input:
		- tag: Question category tag
		- question: Original user question
	Output:
		- Tuple of (processed_question, content)
		- Both elements can be None if no matching content found
	Processing:
		1. Loads content from JSON file
		2. Matches tag to specific content type
		3. Processes content based on tag type
		4. Returns formatted question and relevant content
	"""
  CONTENTS = None
  try:
    with open(f"/app/data/swebok/contents.json", 'r') as f:
      CONTENTS = json.load(f)
  except:
    return None, None
	
  if tag == "number": return question, CONTENTS["chapter_count"]
  elif tag == "title": return f"What is the title of this book? SWEBOK", CONTENTS["title"]
  elif tag == "author": return f"Who is the author? {CONTENTS['author']}", CONTENTS["author"]
  elif tag in ["chapter_title", "summary_chapter"]:
    # Try to match numeric chapter
    chapter_match = re.search(r'chapter\s*0?(\d+)', question.lower())
    chapter_num = None
    if chapter_match:
      chapter_num = chapter_match.group(1)
    else:
      # Try to match word-based chapter
      for chapter in CONTENTS["chapters"]:
        word_pattern = rf"\b{chapter['chapter_number_text']}\b"
        if re.search(word_pattern, question.lower()):
          chapter_num = chapter["chapter"]
          break
    if not chapter_num:
      return f"{question} is invalid", "The specified chapter does not exist. Select a chapter from 1 to 18"

    for chapter in CONTENTS["chapters"]:
      if chapter["chapter"] == chapter_num.zfill(2):
        if tag == "chapter_title":
          context = f"{chapter['title']}"
          return f"{question} {chapter['title']}", context
        else:  # summary_chapter
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
  """
	Purpose: Match user question to appropriate content
	Input:
		- question: User query string
	Output:
		- Tuple of (processed_question, content)
		- Both elements can be None if no match found
	Processing:
		1. Gets tag for question
		2. If tag found, retrieves corresponding content
		3. Returns None, None if no match
	"""
  tag = get_tag(question)
  if tag is not None:
    return get_content(tag, question)
  else:
    return None, None