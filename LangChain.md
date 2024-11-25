## About LangChain

* LangChain is a powerful open-source framework designed to simplify the development of applications that integrate with large language models (LLMs) like OpenAI's GPT, and other similar AI models. It provides tools and abstractions that allow developers to build complex AI-driven applications, especially those involving tasks such as natural language processing, information retrieval, and task automation.

### Key Features of Langchain:

1. **Chain of Thought (CoT) Reasoning:** 

   LangChain emphasizes reasoning and complex workflows, enabling the chaining of different prompts and models. This allows the developer to build 
   sophisticated pipelines where outputs from one model or step can feed into another.

2. **Document Interaction:** 

   LangChain provides built-in tools to handle text-based interaction with documents. It enables developers to create applications that can efficiently 
   search, retrieve, and interact with large datasets or knowledge bases using LLMs.

3. **Integration with External APIs:** 

   LangChain can connect to external APIs and knowledge sources. This means the LLMs can work alongside other tools such as search engines, databases, or 
   custom APIs to fetch real-time data and information.

4. **Memory and Persistence:** 

   LangChain has a memory system that allows applications to remember past interactions. This is particularly useful for chatbots and assistants where 
   continuous context over a conversation is important.

5. **Modularity**: 

   It offers modular components, making it easy to swap models, tools, and data sources. For example, you can switch between different LLMs (like GPT-3, 
   Cohere, etc.) without changing your application’s core logic.

6. **Agents:** 

   One of the standout features of Langchain is its ability to create “agents,” which are LLM-powered applications that take decisions based on external 
   information sources. These agents can run tasks independently, making the system highly interactive and dynamic.

7. **Customizable:** 

   LangChain is designed with flexibility in mind. It can be tailored to specific needs, be it developing a customer support bot, content generation 
   tool, knowledge assistant, or more complex AI-driven workflows.

### Use Cases:

1. **AI-powered Chatbots:** Build chatbots that can handle complex conversations with context and memory.
2. **Automated Research Assistants:** Tools that can search for information, summarize documents, and answer queries.
3. **Task Automation:** Systems that can interact with APIs or databases, execute tasks based on user instructions.
4. **Content Generation:** Applications that create human-like text for blogging, marketing, or educational content.

