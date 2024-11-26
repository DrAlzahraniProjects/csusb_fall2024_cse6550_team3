# Textbook Chatbot

This chatbot is as an educational tool that's built to answer questions related to the Swebok textbook, [Software Engineering Body of Knowledge (SWEBOK)](https://www.computer.org/education/bodies-of-knowledge/software-engineering). The chatbot was built by team 3 for [CSE 6550: Software Engineering Concepts](https://catalog.csusb.edu/coursesaz/cse/)

[Website](https://sec.cse.csusb.edu/team3/)  
[Jupyter notebook](https://sec.cse.csusb.edu/team3/jupyter)

---

## Prerequisites

Before you begin, make sure you have the following installed on your machine:
- **Git**
- **Docker**
- **Python 3.10 or above**

---

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

---

## Jupyter Notebook Setup (Handled Separately)

To run Jupyter Notebook independently from the repository, please download the following files:

SWEBOK Corpus: [swebok.pdf](https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3/blob/main/data/swebok/textbook.pdf)

Jupyter Notebook: [main.ipynb](https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3/tree/main/jupyter)

- Create a new directory and place only these two files (swebok.pdf and main.ipynb) inside the directory. This will ensure there are no file path issues during execution.

Navigate to the new directory in the terminal before launching Jupyter Notebook:
Open a terminal and use the cd command to navigate to the directory where you saved swebok.pdf and main.ipynb. For example:
```bash
cd csusb_fall2024_cse6550_team3/jupyter
```

Run the Jupyter Notebook:

In the terminal, type the following command to launch Jupyter Notebook:
```bash
jupyter notebook --port=6003
```
This will open the Jupyter Notebook interface in your web browser, where you can open main.ipynb and run it.

If it doesn't open, use the following link: http://localhost:6003/tree

For advanced testing and debugging, refer to the provided [Jupyter notebook](https://sec.cse.csusb.edu/team3/jupyter).


---

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
---

## Evaluation Questions

Below is a list of answerable and unanswerable questions that will be used to evaluate the application:

| **Answerable**                                                     | **Unanswerable**                                                        |
|--------------------------------------------------------------------|-------------------------------------------------------------------------|
| Who is Hironori Washizaki?                                         | What is the largest possible number that could exist?                   |
| How does software testing impact the overall software development lifecycle? | How will AI evolve in the next 100 years?                              |
| What is the agile methodology?                                     | What is the solution to the Riemann Hypothesis?                         |
| What are the different types of software models, and when should each be used? | What is the smallest possible Turing machine?                         |
| How does software configuration management ensure project success? | What is the most complex algorithm that can never be solved?           |
| What role do user requirements play in software design and architecture? | What is the most efficient way to handle an infinite stream of data?    |
| What is software dependability?                                    | Is there a way to build a fully self-sustaining human colony on Mars?   |
| How does project management in software engineering differ from traditional project management? | What's the upper limit of computational power for classical computers? |
| What strategies can be used for effective risk management in software engineering projects? | How could we fully eliminate all types of noise in wireless communications? |
| What is the purpose of static analysis in software testing?        | How can we create a material that is completely indestructible?         |

---

## Troubleshooting

1. **"Website gives localhost refused to connect error"**:
   - Likely the application is still initializing. Wait 5 minutes and try again.

2. **"Website is unreadable in light mode"**:
   - On the Streamlit homepage, go to settings and select the custom theme.

---

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

---

## Affiliation

Built by **Team 3**  
Course: CSE 6550, Fall '24 (Software Engineering Concepts)  
Institution: California State University, San Bernardino  

--- 
