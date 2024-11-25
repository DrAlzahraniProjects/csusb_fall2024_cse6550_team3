# About
This documentation provides a comprehensive guide for containerizing a Streamlit application using Docker, specifically aimed at deploying a chatbot based on a software engineering textbook. By following this guide, you'll not only learn how to set up your development environment but also understand how to implement, configure, and troubleshoot your containerized application. Additionally, this guide will walk you through best practices in Dockerization and offer insights into maintaining a seamless development experience.

The chatbot you're building is designed to assist users in interacting with a textbook using natural language, driven by a large language model (LLM). The advantage of containerizing this application is that it ensures consistency across different environments, streamlines deployment, and makes the application more portable. As we explore containerization, you’ll learn not only to run the chatbot locally but also prepare it for production deployment.

# Table of Contents
1. [Installation](https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3/wiki/StreamLit/#1-installation)
2. [Configuration](https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3/wiki/StreamLit#2-configuration)
3. [Implementation](https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3/wiki/StreamLit#3-implementation)
4. [Usage](https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3/wiki/StreamLit#4-usage)
5. [Troubleshooting](https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3/wiki/StreamLit#5-troubleshooting)

# 1. Installation
Containerizing a Streamlit application begins with ensuring your development environment is prepared for efficient, containerized workflows. In this guide, we'll focus on using Docker and Mamba to manage dependencies, providing a clean, portable, and consistent environment for development and deployment.

This section will guide you through the installation process, including setting up Docker, configuring Mamba, and creating an isolated environment for your Streamlit application.

## Step 1. Ensure Docker is Installed
Docker is the backbone of our containerized workflow. It enables you to package your application and its dependencies into a portable container, ensuring consistency across development, testing, and production environments.


### Instructions:
1. Open your terminal and run the following command to verify if Docker is installed:
```bash
docker --version

```

This command should return the installed Docker version, as shown in the screenshot below:

<img width="577" alt="Screenshot 2024-11-21 at 2 57 32 PM" src="https://github.com/user-attachments/assets/3ccf80e9-5f9a-4716-a741-2c72fc0609bc">

_Figure 1:_ If Docker is already installed, it will show you the version like this. 

If Docker isn’t installed, proceed to the next step.

2. Download and install Docker Desktop from the official [Docker website](https://www.docker.com/). After downloading, follow the installation instructions specific to your operating system (Windows, macOS, or Linux). Once installed, you should be able to verify the version again using the previous command.

3. After installation, verify Docker is working by running:

```bash
docker run hello-world

```

This command pulls and runs a test image to confirm your Docker setup is functional.
<img width="723" alt="Screenshot 2024-11-21 at 3 04 56 PM" src="https://github.com/user-attachments/assets/34f560fb-6b59-4f09-aa63-3faae29ab023">

_Figure 2:_ If Docker is installed properly, it will give you the message like this. 


# 2. Configuration
In this section, you will configure the necessary files and settings to prepare your Streamlit application for Dockerization. Proper configuration is crucial to ensure that your Docker container runs your application smoothly. We’ll cover the creation of a requirements.txt file, configuring a Dockerfile, and building a Docker image for your application.

## Step 1. Create a requirements.txt File
A requirements.txt file lists the dependencies required by your Python application. This ensures that when the Docker container is built, all necessary libraries and packages are installed consistently across different environments.

Example requirements.txt:

<img width="287" alt="Screenshot 2024-10-11 at 3 03 41 PM" src="https://github.com/user-attachments/assets/3c746df6-e87d-487c-a974-6a13d11109cf">

_Figure 3:_ Sample of requirements.txt file

This file lists all the necessary packages for the application. You can generate this file manually, or if you already have the dependencies installed, you can export them using:
```bash
pip freeze > requirements.txt

```

This will generate a requirements.txt file based on the libraries installed in your current environment. It’s important to maintain this file to ensure reproducibility across environments.


## Step 2. Dockerfile Configuration
The Dockerfile is a blueprint that defines how your Docker image will be created. It includes instructions for setting up the environment, installing dependencies, and running the application. Here’s a step-by-step guide to building your Dockerfile:

* Use Python as the base image
```bash
FROM python:3.11-slim

```
* Copy requirements.txt into the container
```bash
COPY requirements.txt /app/requirements.txt

```
* Install Python packages from requirements.txt
```bash
RUN mamba install --yes --file requirements.txt && mamba clean --all -f -y

```
* Expose the port that Streamlit will run on
```bash
EXPOSE 5003

```
* Command to run the Streamlit app
```bash
CMD ["streamlit", "run", "app.py"]

```

Explanation:
1. FROM: Specifies the base image (python:3.11-slim) to keep the container lightweight.
2. WORKDIR: Sets the working directory within the container.
3. COPY: Transfers files into the container.
4. RUN: Installs the necessary Python dependencies.
5. EXPOSE: Opens the required port for the Streamlit application.
6. CMD: Specifies the default command to run the application when the container starts.


## Step 3. Building the Docker Image
Once your Dockerfile is prepared, you can build the Docker image. This process packages your application and its dependencies into a single image.

### Instructions:

1. Run the following command to build the Docker image:
```bash
docker build -t team3-app .

```
This command creates a Docker image named team3-app. The terminal will display the build process, and a successful build should output something similar to the screenshot below:

<img width="821" alt="Screenshot 2024-10-11 at 3 35 28 PM" src="https://github.com/user-attachments/assets/6895250e-57c6-4df8-ba5b-1630754340d8">

_Figure 4:_ To view the build details you can access that URL

## Step 4. Running the Docker Container
After the Docker image is built, you can run the container using the following command:

```bash
docker run --env-file .env -p 5003:5003 -v $(pwd):/app team3-app

```
Explanation:
1. --env-file .env: Loads environment variables from the .env file (if any).
2. -p 5003:5003: Maps the host’s port 5003 to the container’s port 5003.
3. -v $(pwd):/app: Mounts the current directory into the container to enable changes without rebuilding the image.

This exposes the Streamlit app on port 5003 so you can now view your Streamlit app in your browser using the following URL:
```bash
http://0.0.0.0:5003/team3

```

# 3. Implementation
With your Dockerized environment set up, the next step is to implement the Streamlit application. This section will guide you through the basic structure of a Streamlit app, integrating your LLM-based chatbot, and handling user inputs.

## Step 1. Importing Streamlit
Begin by importing the necessary libraries into your app.py file.
```bash
import streamlit as st

```
<img width="979" alt="Screenshot 2024-10-11 at 4 11 34 PM" src="https://github.com/user-attachments/assets/e843d6a4-95f8-4a39-a732-0561b0e361ad">

_Figure 5:_ This a basic structure of importing required dependencies.


## Step 2. Add widgets
Streamlit offers a variety of widgets and layout components to create interactive web apps.
* Container Widget

st.container() is a layout element that allows you to create a section (or container) within your app where you can group and add multiple components (like text, buttons, charts, etc.)


<img width="846" alt="Screenshot 2024-10-11 at 4 15 58 PM" src="https://github.com/user-attachments/assets/f85f17ca-bb75-4da5-aee7-422e3b6a8181">

_Figure 6:_ Example for the use of st.container()


* Markdown Widget

st.markdown() is a function used to display formatted text using Markdown syntax


<img width="810" alt="Screenshot 2024-10-11 at 4 19 36 PM" src="https://github.com/user-attachments/assets/42fed75b-e988-4ff0-a281-e5b6c039e88e">

_Figure 7:_ Example for the use of st.markdown()

* Sidebar Widget

Streamlit's sidebar feature is handy for navigation or filters.
It allows you to add widgets (e.g., sliders, text inputs, buttons) to a sidebar
> For example

```bash
st.sidebar.markdown("<h2><a href='https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3?tab=readme-ov-file#evaluation-questions'>Evaluation Report</a></h2>", unsafe_allow_html=True)

```

<img width="1499" alt="Screenshot 2024-11-15 at 8 53 10 PM" src="https://github.com/user-attachments/assets/bb74e14c-8734-4da7-b745-6f8a45875ff8">
_Figure 8:_ This is how you can use the st.sidebar()


```bash
st.sidebar.markdown(
        f"""
        <div class='metric-container'>
            <div class='metric-main' title="{m_tooltip['Sensitivity']}">
                <span class='metric-label'>Sensitivity:</span>
                <span class='metric-value'>{f"{metrics['Sensitivity']:.2f}" if metrics['Sensitivity'] is not None else 'N/A'}</span>
            </div>
            <div class='metric-main' title="{m_tooltip['Specificity']}">
                <span class='metric-label'>Specificity:</span>
                <span class='metric-value'>{f"{metrics['Specificity']:.2f}" if metrics['Specificity'] is not None else 'N/A'}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

```
<img width="1495" alt="Screenshot 2024-11-15 at 8 56 19 PM" src="https://github.com/user-attachments/assets/9fdca82e-053f-4b08-8643-09c8d4df8087">


_Figure 9:_ This is how you can add components to your sidebar



## Step 3. Adding Custom CSS for Styling

To enhance the user interface, you can include custom CSS. Streamlit allows injecting custom HTML and CSS.

* This is the file structure we followed for the styling in order to stay organized

<img width="256" alt="Screenshot 2024-11-15 at 9 00 46 PM" src="https://github.com/user-attachments/assets/4c445477-467e-4de5-96cf-a1a825888b2a">


_Figure 10:_ Example for the file structure

* Here’s how to load a custom CSS file:


```bash
def load_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("Styles/style.css")

```
This function loads the style.css file and applies the styles to your Streamlit app.

# 4. Usage

To maintain state across sessions, use st.session_state to store user inputs or application states.

<img width="1206" alt="Screenshot 2024-10-11 at 5 09 24 PM" src="https://github.com/user-attachments/assets/5f727e03-e458-41c8-9c56-28bd4b584b49">

_Figure 11:_ This ensures that the application retains certain values between different user interactions.

## Step 1: Starting the Application
Start the application using the command specified in the Dockerfile.
```bash
docker run --env-file .env -p 5003:5003 -v $(pwd):/app team3-app

```

Access the app through your web browser using the provided URLs. If you see this message then the server is running and streamlet is working.

<img width="1080" alt="Screenshot 2024-10-13 at 5 26 14 PM" src="https://github.com/user-attachments/assets/008f7adb-7196-4221-9e88-979db7bc0900">

_Figure 12:_ This is how your terminal should look like

## Step 2: Interacting with the Chatbot:

Once the app is live, users can interact with the chatbot by typing in their queries. The chatbot uses an LLM (language model) to generate responses based on the input. The interface is designed for smooth navigation and user interaction.

Examples of Interaction:
1. User inputs a question.
2. The chatbot processes the query using the underlying LLM model.
3. The application returns a response and may suggest follow-up actions.

**User Input:** "What are the key concepts in Agile software development?"

**Chatbot Response:** "The key concepts in Agile software development include:
Values and principles: These include always delivering value to the customer, commitment to technical excellence, and the importance of communication.
Practices: These are the specific methods and techniques used in Agile development, such as peer programming, sprint planning, and retrospective.
Lightweight methods: Agile methods are considered lightweight because of their short, iterative development cycles, self-organizing teams, simpler designs, code refactoring, test-driven development, frequent customer involvement, and emphasis on creating a demonstrable working product with each development cycle.
Agile methods: There are several popular Agile methods, including Extreme Programming (XP), Scrum, Feature-Driven Development (FDD), and Lean software development.
DevOps: DevOps is a set of principles and practices that enable better communication and collaboration between relevant stakeholders for the purpose of specifying, developing, and operating software and systems products and services, and continuous improvements in all aspects of the life cycle.
Continuous delivery: Agile development emphasizes the need for frequent releases to address changing user needs and technological life cycles
"

**User Input:** "Can you explain the difference between functional and non-functional requirements?"

**Chatbot Response:** "Functional requirements and non-functional requirements are two categories of software requirements that serve different purposes.
Functional requirements specify the observable behaviors that the software is expected to provide. They define what the software should do and how it should perform its intended functions. Examples of functional requirements include policies to be enforced, such as "an account shall always have at least one customer as its owner," and processes to be carried out, such as the meanings of depositing and withdrawing money from an account.

On the other hand, non-functional requirements constrain the technologies to be used in the implementation of the software. They specify qualities that the software must possess, such as performance, reliability, usability, and security. Examples of non-functional requirements include response time, throughput, accuracy, and scalability.

In summary, functional requirements focus on what the software should do, while non-functional requirements focus on how well the software should do it."

These examples help illustrate how users can interact with the chatbot and what kind of information they can expect in return.


# 5. Troubleshooting

Despite careful configuration, errors may occur during the development or deployment of your Streamlit application. Here are some common issues and their solutions.


## 1. Access Issues
If you cannot access the application in your browser, verify the following:

   - **Ports**: Ensure that the port specified in the Dockerfile matches the port in your URL. For example, if your Dockerfile exposes port 5003, make sure the URL is `http://0.0.0.0:5003`.

   *Example*: If the Dockerfile exposes port 5003, your URL should be:
  
   http://0.0.0.0:5003

<img width="691" alt="Screenshot 2024-10-11 at 5 16 44 PM" src="https://github.com/user-attachments/assets/a908aa5d-e232-4aa1-98bd-5034a82df321">

_Figure 13:_ PORT exposed


<img width="312" alt="Screenshot 2024-10-11 at 5 17 37 PM" src="https://github.com/user-attachments/assets/d87ec634-9f73-4c83-887a-2f9b2909e80d">

_Figure 14:_ PORT in URL

Both has to be same

## 2. Check for errors

Check both the terminal and browser for error messages. Typically, Streamlit will display useful logs in the terminal that can help debug issues. Below is an example of a browser error:

![3ae2f46a2945b420ad4327c51293288c80be40bb](https://github.com/user-attachments/assets/4904318a-f79a-47fd-b591-8bfb752b48b0)

_Figure 15:_ An example of an Streamlit error

Common Log Entry Example: If you see an error like ModuleNotFoundError: No module named 'streamlit', it indicates that the streamlit library was not installed correctly. You can resolve this by checking your requirements.txt file and ensuring all packages are installed.

## 3. Dependency Issues
Make sure that all dependencies are installed correctly by verifying the requirements.txt file. If a required package is missing or has an incompatible version, you can update it by running:

```bash
pip install <package> --upgrade

```

## 4. Debugging in Docker
Use Docker logs to troubleshoot issues inside the container. You can view the logs using:
```bash
docker logs <container-id>

```

This will give you detailed information about the application’s runtime behavior.

Common Log Entry Example: If you see an error like ModuleNotFoundError: No module named 'streamlit', it indicates that the streamlit library was not installed correctly. You can resolve this by checking your requirements.txt file and ensuring all packages are installed.

Tip: Look for error messages or stack traces in the logs to identify the root cause of any issues.

# Conclusion
By following this guide, you now have a fully containerized Streamlit application running within Docker, ready to be deployed as an interactive chatbot. You've learned how to install the necessary dependencies, configure Docker, build and run the application, and even troubleshoot common issues.

By following this guide, you’ll have successfully containerized your Streamlit chatbot application, integrated an LLM, and deployed it using Docker. The advantage of Dockerizing the application is that it guarantees consistency across environments and simplifies the deployment process. Whether you're running the chatbot locally for development or deploying it in a production environment, this documentation serves as a comprehensive reference.