* By providing high-level abstractions and interfaces, Langchain allows developers to harness the power of LLMs without needing to manage the intricate details of model interactions, memory, and external API connections. This makes it easier to build more intelligent, capable, and context-aware applications.

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Implementation](#Implementation)
4. [Usage](#usage)
5. [Troubleshooting](#troubleshooting)


# Installation

**1. Create the requirements.txt File**

  * To begin, you must create a ```requirements.txt file```, which will list all the necessary Python libraries required for your LangChain project. This 
    file should include LangChain and other dependencies like FAISS and Hugging Face, among others.

  * Create a file called ```requirements.txt``` in your project folder with the following content:

* ```requirements.txt```:
```bash
faiss-cpu
huggingface_hub
ipykernel
jupyter
langchain
langchain-community
langchain-huggingface
langchain-mistralai
pypdf
python-dotenv
roman
streamlit
sentence-transformers
sqlalchemy
tiktoken
```
* These dependencies ensure that LangChain and all the necessary tools (like Hugging Face, FAISS, and others) are installed in your project environment.

![LC 101](https://github.com/user-attachments/assets/da9d19c7-9a29-4878-a489-d8d25da9a0c6)

Fig 1: Dependencies

**2. Copy ```requirements.txt``` into the Docker Container**

* To ensure that the ```requirements.txt``` file is available inside the Docker container, copy it into the container using the following Dockerfile 
  command:

```bash
COPY requirements.txt /app/requirements.txt
```
* This command copies the local ```requirements.txt``` file from your project directory into the /app/ directory inside the Docker container.

**3. Install Python Packages from requirements.txt**

* Once the ```requirements.txt``` file is inside the container, use the following command to install the listed dependencies. We will use Mamba instead 
  of pip because of its faster dependency resolution

```bash
RUN mamba install --yes --file requirements.txt && mamba clean --all -f -y
```
**Explanation:**

* ```mamba install```: Installs the packages listed in requirements.txt using Mamba.

* ```--yes```: Automatically accepts all installation prompts.

* ```--file requirements.txt```: Tells Mamba to install the packages from the requirements.txt file.

* ```mamba clean --all -f -y```: Cleans up unnecessary files, reducing the image size.

**Why Use Mamba Instead of Pip?**

* Mamba is faster than pip for managing environments and dependencies, particularly when dealing with complex scientific libraries (like FAISS or NumPy). 
  It is optimized for faster dependency resolution and is generally more efficient in managing Conda environments..

**Benefits of Mamba:**

* Faster dependency resolution: Mamba can install packages faster than Conda or Pip because it uses a more efficient dependency solver.

* Better for conda environments: Mamba is used for managing conda environments, which are often needed for scientific Python projects.

![LC 103](https://github.com/user-attachments/assets/473a46ce-dfd5-4e09-9464-c1e0b744a83a)

Fig 2: Python packages

![CB 1](https://github.com/user-attachments/assets/783d6dd2-0f93-4de5-a041-f1c080d2361b)

Fig 3: Installation


# Configuration

* Now that the environment is set up, the first step in configuration is to import the necessary libraries for working with LangChain and other modules.

## Import the libraries
```bash
import os
from roman import toRoman
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
```
![CB 14](https://github.com/user-attachments/assets/51a37d36-c597-44cb-a04a-e773b0bffa71)

Fig 4: Importing the libraries

**Explanation:**

* ```import os``` : The ```os``` module in Python provides functions for interacting with the operating system. It allows you to work with directories, files, environment variables, and other OS-level operations.

* ```from roman import toRoman``` : This import is used to convert integers to Roman numerals. The ```roman``` package in Python is typically used for converting between Roman numerals and integers.

* ```from langchain.chains.retrieval import create_retrieval_chain``` :  This import is from the Langchain framework, which is designed for chaining together different components (LLMs, APIs, etc.) for tasks like document retrieval. The ```create_retrieval_chain``` method is used to build chains that retrieve relevant documents based on a query.

* ```from langchain.chains.combine_documents import create_stuff_documents_chain``` : This is another Langchain component that helps in combining documents retrieved in response to a query. The ```create_stuff_documents_chain``` function allows you to aggregate multiple documents (usually from a retrieval chain) into one response.

* ```from langchain_core.prompts import ChatPromptTemplate``` : The ```ChatPromptTemplate``` is a utility from Langchain that simplifies the creation of chat-based prompts for large language models. It allows you to structure and format input for AI-driven chat models.

* ```from langchain_mistralai import ChatMistralAI``` : ```ChatMistralAI``` is likely a module for integrating Mistral AI into Langchain, enabling the use of the Mistral language model for chat or other LLM tasks. Mistral AI is a company that develops advanced language models similar to GPT models from OpenAI.


## Loading and setting up the environment

* Next, load the environment variables using the python-dotenv library. This is crucial for accessing sensitive information like API keys.

![CB 15](https://github.com/user-attachments/assets/cdfb9708-ad4b-4359-9172-5a2db7cb317c)

Fig 5: Import and load environment variables

* The ```override=True``` argument ensures that if any environment variables are already set, they will be replaced with those from the ```.env``` file.

**Explanation:**

* ```from dotenv import load_dotenv``` : This line imports the ```load_dotenv``` function from the ```dotenv``` module, which is part of the python-dotenv library. The load_dotenv function reads key-value pairs from a .env file and loads them as environment variables into your application.

* ```dotenv``` : This package allows you to define environment variables in a ```.env``` file, which you can then easily load into your Python code.

* ```load_dotenv(override=True)``` : The ```load_dotenv()``` function loads environment variables from a ```.env``` file into the system environment. These variables can then be accessed in your Python code using os.getenv().

* ```override=True``` : This argument tells ```load_dotenv()``` to override any existing environment variables with values from the .env file, even if those variables are already set in the system environment.


##  Loading Documents and Creating the FAISS Vector Store

* Documents are loaded from the data/textbook directory.
* The FAISS vector store is created (or loaded if it already exists) to store document embeddings, which allow for efficient similarity searches.
* A hybrid retriever is set up to query these documents. The retriever searches the documents using the FAISS vector store and returns the top 15 documents most relevant to the query.

![CB 16](https://github.com/user-attachments/assets/62ee8704-06f2-462c-884a-f0d88300c977)

Fig 6: Load documents and the embeddings from the FAISS vector store

**Explanation:**

* ```document_path = "data/textbook"``` :  The ```document_path`` is a directory (folder) that contains the documents (such as PDFs, text files, or other formats) that you want to process. In this case, it points to a folder called ```tex
tbook``` inside the ```data``` directory.

* ```documents = load_documents_from_directory(document_path)```:  This line loads all documents from the specified directory into memory using the function ```load_documents_from_directory.```

* ```faiss_store = load_or_create_faiss_vector_store(documents, "pdf_collection", "faiss_indexes")``` : This line either creates a new FAISS vector store or loads an existing one, depending on whether it already exists. A vector store is a data structure used to store vector representations (embeddings) of documents or text for similarity-based retrieval.

* ```retriever = get_hybrid_retriever(documents=documents, vector_store=faiss_store, k=15)``` : This line creates a hybrid retriever, which combines different retrieval methods (e.g., keyword-based search and vector similarity search) to find relevant documents. The retriever will return the top k most relevant documents for a given query.



## Loading the LLM (Mistral AI)

* Retrieves the Mistral API key from the environment and loads the Mistral language model. The model is configured with parameters such as:
* temperature=0.2 (lower temperatures make the model more deterministic),
* max_tokens=256 (limit on the number of tokens generated),
* top_p=0.4 (controls diversity).

![CB 17](https://github.com/user-attachments/assets/be244c52-7b1e-4b4d-87fb-e9663cbd4009)

Fig 7: Get mistral API key from the environment variables

**Explanation:**

* ```api_key = os.getenv("MISTRAL_API_KEY")``` : This line retrieves the value of the environment variable ```MISTRAL_API_KEY``` using the ```os.getenv()``` function from the os module.The environment variable ```MISTRAL_API_KEY``` is expected to store the API key required to authenticate and interact with the Mistral AI service.

* ```def load_llm_api()``` : This defines a function named ```load_llm_api()``` that is responsible for loading and configuring the Mistral AI large language model (LLM). The function checks if the API key is available and then returns an instance of ```ChatMistralAI``` with the necessary configurations.

* ```if not api_key``` : This line checks if ```api_key``` (the environment variable ```MISTRAL_API_KEY```) is either ```None``` or an empty string. If ```api_key``` is not found, it raises an error.

* ```return ChatMistralAI(...)``` : If the api_key is found, the function returns an instance of the ```ChatMistralAI``` class, configured with specific parameters.

* ```model="open-mistral-7b"``` : This specifies the model version that will be used. In this case, the model is ```"open-mistral-7b"```, which likely refers to the 7-billion-parameter version of the Mistral AI language model. This larger model can provide more nuanced and sophisticated language understanding.

* ```mistral_api_key=api_key``` : The ```api_key``` retrieved from the environment variable ```MISTRAL_API_KEY``` is passed here to authenticate the API requests to Mistral AI. Without this key, requests to the Mistral service would be unauthorized.

* ```temperature=0.2``` : Temperature controls the randomness or creativity of the model’s responses.
A low value like ```0.2``` makes the model more deterministic, meaning it will generate more predictable and less random responses. The model will tend to choose more common or “safer” words, reducing variability in the output.

* ```top_p=0.4``` : Top-p sampling (also called nucleus sampling) is a method used to control the diversity of the model’s output.
The model will sample from the smallest set of tokens whose cumulative probability adds up to ```top_p``` (in this case, ```0.4``` or 40%).
A low value like ```0.4``` makes the model focus on the most likely outputs, ensuring more focused and precise responses. Higher values make the model more creative but may result in less coherent outputs.


# Implementation

## Defining the System Prompt

* This prompt tells the language model what its role is and how to respond using the retrieved documents. The placeholder {context} will be filled with the context from the retriever.

![CB 18](https://github.com/user-attachments/assets/120fed4c-b421-4e10-bb17-333b42f2ce24)

Fig 8: System prompt template

**Explanation:**

* ```system_prompt = """``` : This line starts the definition of a multi-line string (in Python, triple quotes ```"""``` allow you to define a string that spans multiple lines).
This string will serve as the system prompt, i.e., the instruction set provided to the model, outlining how it should behave when answering questions.

* ```You are an assistant for question-answering tasks.``` : The first line in the prompt clearly defines the role of the model: "You are an assistant for question-answering tasks."
This statement serves to frame the model's identity and purpose. The model is instructed to act specifically as a helper that provides answers to user questions.

* ```Use the following pieces of retrieved context to answer the question.``` : This instruction tells the model to use the retrieved context (information passed as part of the system’s setup) to form its responses.
"Retrieved context" refers to information gathered from external sources or documents (e.g., from a database, a search engine, or other document retrieval systems) that the assistant can use to provide accurate answers.

* ```If you don't know the answer, say that you don't know.``` : This instruction tells the model to admit uncertainty if it cannot find the answer within the provided context.
Instead of generating a potentially incorrect or misleading answer, the model is instructed to say, "I don't know."

* ```Give detailed well formatted concise answers.``` : The responses should include enough relevant information to fully answer the question.

* ```{context}``` : ```{context}``` is a placeholder within the system prompt. It is used to dynamically insert the retrieved context (the relevant information that was previously fetched) at the time of generating the response.

* ```\n\n``` : The ```\n\n``` in the prompt represents two newlines, which are used to insert a blank line in the output. It separates different parts of the instruction (in this case, separating the instructions from the ```{context}``).


## Creating the Chat Prompt

* This combines the system prompt with a human input prompt. The {input} placeholder will be replaced with the actual user query during execution.

![CB 19](https://github.com/user-attachments/assets/ec7f1c9c-42fe-425a-87de-89107cb54db8)

Fig 9: Create the prompt template

**Explanation:**

* ```prompt = ChatPromptTemplate.from_messages([...])``` : This line creates a chat prompt template by using the ```from_messages()``` method of the ```ChatPromptTemplate``` class.
The ```from_messages()``` method takes in a list of messages (both system and human) that will guide the interaction between the model and the user. These messages are then used to create the final prompt structure.

* ```("system", system_prompt)``` : This tuple specifies a system message. The first element, ```"system"```, tells the model that this message is from the system.
The second element, ```system_prompt```, refers to the system prompt defined earlier, which contains instructions for how the assistant should behave.

* ```("human", "{input}")``` : This tuple specifies a human message, where ```"human"``` indicates that this message is coming from the user (or human).
The second element, ```"{input}"```, is a placeholder that represents the actual question or input that the user will provide during the interaction.
	

## Extracting Answers and Formatting Sources

* The get_answer_with_source function processes the response from the model and extracts the source document information. It does the following:
* Extracts the answer from the model's output.
* Collects the metadata from the retrieved documents, including file names and page numbers.
* Adjusts page numbers to be relative to some base (e.g., 33).
* Formats page numbers as Roman numerals if they are negative.
* Constructs hyperlinks to the source documents.

![CB 20](https://github.com/user-attachments/assets/e58b9814-be26-4f58-9e76-787af9fa621a)

Fig 10: Function to extract answer and source information

**Explanation:**

* ```def get_answer_with_source(response)``` : This defines a function that takes one argument, ```response```, which is a dictionary containing the answer and context (likely from the output of a Retrieval-Augmented Generation chain).

* ```""" ... """``` : This is a docstring that provides a detailed explanation of the function, including its purpose, arguments, and return value.

* ```answer = response.get('answer', 'No answer found.')``` : The function attempts to retrieve the value associated with the ```'answer'``` key from the ```response``` dictionary.If the ```'answer'``` key is not present, the default message 'No answer found.' is returned.

* ```sources = []``` : The function initializes an empty list sources to store the ```source``` information (links to documents and pages).

* Iterating Through Contexts:
 
```bash 
for doc in response['context'][:4]:
```
The function iterates over the first four context documents in ```response['context']```. The ```[:4]``` ensures that no more than four contexts are processed, even if more are available.

* Extracting Source Metadata:

```bash
source = doc.metadata.get('source', 'Unknown source')
file_name = os.path.basename(source)
page = doc.metadata.get('page', 'Unknown page')
```
**Explanation:**

1. ```source```: Extracts the source of the document from the metadata field of the doc. If the 'source' key is missing, it defaults to 'Unknown source'.

2. ```file_name```: Extracts the filename from the full path using os.path.basename(). This will be used in the hyperlink.

3. ```page```: Extracts the page number from the document’s metadata. If the 'page' key is missing, it defaults to 'Unknown page'.

* Adjusting Page Numbers:

```bash
adjusted_page = page - 33
if adjusted_page >= 1:
	link = f'<a href="/team3/?view=pdf&file={file_name}&page={page}" target="_blank">[{adjusted_page}]</a>'
else:
	adjusted_page = toRoman(page)
	link = f'<a href="/team3/?view=pdf&file={file_name}&page={page}" target="_blank">[{adjusted_page}]</a>'
```

**Explanation:**

1. The page number is adjusted by subtracting 33. This might be necessary because, in some documents, there is an offset where the numbering starts from a certain point (e.g., skipping the first few introductory pages).

2. If the adjusted page is greater than or equal to 1, a link is created with the adjusted page number.

3. If the adjusted page is less than 1, the page number is converted to Roman numerals using the toRoman() function (likely for front matter pages like introductions or prefaces, which are often numbered in Roman numerals).

4. Each link is an HTML anchor tag that points to a file and page within the system ("/team3/?view=pdf&file={file_name}&page={page}"). This creates a clickable link that opens the PDF document to the specific page.

* Collecting Source Links:

```bash
sources.append(link)
```
**Explanation:**

1. Each generated source link is appended to the sources list.

*  Formatting Sources Information:

```bash
sources_info = "\nSources: " + "".join(sources)
```
1. Joins the list of source links (sources) into a single string and prepends the string "Sources: " to indicate that these are the references for the answer.

*  ```final_answer = f"{answer}\n\n{sources_info}"``` : Combines the extracted ```answer``` with the ```sources_info``` string into a single formatted string.

* ```return final_answer```: Returns the fully formatted answer with source references.


# Usage

## Completing the Question Answering Process

* The chat_completion function runs the RAG chain:
* It creates a question-answer chain using the create_stuff_documents_chain function.
* It creates a retrieval chain that retrieves relevant documents and uses them to generate an answer.
* It invokes the chain with the user’s input question and formats the final response using get_answer_with_source.

```bash
def chat_completion(question):
    print(f"Running prompt: {question}")
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    response = rag_chain.invoke({"input": question})
    final_answer = get_answer_with_source(response)
    return final_answer
```

![CB 21](https://github.com/user-attachments/assets/54b8ea20-e7a5-4d25-add1-f12326130a75)

Fig 11: Generation of response to a question

**Explanation:**

* ```def chat_completion(question)``` : Defines a function called ```chat_completion``` that accepts a single argument, ```question```. This argument represents the user's question.

* Docstring Explanation:

```bash
"""
Generate a response to a given question using the RAG (Retrieval-Augmented Generation) chain.
Args:
	question (str): The user question to be answered.
Returns:
	str: The generated answer to the question.
"""
```
1. Input: It takes a ```question``` (which is a string).

2. Output: It returns a formatted string with the generated answer.

3. It also mentions that the function utilizes RAG (Retrieval-Augmented Generation), meaning that it involves retrieving relevant documents before generating an answer using a language model.

* ```print(f"Running prompt: {question}")``` : Prints the question to the console for debugging purposes, letting you see which prompt is being processed.

* ```question_answer_chain = create_stuff_documents_chain(llm, prompt)``` : ```llm``` This is the language model (LLM) that will be used for generating the answer.```prompt``` This is the prompt template that defines the structure of the conversation, containing system instructions and placeholders for the user's question.

* ```rag_chain = create_retrieval_chain(retriever, question_answer_chain)``` : Calls ```create_retrieval_chain()``` to build the Retrieval-Augmented Generation (RAG) chain. ```retriever```This is the retrieval mechanism, which is responsible for finding the relevant documents based on the user's question. ```question_answer_chain``` This is the chain created earlier, which will generate answers using the retrieved documents.

* ```response = rag_chain.invoke({"input": question})``` : Invokes the RAG chain by passing a dictionary with the key ```"input"``` and the value being the user's ```question```.
The RAG chain uses this input to retrieve relevant documents and then generate an answer based on those documents.
The result of this invocation is stored in the variable ```response```, which is expected to be a dictionary containing both the answer and the retrieved context documents.

* ```final_answer = get_answer_with_source(response)``` : Calls the function ```get_answer_with_source()``` and passes the response as an argument.
Extract the answer from the ```response``` dictionary.
Extract and format the sources (i.e., the documents and pages where the answer was derived from).
Return a formatted string that contains both the answer and the sources.

* ```return final_answer``` : Returns the ```final_answer``` (a string) as the function’s output. This string contains the generated answer along with references to the sources used to generate that answer.



# Troubleshooting

### 1. Environment Variables Not Loaded Correctly

* One possible issue could be with loading the Mistral API key from the ```.env``` file.

**Potential Problem:**

 * MISTRAL_API_KEY not loaded:

  If the .env file is not properly loaded, the os.getenv("MISTRAL_API_KEY") call will return None, causing the function to raise a ValueError with the 
  message: "MISTRAL_API_KEY not found in .env".  
   
 * Troubleshooting Steps:

  Ensure .env file exists: Make sure that the .env file exists and contains the correct API key, i.e., MISTRAL_API_KEY=<your-api-key>.

  Path issue: Confirm that the .env file is in the correct directory and that the script is executing in the correct working directory.

  Check permissions: Ensure the script has permission to read the .env file.

  Recheck loading: Try printing the API key for debugging
 
```bash
print(f"Loaded API key: {os.getenv('MISTRAL_API_KEY')}")
```
### 2. Document Loading Issues

* The document loading and embedding step might fail if there are issues with file paths or formats.

**Potential Problem:**

  * Document path is invalid:

  The document_path = "data/textbook" might be incorrect or inaccessible.

  * Troubleshooting Steps:

  Path check: Verify that the directory data/textbook exists and is accessible from the script's location.

  File format: Ensure the files in the data/textbook directory are in a supported format for loading and embedding.

```bash
import os
print(os.listdir(document_path))
```

### 3. FAISS Vector Store Loading Errors

* If there’s an issue with loading or creating the FAISS vector store, it may cause the retrieval process to fail.

**Potential Problem:**

  * FAISS Index loading error:  

  The function load_or_create_faiss_vector_store() could fail if it cannot locate or create the FAISS index.
 
  * Troubleshooting Steps:

  Check FAISS Installation: Ensure FAISS is installed correctly on your system.

  Print debug information: Add print statements to verify that the FAISS index is being loaded or created properly.

### 4. Incorrect Retrieval Configuration

* The get_hybrid_retriever function might be misconfigured, causing poor document retrieval.

**Potential Problem:**

  * Retriever misconfiguration:

  If the number of k results (here 15) is too large or too small, or the retriever is not configured correctly, the retrieval process might fail or 
  return irrelevant results.

  * Troubleshooting Steps:

  Test different values for k: Start with smaller or larger values for k to see if retrieval improves.

  Check retrieval behavior: Print out the documents retrieved by the retriever:

```bash
retrieved_docs = retriever.get_relevant_documents(question)
print(f"Retrieved {len(retrieved_docs)} documents for the question.")
```
### 5. Prompt and Model Issues

* There could be issues with how the prompt is structured or how the model is being invoked.

### 6. Error in Response Handling and Source Extraction

* The function ```get_answer_with_source()``` may not handle the response correctly, particularly if the context is missing or misformatted.

### 7. General Error Logging

* To capture any unexpected errors that may occur in the workflow, you can add a try-except block around critical sections.







