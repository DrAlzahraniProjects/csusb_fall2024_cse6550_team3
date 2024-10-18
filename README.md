# Textbook Chatbot 

The Textbook Chatbot project for CSE 6550 is designed to assist with queries related to the textbook."Software Engineering: A Practitioner's Approach." The chatbot serves as an educational tool, helping users by providing information, answering questions, and possibly retrieving content from the textbook.

## Prerequisites
Before you begin, make sure you have the following installed on your machine:
- **Git**
- **Docker**

## Setup
1. Running from Dockerhub
   
   Pull the repository from DockerHub
   
   Download the repository from    DockerHub latest
  
``` bash
docker pull pavankunchala/team3-app:latest
```

2. Run the Docker container

     Execute the Docker container downloaded from pavankunchala/team3-app

```bash
docker run -p 5003:5003 pavankunchala/team3-app
```
The application will be available at:  http://localhost:5003/team3

## Developer Setup

To get started, first clone the repository to your local machine:
```
git clone https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3.git
```

After cloning the repository, navigate to the project directory:
```
cd csusb_fall2024_cse6550_team3
```

Update Local Repository
```
git pull origin main
```

Create a [Mistral AI token](https://console.mistral.ai/api-keys/). Then create a .env file and add the following (Do not commit this file to git)
```
MISTRAL_API_KEY= = <Mistral AI key>
```

Build the Docker image:
```
docker build -t team3-app .
```

Now, run the Docker container:
```
docker run --env-file .env -p 5003:5003 -v $(pwd):/app team3-app
```

The application will be available at:  http://localhost:5003/team3

<!-- Accessing Jupyter Notebook http://localhost:6003/ -->

---
## Project Structure

- `.github/workflows/docker-publish.yml`: Defines a GitHub Action workflow to automate Docker publishing
- `app.py`: Main entry point for the application
- `data`
	- `default`: Contains textbook PDF and FAISS indexes
		- `textbook` PDF
		- `faiss_indexes`: Contains pre-built embeddings and metadata for the textbook
- `backend`
	- `document_loading.py`: Document loading, embedding creation and search logic
	- `inference.py`: LLM inference and RAG logic
	- `prompts.py`: Contains the prompt
	- `citations.py`: Logic for getting sources for a response
	- `statistics.py`: Database schema and querying
- `frontend`
	- `styles/`: Contains CSS styling for Streamlit
	- `streamlit.py`: Main streamlit file
	- `pdf.py`: PDF viewer
- `jupyter`
	- `Hello_world.ipynb`: Main Jupyter notebook file
- `.env.template`: Template for what a .env file should look like
- `.gitignore`: Specifies which files and directories should be ignored by Git
- `Dockerfile`: Contains instructions to build the Docker image for the project
- `README.md`: Project documentation containing setup instructions and information about the project
- `requirements.txt`: Lists Python package dependencies required for the project

---

## Affiliation

TEAM 3

CSE 6550: Software Engineer Concepts, Fall 24

California State University, San Bernardino
