**Welcome to the csusb_fall2024_cse6550_team3 wiki!**     

## About project 

The textbook chatbot project for CSE 6550 is designed to assist with queries related to the textbook "Software Engineering: A Practitioner's Approach." The chatbot serves as an educational tool, helping users by providing information, answering questions, and possibly retrieving content from the textbook.

## Table of contents
- [Features](#features)
- [Getting started](#getting-started)
- [FAQ](#faq)
- [Community and support](#community-and-support)
- [Contact](#contact)

## Features
- Answers questions about SWEBOK Textbook with sources.
- Confusion matrix and performance metrics for evaluation.
- User feedback mechanism.

## Setup

1. To get started, first clone the repository to your local machine:
   ```
   git clone https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3.git
   ```

2. After cloning the repository, navigate to the project directory:
   ```
   cd csusb_fall2024_cse6550_team3
   ```

3. Update local repository
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

5. Build the docker image using the following command:

   Before running this command include API key in the end 

   Go to [team3](https://csusb.instructure.com/courses/43192/discussion_topics/419698) in canvas for API key
   
   ```
   docker build -t team3-app . --build-arg MISTRAL=
   ```
6. Now, run the docker container:
 
   ```
   docker run -d -p 5003:5003 -p 6003:6003 team3-app
   ```

7. Allow upto 5 minutes before accessing the application
    
   The application will be available at
  
    Website: [http://localhost:5003/team3](http://localhost:5003/team3)
   
    Jupyter: [http://localhost:6003/team3/jupyter](http://localhost:6003/team3/jupyter)


## FAQ

1. What is this chatbot designed to do? 

   This chatbot is designed to assist users with answering questions from SE Textbook.

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
