from  langchain_community.chat_models.ollama import ChatOllama
from document_loading import load_documents_from_directory, load_or_create_faiss_vector_store , get_hybrid_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
import os
from langchain_core.prompts import ChatPromptTemplate

MODEL_NAME = "mistral"
document_path = "data"

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Give detailed well formatted answers "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)



def setup_llm(model_name=MODEL_NAME):
    print(f"Setting up LLM with model name: {model_name}")
    return ChatOllama(model=model_name, temperature=0.2)









# Load documents and create or load the FAISS vector store
documents = load_documents_from_directory(document_path)
faiss_store = load_or_create_faiss_vector_store(documents, "pdf_collection", "faiss_indexes")





# Initialize the chat model with the FAISS store and retrievers
# chat_model = ChatOllama(model_name=MODEL_NAME, faiss_store=faiss_store, retrievers=[BM25Retriever(), EnsembleRetriever()])
def answer_user_question(question ):
    llm = setup_llm()

    retriever = get_hybrid_retriever(documents= documents,vector_store=faiss_store, k = 10)

    # relevant_docs = retriever

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    response = rag_chain.invoke({"input": question})

    return response['answer']


user_question = input("user question")


response = answer_user_question(user_question)

# Save the response to a text file for display in Streamlit
output_file = "./data/output.txt"
with open(output_file, "w") as file:
    file.write(response)

print(f"Response saved to {output_file} for display in Streamlit.")
