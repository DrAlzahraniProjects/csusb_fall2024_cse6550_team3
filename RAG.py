import os
from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_milvus import Milvus
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from pymilvus import connections, utility
import pdfplumber
from langchain.schema import Document  # Import the Document class
from langchain.chains import create_retrieval_chain  # Import this function

load_dotenv()
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")

MILVUS_URI = './milvus/milvus_vector.db'
MODEL_NAME = "sentence-transformers/all-MiniLM-L12-v2"
PDF_PATH = "data/Textbook.pdf"  # Path to your PDF file

class RAG:
    def __init__(self, pdf_path=PDF_PATH, milvus_uri=MILVUS_URI):
        self.pdf_path = pdf_path
        self.milvus_uri = milvus_uri
        self.embedding_function = self.get_embedding_function()
        self.vector_store = self.load_existing_db()

        # Force initialization if no existing vector store is found
        if self.vector_store is None:
            print("No existing Vector Store found. Initializing the vector store...")
            self.vector_store = self.initialize_milvus()

    def get_embedding_function(self):
        """Returns the embedding function for the model."""
        return HuggingFaceEmbeddings(model_name=MODEL_NAME)

    def query(self, query_text):
        """Generate an answer for the given query."""
        model = ChatMistralAI(model='open-mistral-7b')
        prompt = self.create_prompt()
        retriever = self.vector_store.as_retriever()
        document_chain = create_stuff_documents_chain(model, prompt)
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        response = retrieval_chain.invoke({"input": f"{query_text}"})
        return response["answer"]

    def create_prompt(self):
        """Create a prompt template for the RAG model."""
        PROMPT_TEMPLATE = """
        Human: You are an AI assistant, providing answers using fact-based and statistical information.
        Use the information in <context> to answer the question in <question>.
        If you don't know the answer, say that you don't know.
        <context>
        {context}
        </context>
        <question>
        {input}
        </question>
        Assistant:"""
        return PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["context", "question"])

    def initialize_milvus(self):
        """Initialize the vector store."""
        embeddings = self.get_embedding_function()
        documents = self.load_documents_from_pdf()
        if not documents:
            print("No documents loaded from the PDF.")
            return None
        docs = self.split_documents(documents)
        return self.create_vector_store(docs, embeddings)

    def load_documents_from_pdf(self):
        """Load documents from the specified PDF file."""
        text = ""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    
        if not text:
            print(f"No text extracted from {self.pdf_path}")
            return []
        
        # Return a list of Document objects
        return [Document(page_content=text, metadata={"source": self.pdf_path})]

    def split_documents(self, documents):
        """Split the documents into chunks."""
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300, is_separator_regex=False)
        return text_splitter.split_documents(documents)

    def create_vector_store(self, docs, embeddings):
        """Create a Milvus vector store."""
        # Ensure the directory for the Milvus database exists
        head = os.path.split(self.milvus_uri)[0]
        if not os.path.exists(head):
            os.makedirs(head, exist_ok=True)
            print(f"Created directory for Milvus at {head}")

        # Connect to the Milvus database
        try:
            connections.connect("default", uri=self.milvus_uri)
        except Exception as e:
            print(f"Failed to connect to Milvus: {e}")
            return None

        # Check if the collection already exists
        if utility.has_collection("Textbook_Chatbot"):
            print("Collection already exists. Loading existing Vector Store.")
            return Milvus(
                collection_name="Textbook_Chatbot",
                embedding_function=embeddings,
                connection_args={"uri": self.milvus_uri}
            )

        # Create a new vector store and drop any existing one
        vector_store = Milvus.from_documents(
            documents=docs,
            embedding=embeddings,
            collection_name="Textbook_Chatbot",
            connection_args={"uri": self.milvus_uri},
            drop_old=True,
        )
        print("Vector Store Created")
        return vector_store

    def load_existing_db(self):
        """Load an existing vector store from the local Milvus database."""
        # Check if the Milvus directory exists
        head = os.path.split(self.milvus_uri)[0]
        if not os.path.exists(head):
            print(f"Milvus directory does not exist: {head}")
            return None

        # Connect to the Milvus database
        try:
            connections.connect("default", uri=self.milvus_uri)
        except Exception as e:
            print(f"Failed to connect to Milvus: {e}")
            return None

        # Check if the collection exists
        if utility.has_collection("Textbook_Chatbot"):
            print("Loading existing Vector Store from Milvus.")
            return Milvus(
                collection_name="Textbook_Chatbot",
                embedding_function=self.embedding_function,
                connection_args={"uri": self.milvus_uri}
            )
        print("No existing Vector Store found.")
        return None

if __name__ == '__main__':
    # Example usage
    rag = RAG()
    print("RAG instance created")
