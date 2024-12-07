# Textbook Chatbot

This chatbot is as an educational tool that's built to answer questions related to the Swebok textbook, [Software Engineering Body of Knowledge (SWEBOK)](https://www.computer.org/education/bodies-of-knowledge/software-engineering). The chatbot was built by team 3 for [CSE 6550: Software Engineering Concepts](https://catalog.csusb.edu/coursesaz/cse/)

[Website](https://sec.cse.csusb.edu/team3/)  
[Jupyter notebook](https://sec.cse.csusb.edu/team3/jupyter)

## Prerequisites

Before you begin, make sure you have the following installed on your machine:
- **Git**
- **Docker**
- **Python 3.10 or above**


## Automated App Setup ##

The `setup.py` script automates the setup process, including downloading the repository, building the Docker container, and running the application.

### Steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3.git
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd csusb_fall2024_cse6550_team3
   ```
3. **Update Local Repository**:
   ```
   git pull origin main
   ```
4. **Run the Setup Script**:  
   ```bash
   python setup.py
   ```
   **Note:** If the above command does not work (e.g., on Linux), try using:
   ```bash
   python3 setup.py
   ```

4. **Follow On-Screen Prompts**:
   - The script will ask for the Mistral API key (provided in the team discussion on Canvas).
   - It will stop any existing containers, pull updates, build the Docker image, and run the container.

5. **Access the Application**:
   - Website: [http://localhost:5003/team3](http://localhost:5003/team3)


## Jupyter Notebook Setup (Handled Separately)

To run the Jupyter Notebook independently from the repository, please follow these steps:

 Jupyter Notebook: [main.ipynb](https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3/blob/main/jupyter/main.ipynb)

1. Download the Required File:

- Jupyter Notebook: ```main.ipynb```.

2. Create a New Directory:

- Ensure a clean environment by creating a new directory to avoid file path issues during execution.

3. Move the File:

- Place the ```main.ipynb``` file in the newly created directory.

4. Navigate to the New Directory:

- Open a terminal and use the `cd` command to navigate to the directory where you saved ```main.ipynb```. For example:
```bash
  cd ~/csusb_fall2024_cse6550_team3/jupyter
```
5. Launch Jupyter Notebook:

- In the terminal, type the following command to start Jupyter Notebook:
```bash
jupyter notebook --port=6003
```

- This will open the Jupyter Notebook interface in your web browser, where you can open ```main.ipynb``` and run it.

- If it doesn't open, use the following link: http://localhost:6003/tree

- For advanced testing and debugging, refer to the provided [Jupyter notebook](https://sec.cse.csusb.edu/team3/jupyter).


## Manual Docker Setup (Alternative)

If for any reason you cannot use `setup.py`, follow the steps below:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3.git
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd csusb_fall2024_cse6550_team3
   ```

3. **Pull Updates**:
   ```bash
   git pull origin main
   ```

4. **Stop and Remove Running Containers**:
   - Check running containers:
     ```bash
     docker ps
     ```
   - To stop a running container, replace `<container_id>` with the ID from the `docker ps` output:
     ```bash
     docker stop <container_id>
     ```
   - To remove/delete a container:
     ```bash
     docker rm <container_id>
     ```

5. **Build Docker Image**:
   ```bash
   docker build -t team3-app . --build-arg MISTRAL=<your_api_key>
   ```

6. **Run Docker Container**:
   ```bash
   docker run -d -p 5003:5003 team3-app
   ```
**Access the Application**:
   - Website: [http://localhost:5003/team3](http://localhost:5003/team3)


## Testing

1. **Build Docker image**
   ```bash
   docker build -t team3-app .
   ```
2. **Run tests**
   ```bash
   docker run --env-file .env -v $(pwd):/app --entrypoint python team3-app -m pytest tests/test_questions.py -p no:warnings --tb=no -s
   ```

## Evaluation Questions

Below is a list of answerable and unanswerable questions that will be used to evaluate the application:

| **Answerable**                                                     | **Unanswerable**                                                        |
|--------------------------------------------------------------------|-------------------------------------------------------------------------|
| Who is Hironori Washizaki?                                         | What class does Dr. Alzahrani teach?                   |
| How does software testing impact the overall software development lifecycle? | How will AI evolve in the next 100 years?                     |
| What is the agile methodology?                                     | What GPA do you have?                         |
| What are the different types of software models, and when should each be used? | What is the smallest possible Turing machine?               |
| How does software configuration management ensure project success? | Microsoft stock price?                                                    |
| What role do user requirements play in software design and architecture? | What is the most efficient way to handle an infinite stream of data?    |
| What is software dependability?                                    | Is there a way to build a fully self-sustaining human colony on Mars?   |
| How does project management in software engineering differ from traditional project management? | What is chapter 200 about? |
| What is chapter 11 about?                                          | How could we fully eliminate all types of noise in wireless communications? |
| What is the purpose of static analysis in software testing?        | How can we create a material that is completely indestructible?         |


## Troubleshooting

1. **"Website gives localhost refused to connect error"**:
   - Likely the application is still initializing. Wait 5 minutes and try again.

2. **"Website is unreadable in light mode"**:
   - On the Streamlit homepage, go to settings and select the custom theme.


## Project Structure

- **Setup and Automation**:
  - `setup.py`: Automates downloading, building, and running the application.
- **Jupyter Notebooks**:
  - `jupyter/main.ipynb`: Contains Jupyter notebook for advanced testing and debugging.
- **Frontend**:
  - `frontend/streamlit.py`: Main Streamlit app file.
  - `frontend/styles/`: Contains CSS styles.
  - `frontend/pdf.py`: Handles PDF rendering.
- **Backend**:
  - `backend/document_loading.py`: Logic for loading documents and creating embeddings.
  - `backend/inference.py`: Handles inference using LLM.
  - `backend/citations.py`: Source citation logic.
  - `backend/statistics.py`: Database schema and querying.
- **Data**:
  - `data/default/`: Contains textbook PDFs and FAISS indexes.
- **Other**:
  - `Dockerfile`: Instructions to build Docker images.
  - `README.md`: Project documentation.
  - `.env.template`: Template for environment variables.


## Affiliation

Built by **Team 3**  
Course: CSE 6550, Fall '24 (Software Engineering Concepts)  
Institution: California State University, San Bernardino  

