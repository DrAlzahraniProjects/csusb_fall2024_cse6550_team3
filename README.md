
# Textbook Chatbot 

The Textbook Chatbot project for CSE 6550 is designed to assist with queries related to the textbook."Software Engineering: A Practitioner's Approach." The chatbot serves as an educational tool, helping users by providing information, answering questions, and possibly retrieving content from the textbook.

## Prerequisites
Before you begin, make sure you have the following installed on your machine:
- **Git**
- **Docker**

## Setup

1. To get started, first clone the repository to your local machine:
   ```
   git clone https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3.git
   ```

2. After cloning the repository, navigate to the project directory:
   ```
   cd csusb_fall2024_cse6550_team3
   ```

3. Update Local Repository
   ```
   git pull origin main
   ```

4. Preliminary steps: make sure to execute all three steps given below to delete previous image

   To see all the running containers in your machine: 
   ```
    docker ps
   ```
  
   To stop a running container, replace <container_id> with the one found in docker ps
   ```
   docker stop <container_id>
   ```

   To remove/delete a docker container, replace <container_id> with the one found in docker ps
   ```
   docker rm <container_id>
   ```

5. Build the Docker image using the following command:

   Befere running this command include API key in the end 

   Go to [team3](https://csusb.instructure.com/courses/43192/discussion_topics/419698) in canvas for API key
   
   ```
   docker build -t team3-app . --build-arg MISTRAL=
   ```
6. Now, run the Docker container:
 
   ```
   docker run -d -p 5003:5003 -p 6003:6003 team3-app
   ```

7. Allow upto 5 minutes before accessing the application
    
   The application will be avilable at
  
    Website: [http://localhost:5003/team3](http://localhost:5003/team3)
   
    Jupyter: [http://localhost:6003/team3/jupyter](http://localhost:6003/team3/jupyter)

---

## Evaluation Questions

1. Answerable questions

   ```
   Who is Hironori Washizaki?
   ```
   ```
   What is software quality?
   ```
   ```
   What is agile approach?
   ```
   ```
   How does the Agile approach impact software quality?
   ```
   ```
   What is software testing process?
   ```
   ```
   What is ROI?
   ```
   ```
   What is a Quality Management System (QMS) in software?
   ```
   ```
   What are some key challenges to ensuring software quality?
   ```
   ```
   How do risk management and SQA interact in projects?
   ```
   ```
   How does testability affect software testing processes?
   ```

2. Unanswerable questions
   
   ```
   How many defects will occur in a specific software project?
   ```
   ```
   What is the cost of nonconformance for a project?
   ```
   ```
   How will a new process affect software defect rates?
   ```
   ```
   What is the probability of a defect reoccurring in software?
   ```
   ```
   How long will it take to resolve defects from an audit?
   ```
   ```
   What level of software quality is `good enough` for stakeholders?
   ```
   ```
   What is the future impact of AI on software quality standards?
   ```
   ```
   What ROI will be achieved through additional SQA measures?
   ```
   ```
   What specific changes improve software quality across all projects?
   ```
   ```
   How many resources are needed to achieve a quality level?
   ```
   
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
