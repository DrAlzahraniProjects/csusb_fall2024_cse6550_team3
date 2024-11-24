# Textbook Chatbot

The Textbook Chatbot project for CSE 6550 is designed to assist with queries related to the textbook, "Software Engineering: A Practitioner's Approach." The chatbot serves as an educational tool, helping users by providing information, answering questions, and possibly retrieving content from the textbook.

[Website](https://sec.cse.csusb.edu/team3/)

[Jupyter notebook](https://sec.cse.csusb.edu/team3/jupyter)

## Prerequisites

Before you begin, make sure you have the following installed on your machine:
- **Git**
- **Docker**
- **Python 3.10 or later**

To verify your Python version, run the following command:
```sh
python --version
```
Ensure that the output shows Python 3.10 or later.

## Setup

1. To get started, first clone the repository to your local machine:
   ```
   git clone https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3.git
   ```

2. After cloning the repository, navigate to the project directory:
   ```
   cd csusb_fall2024_cse6550_team3
   ```

3. Update your local repository to the latest version:
   ```
   git pull origin main
   ```

4. Preliminary steps: Make sure to execute all three steps given below to delete any previous Docker image.

   To see all the running containers on your machine:
   ```
   docker ps
   ```
  
   To stop a running container, replace `<container_id>` with the one found in the `docker ps` output:
   ```
   docker stop <container_id>
   ```

   To remove/delete a Docker container, replace `<container_id>` with the one found in the `docker ps` output:
   ```
   docker rm <container_id>
   ```

5. Build the Docker image using the following command:

   Before running this command, make sure to include the API key at the end.

   Go to [team3](https://csusb.instructure.com/courses/43192/discussion_topics/419698) on Canvas for the API key.
   ```
   docker build -t team3-app . --build-arg MISTRAL=
   ```

6. Now, run the Docker container:
   ```
   docker run -d -p 5003:5003 team3-app
   ```

7. Allow up to 5 minutes before accessing the application.

   The application will be available at:

   - Website: [http://localhost:5003/team3](http://localhost:5003/team3)

8. Run the setup script:
   ```
   python setup.py
   ```
   When prompted, enter the Mistral API key from Canvas to complete the setup process.

9. To access the Jupyter notebook, run the following script:
   ```
   python3 run_jupyter.py
   ```
   Enter the Mistral API key when prompted to access the Jupyter notebook.

## Evaluation Questions

Below is a list of answerable and unanswerable questions that will be used to evaluate the application:

| **Answerable**                                                     | **Unanswerable**                                                        |
|--------------------------------------------------------------------|-------------------------------------------------------------------------|
| Who is Hironori Washizaki?                                         | What is the largest possible number that could exist?                   |
| How does software testing impact the overall software development lifecycle? | How will AI evolve in the next 100 years?                               |
| What is the agile methodology?                                     | What is the solution to the Riemann Hypothesis?                         |
| What are the different types of software models, and when should each be used? | What is the smallest possible Turing machine?                          |
| How does software configuration management ensure project success? | What is the most complex algorithm that can never be solved?            |
| What role do user requirements play in software design and architecture? | What is the most efficient way to handle an infinite stream of data?  |
| What is software dependability?                                    | Is there a way to build a fully self-sustaining human colony on Mars with current technology? |
| How does project management in software engineering differ from traditional project management? | What's the upper limit of computational power for classical computers? |
| What strategies can be used for effective risk management in software engineering projects? | How could we fully eliminate all types of noise in wireless communications? |
| What is the purpose of static analysis in software testing?        | How can we create a material that is completely indestructible?         |

## Troubleshooting

1. **I ran the Docker run command but the website gives me `localhost refused to connect` error**
   
   This is probably because the application is still being spun up. Wait for a few minutes and try again.

2. **I'm in light mode and the website is unreadable**
   
   On the Streamlit homepage, go to settings and select the custom theme.

## Project Structure

- `.github/workflows/docker-publish.yml`: GitHub Action workflow to automate Docker publishing
- `app.py`: Main entry point for the application
- `data`
  - `default`: Contains textbook PDF and FAISS indexes
    - `textbook`: PDF
    - `faiss_indexes`: Pre-built embeddings and metadata for the textbook
- `backend`
  - `document_loading.py`: Document loading, embedding creation, and search logic
  - `inference.py`: LLM inference and RAG logic
  - `prompts.py`: Contains the prompt
  - `citations.py`: Logic for getting sources for a response
  - `statistics.py`: Database schema and querying
- `frontend`
  - `styles/`: CSS styling
  - `streamlit.py`: Main Streamlit file
  - `pdf.py`: PDF viewer
  - `utils.py`: Contains utility functions such as the confusion matrix
- `jupyter`
  - `main.ipynb`: Jupyter notebook file
- `.env.template`: Template for what a .env file should look like
- `.gitignore`: Files and directories to be ignored by Git
- `Dockerfile`: Instructions to build the Docker image
- `README.md`: Project documentation
- `requirements.txt`: Lists required Python dependencies

## Affiliation

Built by **Team 3**

Course: CSE 6550, Fall '24 (Software Engineering Concepts)

Institution: California State University, San Bernardino

