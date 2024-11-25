# FAISS (Facebook AI Similarity Search)

FAISS (Facebook AI Similarity Search) is an open-source library developed by Facebook AI Research. It is a powerful tool for efficient similarity search and clustering of dense vectors. FAISS is extensively used in applications like image recognition, natural language processing (NLP), recommendation engines, and other AI-driven systems that require fast similarity search on large-scale, high-dimensional data.

The main advantage of FAISS is that it is highly optimized for both exact and approximate nearest neighbor searches and offers superior performance, especially when dealing with large datasets. FAISS also takes full advantage of modern hardware, offering implementations that can scale across multi-core CPUs and GPUs, making it a popular choice for AI applications that require fast and scalable retrieval of high-dimensional vectors.

Real-world use cases for FAISS are vast. In recommendation engines, for example, FAISS can help users find similar products or content based on previously interacted items. In image recognition, FAISS enables quick retrieval of similar images from vast datasets, a task commonly needed for content moderation, object detection, or even medical imaging analysis. The library’s efficiency in handling large-scale vector searches makes it the go-to solution for industries that work with significant amounts of data.

This guide will provide a comprehensive overview of FAISS, from installation and configuration to implementation and usage. It also includes troubleshooting steps, ensuring that even if you run into issues, you can resolve them efficiently. You will also learn how to integrate FAISS into a Dockerized environment for consistency across different systems and setups.

By the end of this guide, you will have a thorough understanding of how to use FAISS to handle vector-based retrieval tasks efficiently in your AI-powered applications.

