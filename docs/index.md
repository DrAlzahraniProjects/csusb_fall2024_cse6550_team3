**Welcome to the csusb_fall2024_cse6550_team3 wiki!**     

## About project 

The textbook chatbot project for CSE 6550 is designed to assist with queries related to the textbook "Software Engineering Body of Knowledge (SWEBOK)." The chatbot serves as an educational tool, helping users by providing information, answering questions, and possibly retrieving content from the textbook.

## Table of contents
- [Features](#features)
- [Getting started](#setup)
- [FAQ](#faq)
- [Community and support](#community-and-support)
- [Contact](#contact)

## Features
- Answers questions about [SWEBOK](https://www.computer.org/education/bodies-of-knowledge/software-engineering) textbook with sources.
- Confusion matrix and performance metrics for evaluation.
- User feedback mechanism.

## Setup

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

## Jupyter Notebook Setup 
1. How to run the jupyter notebook in virtual environment.
   
   * Navigate to the folder:
     ```bash
     cd csusb_fall2024_cse6550_team3/jupyter
     ```
   * Run jupyter notebook:
     ```bash
     jupyter notebook --port=6003
     ```
   * Wait for the browser to open automatically.
     
      If it doesn't open, use the following link: http://localhost:6003/tree


For advanced testing and debugging, refer to the provided [Jupyter notebook](https://sec.cse.csusb.edu/team3/jupyter).

---

## FAQ

1. What is this chatbot designed to do? 

   This chatbot is designed to assist users with answering questions from SWEBOK Textbook.

2. How do I interact with the chatbot?

   You can interact with the chatbot by following the above instructions on how to install, once you have the docker image built you can directly ask 
   questions on the chatbot which uses Streamlit UI.

3. What platforms does the chatbot support?

   The chatbot can be deployed on your local system and used in almost all browsers like Brave, Chrome and Edge.

4. How can I customize the chatbot?

   You can customize the chatbot by customization instructions.

5. What technologies were used to build the chatbot?

   The chatbot was built using a lot of different technologies to make it functional and efficient, we have used Langchain for the backend, Streamlit 
   for the frontend and Mistral as our core LLM 

6. What should I do if the chatbot doesn’t respond?

   If the chatbot doesn’t respond, try troubleshooting steps.

7. How do I report bugs or issues?

   You can report bugs or issues by creating a new issue on the GitHub issues page from [here](https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3/issues) or contact the project manager from the given email below 

8. Can the chatbot handle multiple users?

   Yes, the chatbot is designed to handle multiple users simultaneously.

9. Is there a limit to the number of questions I can ask?

   No, there is no limit to the number of questions you can ask.

## Community and support
[Click here for technical and non technical discussions](https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3/discussions)

## Contact
Project manager: Fruzsina Ladanyi, 008455051@coyote.csusb.edu

## Feedback
[Click here to submit your feedback](https://forms.gle/i29r4a7dunjwBNDQA)
