
# Textbook Chatbot 

The Textbook Chatbot project for CSE 6550 is designed to assist with queries related to the textbook."Software Engineering: A Practitioner's Approach." The chatbot serves as an educational tool, helping users by providing information, answering questions, and possibly retrieving content from the textbook.

[Website](https://sec.cse.csusb.edu/team3/) 

[Jupyter notebook](https://sec.cse.csusb.edu/team3/jupyter)

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


## Evaluation Questions

Below is a list of answerable and unanswerable questions related to Software Quality Assurance (SQA).

| **Answerable**                                                     | **Unanswerable**                                                        |
|--------------------------------------------------------------------|-------------------------------------------------------------------------|
| Who is Hironori Washizaki?                                         | How many developers are ideal for any given software project?            |
| What is software quality?                                          | Can all software bugs be prevented with enough testing?                       |
| What is the agile methodology?                                            | What is the exact ROI of refactoring legacy code?                    |
| How does the agile methodology impact software quality?                | How long should code reviews ideally take for maximum effectiveness?            |
| What is software testing process?                              | Is there a universally best way to measure developer productivity?                 |
| What is the purpose of a task network in project scheduling?        | Can software be made 100% secure?       |
| What is a Quality Management System (QMS) in software?             | Is there a way to build a fully self-sustaining human colony on Mars with current technology?          |
| What are some key challenges to ensuring software quality?         | What's the upper limit of computational power for classical computers?              |
| How do risk management and SQA interact in projects?               | How could we fully eliminate all types of noise in wireless communications?     |
| How does testability affect software testing processes?            | Is there a way to completely avoid all cyber threats in interconnected global networks?               |


## Troubleshooting

1. I ran the docker run command but the website gives me `localhost refused to connect` error
   
   This is probably because the application is still being spun up. Wait for a few minutes and try again.
   
2. I'm in light mode and the website is unreadable
   
   On the streamlit homepage, go to settings and select the custom theme
   

## Project Structure

- `.github/workflows/docker-publish.yml`: GitHub Action workflow to automate Docker publishing
- `app.py`: Main entry point for the application
- `data`
	- `default`: Contains textbook PDF and FAISS indexes
		- `textbook` PDF
		- `faiss_indexes`: Pre-built embeddings and metadata for the textbook
- `backend`
	- `document_loading.py`: Document loading, embedding creation and search logic
	- `inference.py`: LLM inference and RAG logic
	- `prompts.py`: Contains the prompt
	- `citations.py`: Logic for getting sources for a response
	- `statistics.py`: Database schema and querying
- `frontend`
	- `styles/`: CSS styling
	- `streamlit.py`: Main streamlit file
	- `pdf.py`: PDF viewer
   - `utils.py`: Contains utility functions such as the confusion matrix
- `jupyter`
	- `main.ipynb`: Jupyter notebook file
- `.env.template`: Template for what a .env file should look like
- `.gitignore`: Files and directories should be ignored by Git
- `Dockerfile`: Instructions to build the Docker image
- `README.md`: Project documentation
- `requirements.txt`: Lists required python dependencies

## Affiliation

Built by `Team 3`

Course: CSE 6550, Fall '24 (Software Engineer Concepts)

Institution: California State University, San Bernardino