---

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Implementation](#implementation)
4. [Usage](#usage)
5. [Troubleshooting](#troubleshooting)

---

## Installation

FAISS can be installed using docker, with separate versions for CPU and GPU-based systems. GPU installations are particularly beneficial for large datasets, where computational speed becomes critical. In this section, we will cover the installation steps for both CPU and GPU versions of FAISS.

---

### Step 1: Install FAISS
In a Docker-based environment, FAISS can be installed automatically by including it in the `requirements.txt` file. This ensures consistent installations across various environments.

This is how FAISS should be added to the `requirements.txt` file:

```
faiss-cpu==1.7.1
# or
faiss-gpu==1.7.1
```

![2](https://github.com/user-attachments/assets/8f431b5f-2e53-4d6e-87b3-d2bb4cff690e)

**Image 1: Adding FAISS to the Requirements**  
The image above illustrates the addition of FAISS to a `requirements.txt` file. This file is commonly used in Python projects to manage dependencies. Including FAISS in this file ensures that every time the project is deployed in a new environment (for example, in Docker or on another developer's machine), FAISS will be automatically installed along with the other required libraries. This is an essential step for maintaining consistency across development, testing, and production environments, ensuring that the application behaves the same way in all scenarios.

You can then build your Docker image as usual:

```bash
docker build -t faiss_app .
```

![3](https://github.com/user-attachments/assets/8b9f0147-d1f3-4c42-ad45-f379f1a9e667)

**Image 2: Installing FAISS via Docker**  
The image above shows the FAISS installation process within a Docker environment. Docker is a tool that allows developers to package applications and their dependencies into lightweight containers. By including FAISS in a Dockerfile or requirements file, it ensures that the FAISS library, along with all of its dependencies, will be installed in the Docker container. This allows for a consistent setup across different machines, which is especially useful in collaborative projects or when deploying the application to cloud platforms like AWS, Google Cloud, or Azure.
## Docker Installation
To ensure consistent installations across various environments, include FAISS in your requirements.txt file. This enables Docker to automatically install FAISS along with other dependencies.

* Add FAISS to requirements.txt:
```bash
faiss-cpu==1.7.1
# or
faiss-gpu==1.7.1

```
* Build Docker Image:
```bash
docker build -t faiss_app .

```
## Local Installation
For users installing locally without Docker, use the following command based on your setup:
```
* Build Docker Image:
```bash
pip install faiss-cpu
# or
pip install faiss-gpu


```
---

## Configuration

Once FAISS is installed, it is essential to configure your environment for optimal usage. One of the most common configurations is setting up the directory structure for storing FAISS indexes, as it allows you to save, load, and reuse indexes as needed. This is especially useful when working with large datasets that would take too long to re-index every time the program is restarted.

---

### Step 1: Directory Setup for FAISS Indexes

To manage FAISS indexes effectively, create a dedicated directory for storing them. This approach prevents re-indexing for each restart, saving both time and computational resources.

* Create Directory Structure:

```python
import os

directory_path = "faiss_indexes"
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

index_path = os.path.join(directory_path, "my_faiss_index.index")
print("Directory setup complete.")

```
This setup ensures easy retrieval, update, and management of FAISS indexes, particularly beneficial when multiple indexes are required across various datasets.

![4](https://github.com/user-attachments/assets/a0269b94-0cf3-45db-a71c-1e521506f6cf)

**Image 3: Setting up Directory for FAISS Indexes**  
In the image above, we can see the process of creating a dedicated directory for storing FAISS indexes. Having a well-structured directory system is essential when working with FAISS, especially in production environments where multiple indexes might be used. By saving indexes to a specific directory, you can easily retrieve, update, and manage multiple FAISS indexes across various datasets. This also facilitates efficient reloading of pre-built indexes without the need to rebuild them from scratch, saving time and computational resources, particularly for large-scale datasets.

---

## Implementation

### Actual Project Implementation

Here’s a function that efficiently manages FAISS indexes by loading an existing index or creating a new one if it doesn’t exist:  
```
def load_or_create_faiss_vector_store(
    documents,
    persist_directory,
    collection_name="collection"
):
    index_path = os.path.join(persist_directory, f'{collection_name}')
    if os.path.exists(index_path):
        print(f"Loading existing FAISS vector store from {index_path}...\n")
        faiss_store = FAISS.load_local(index_path, embeddings=EMBEDDING_FUNCTION, allow_dangerous_deserialization=True)
    else:
        print(f"Creating new FAISS vector store in {index_path}...\n")
        faiss_store = FAISS.from_documents(documents, embedding=EMBEDDING_FUNCTION)
        faiss_store.save_local(index_path)
    return faiss_store

```
* **Explanation:** This function saves time and resources by reusing existing indexes. It accepts document lists, a directory path, and a collection name for seamless FAISS index management.


![n1](https://github.com/user-attachments/assets/40e4a2e0-a327-4552-b5a7-c1dd45cdea69)
![111](https://github.com/user-attachments/assets/f03650ef-eb8d-4354-9947-98098cb74bce)

**Image 4: Showing how we implemented in our Project**

This image shows the `load_or_create_faiss_vector_store` function, which manages FAISS indexes by either loading an existing index from disk or creating a new one if it doesn't exist. This function saves time by reusing previously saved indexes, enhancing efficiency in projects requiring repeated similarity searches. It takes a list of documents, a directory path, and a collection name to handle the FAISS index storage and retrieval process seamlessly.

## Generalized version for implementing Faiss
 
FAISS provides a variety of index types suited for different use cases. The most basic index type is `IndexFlatL2`, which uses Euclidean distance (L2) for similarity search. FAISS also offers more advanced index types, such as Inverted File (IVF) indexes and Hierarchical Navigable Small World (HNSW) indexes, which provide approximate nearest neighbor searches and are more suitable for very large datasets that prioritize speed over absolute accuracy.

Let’s start by looking at some simple implementations of FAISS, followed by more complex use cases.

--- 

### Example 1: Creating and Adding Data to a FAISS Index

Below is a basic example of how to create an index using FAISS and add random vectors to it:

```python
import numpy as np
import faiss

# Define the dimensionality of the vectors
dimension = 128  # Example dimensionality

# Create a FAISS index with L2 (Euclidean) distance
index = faiss.IndexFlatL2(dimension)

# Generate some random data and add it to the index
num_vectors = 1000
vectors = np.random.random((num_vectors, dimension)).astype('float32')
index.add(vectors)

print("FAISS index created and data added.")
```

![5](https://github.com/user-attachments/assets/3a68860e-a46d-4b1c-945e-a0f8b169261e)

**Image 5: Creating and Adding Data to a FAISS Index**  
In the above example, we create a FAISS index that uses the Euclidean distance metric to measure the similarity between vectors. The process involves first specifying the dimensionality of the vectors (in this case, 128) and then adding 1000 randomly generated vectors to the index. This is one of the most basic ways to use FAISS, but it highlights the simplicity and power of the library for high-dimensional vector storage and search. The FAISS library ensures efficient vector indexing and retrieval, even when the dataset grows in size.

---

### Example 2: Saving and Loading the FAISS Index

Once an index has been created and data has been added, it is useful to save the index to disk for later use. This prevents you from having to rebuild the index each time your program starts.

Here’s how you can save and load a FAISS index:

```python
import os
import faiss

# Define the directory path for index storage
directory_path = "faiss_indexes"
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

# Save the index
index_path = os.path.join(directory_path, "my_faiss_index.index")
faiss.write

_index(index, index_path)
print(f"FAISS index saved to {index_path}.")

# Load the FAISS index from the file
loaded_index = faiss.read_index(index_path)
print(f"FAISS index loaded from {index_path}.")
```

![6](https://github.com/user-attachments/assets/9cb69812-7cb8-4921-9fd7-936a889843d0)

**Image 6: Saving and Loading a FAISS Index**  
This image demonstrates the process of saving and loading a FAISS index. When working with large datasets, rebuilding indexes each time the program is restarted can be computationally expensive. By saving an index to disk after it has been built, you can reload it in subsequent sessions, significantly reducing the time and computational resources needed for large-scale data operations. This is particularly beneficial in production environments where multiple indexing processes might be running concurrently, and speed is critical.

---

## Usage

### Actual Usage in Our Project:
```
########################
# LOAD EMBEDDINGS #
########################

# Load documents and the embeddings from the FAISS vector store
document_path = os.getenv("CORPUS_SOURCE")
persist_directory = os.path.join(document_path, "faiss_indexes")

top_k = 15  # Number of relevant documents to be returned
documents = load_documents_from_directory(document_path)
faiss_store = load_or_create_faiss_vector_store(documents, persist_directory)
retriever = get_hybrid_retriever(documents, faiss_store, top_k)

```
![n2](https://github.com/user-attachments/assets/838ddf80-f907-453e-8596-9ba97325f36d)
**Image 7: Actual Usage in our Project** 

Here loading of documents and embeddings from a FAISS vector store takes place. It sets up the `document_path` and `persist_directory` for indexing, then calls `load_or_create_faiss_vector_store` to load an existing FAISS index or create a new one if needed. The `top_k` parameter defines the number of relevant documents to retrieve. Finally, `get_hybrid_retriever` is used to enable hybrid retrieval with FAISS, returning the top `k` similar documents. 

This setup is essential for efficiently querying and retrieving relevant documents in our projects utilizing FAISS for vector similarity search. 

### General Usage
FAISS supports both exact and approximate nearest neighbor searches. In this section, we’ll explore how to use FAISS to perform similarity searches and how to add more data to an existing index.

---

### Example 1: Performing a Similarity Search

To perform a similarity search, you need to pass a query vector to the FAISS index. The index will then return the nearest neighbors based on the distance metric (in this case, Euclidean distance).

```python
import numpy as np
import faiss

# Create the FAISS index and add data as before
dimension = 128
index = faiss.IndexFlatL2(dimension)

# Generate random data and add it to the index
num_vectors = 1000
vectors = np.random.random((num_vectors, dimension)).astype('float32')
index.add(vectors)

# Define query data (e.g., one random vector)
query_vector = np.random.random((1, dimension)).astype('float32')

# Perform a search for the top 5 similar vectors
k = 5
distances, indices = index.search(query_vector, k)

# Display search results
print("Top 5 results (indices):", indices)
print("Top 5 distances:", distances)
```

![7](https://github.com/user-attachments/assets/ad6dcf1a-6dab-48b8-af9e-4f6831e84da2)

**Image 8: Performing a Similarity Search**  
The above image shows how to perform a similarity search using FAISS. In this example, the index is queried with a single vector, and FAISS returns the top 5 nearest neighbors from the index based on Euclidean distance. FAISS is designed to handle such queries efficiently, even when dealing with very large datasets. In real-world applications, this type of search is often used in recommendation systems or search engines, where you need to find the most similar items (e.g., products, documents, or images) to a given query.

---

### Example 2: Adding More Data to the Index

FAISS allows you to add more vectors to an existing index, which can be helpful as your dataset grows. Below is an example of how to add additional vectors to an index:

```python
import numpy as np
import faiss

# Create the FAISS index as before
dimension = 128
index = faiss.IndexFlatL2(dimension)

# Generate and add initial data
num_vectors = 1000
vectors = np.random.random((num_vectors, dimension)).astype('float32')
index.add(vectors)

# Add more vectors to the index
new_vectors = np.random.random((500, dimension)).astype('float32')
index.add(new_vectors)

print("More data added to the index.")
```

![8](https://github.com/user-attachments/assets/7a579115-bf52-4311-9e7d-a01a78f73493)

**Image 9: Adding More Data to the FAISS Index**  
This image illustrates the process of adding more vectors to an existing FAISS index. FAISS makes it easy to incrementally update an index as new data becomes available. This capability is particularly useful in dynamic applications where new data is constantly being generated, such as in real-time recommendation systems or dynamic search engines. The ability to add data without needing to rebuild the index from scratch ensures that FAISS remains performant, even as datasets grow over time.

---

## Troubleshooting

Even though FAISS is highly optimized, you may encounter issues during installation or configuration. This section covers common issues and how to resolve them.

---

### Common Issues and Solutions

- **Directory Not Found**  
If you encounter a Directory Not Found error when saving an index, ensure the directory exists:

    ```python
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    ```

![9](https://github.com/user-attachments/assets/209a50bb-df6c-4616-aa1e-49fe876e477c)

**Image 10: Handling Directory Not Found Errors**  
In this image, we see a solution to the common error where the directory for saving the FAISS index does not exist. By using the `os.makedirs()` function, we ensure that the directory is created if it doesn’t already exist, preventing errors during the index saving process. This simple check can save significant time when working with large-scale applications where multiple directories and indexes are being handled simultaneously.

- **Dimension Mismatch**  
  All vectors added to the FAISS index must match its dimensionality. For instance, if the index was created with dimension=128, only vectors with 128 dimensions can be added.

**Import Errors**
If you experience import errors, ensure FAISS and dependencies like NumPy are installed:
    ```bash
    pip install faiss-cpu numpy

    ```
- **Import Errors**  
  If you run into import errors while using FAISS, ensure that all required dependencies are installed. For example, you may need to install FAISS and NumPy:

    ```bash
    pip install faiss-cpu numpy
    ```

![10](https://github.com/user-attachments/assets/8dc72373-7c44-47d2-bb13-5e8a75a392c8)

**Image 11: Handling Import Errors**  
The image above depicts the solution to import errors that may occur when FAISS is not installed properly. Ensuring that both FAISS and its dependencies, like NumPy, are correctly installed will help you avoid these errors. Using pip to install the required packages ensures that all dependencies are met, and the environment is properly set up for using FAISS without interruptions.

---

### Debugging Tips

Use print statements to output key variables, such as directory paths and search results, to help locate issues:

Additional Tip: Implementing try-except blocks around critical FAISS operations can provide further debugging information without interrupting your workflow.
- **Check the Total Number of Vectors**  
  You can check how many vectors are stored in the index by printing the `ntotal` property:

    ```python
    print("Number of vectors in the index:", index.ntotal)
    ```

![11](https://github.com/user-attachments/assets/b66ad461-3454-44c1-a88a-43bfc9fb2960)

**Image 12: Checking the Total Number of Vectors in the Index**  
In this image, we see an example of how to check the total number of vectors stored in the FAISS index. This is an important debugging tool when working with large datasets, as it allows you to verify that the correct number of vectors have been added to the index. Printing the `ntotal` property of the index can help you confirm that the index is properly populated and ready for similarity searches.

- **Use Print Statements**  
  Print important variables such as directory paths, index configurations, and search results for debugging purposes:

    ```python
    print("Directory path:", directory_path)
    print("Index path:", index_path)
    print("FAISS index configuration:", index)
    ```

![12](https://github.com/user-attachments/assets/fef4aa08-ec7a-4c8d-8c49-e9da4190386b)

**Image 13: Using Print Statements for Debugging**  
The above image illustrates the use of print statements for debugging purposes. Printing key variables such as directory paths and index configurations can help identify the root cause of issues that may arise during FAISS usage. By examining the output of these print statements, you can quickly determine if there are problems with file paths, index loading, or search results, and take appropriate steps to resolve them.

---

By following the steps in this guide, you should now have a solid understanding of how to install, configure, and use FAISS for vector-based similarity searches. FAISS is an essential tool for building AI applications that require fast and accurate nearest neighbor searches, whether in recommendation systems, search engines, or NLP-based tasks.

With its ability to handle vast amounts of high-dimensional data, FAISS plays a crucial role in advancing the efficiency of modern AI systems. It is particularly valuable for large-scale machine learning and data science applications where vector search needs to be both fast and scalable. Whether in e-commerce recommendation systems, facial recognition technologies, or semantic search engines, FAISS provides a robust and scalable solution for vector similarity search and retrieval.
