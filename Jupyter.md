# Jupyter

This Wiki provides a guide to setting up and running **Jupyter Notebook** inside a docker container


---

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Implementation](#implementation)
4. [Usage](#usage)
5. [Troubleshooting](#troubleshooting)

---

## Installation

**To install Jupyter in the Dockerfile provided, follow these steps:**


1 Make sure to add Jupyter to your `requirements.txt` file so that it gets installed with the other Python packages:

```bash
jupyter
ipykernel
```
![image](https://github.com/user-attachments/assets/795444f9-8220-4d5d-8d4f-c03c5b3940a3)

**Image 1: Add Jupyter to ```requirements.txt```**

2. ### Check dependencies

- Specify the base image for the Docker container in your Dockerfile. Use the lightweight version of Python:

```bash
FROM python:3.11-slim
```
- Set the working directory:

```bash
WORKDIR /app
```
![image](https://github.com/user-attachments/assets/ee929146-3fb0-43a5-840b-1727dbdd534e)

**Image 2: Check dependencies and base image**

- This specifies the base image for the Docker container. It uses the python:3.11-slim image, which is a lightweight version of Python 3.11
- ```WORKDIR /app``` this sets the working directory inside the Docker container to ```/app```
- ```RUN apt-get update && apt-get install -y wget```: This line uses the ```RUN``` command to execute shell commands during the Docker build process
- ```apt-get update```: Updates the list of available packages and their versions, ensuring that the container has access to the latest package information
- ```apt-get install -y wget```: Installs the wget package, a tool used to download files from the web. The ```-y``` flag automatically answers "yes" to any prompts, making the installation process non-interactive

- It’s crucial to test whether the base image provides all the dependencies needed for your application to function smoothly, and additional system dependencies (like compilers or dev tools) might be necessary for certain packages.

3. ### Jupyter Installation in Docker

Verify Docker Installation: Before setting up Jupyter in Docker, make sure Docker is installed by running:

``` bash
docker --version
```

If Docker is not installed, refer to the https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3/wiki/Docker

4. ### Modify the Dockerfile

- To install Jupyter, you need to ensure that it's included in the environment setup

![image](https://github.com/user-attachments/assets/6c1170c8-f064-4580-b7a9-c7742f7dd9f5)

**Image 3: Copy requirements** into the docker by following command

```bash
COPY requirements.txt /app/requirements.txt
```
- This is a Docker instruction used to copy files from the host machine (the machine where you're building the Docker image) into the Docker container
- ```requirements.txt```: This is the source file located on your host machine. It typically lists all the Python packages and dependencies that need to be installed in the container
- ```/app/requirements.txt```: This is the destination path inside the Docker container where the ```requirements.txt``` file will be placed

5. ### Jupyter installation

- To install Jupyter, ensure you have Python `3.x` installed on machine. You can install Jupyter using `pip.` Run the following command in your terminal:

```bash
pip install jupyter
```
- Prerequisites:

- Ensure you have Python 3.6 or later installed: If you don't have pip installed, you can refer to the [official pip installation guide](https://pip.pypa.io/en/stable/installation/).

- Install Jupyter to docker by using following commands

```bash
RUN /bin/bash -c "source ~/.bashrc && mamba install -c conda-forge jupyter"
```

![image](https://github.com/user-attachments/assets/bdad4af2-1784-423d-ab91-872899f11368)
  **Image 4: Jupyter installation in the docker file**

- This line installs Jupyter Notebook along with the required IPython kernel inside the Docker container

- ```RUN```: This Docker instruction is used to execute commands in the container during the build process
- ```/bin/bash -c```: This ensures that the command is run in a Bash shell. The ```-c``` option tells Bash to execute the following command string
- ```source ~/.bashrc```: This reloads the environment variables from the .bashrc file, which may contain necessary paths or environment settings for the container. It makes sure that the current shell has access to all the configurations that were set up earlier.
```mamba install```: ```mamba``` is a fast package manager (similar to conda), this command installs the necessary packages inside the environment, it’s faster and more efficient than ```conda``` but works similarly
- ```-c conda-forge```: This tells ```mamba``` to download and install the packages from the ```conda-forge channel```, which is a widely-used repository for Python and data science tools. It’s a trusted source for getting Jupyter and other related packages
- ```jupyter```: This is the main Jupyter Notebook application, which provides a web-based interface for writing and running Python code interactively
- ```ipykernel```: This package provides the IPython kernel, which allows Jupyter to run Python code in the notebooks. Without it, Jupyter won’t be able to execute python code

## 
### 
# Configuration

**Steps to configure Jupyter in the Dockerfile:**
1. ### Environment activation

```bash
ENV PATH /root/miniconda3/envs/team3_env/bin:$PATH
```

- Set the environment path for your Conda environment:
- The environment path is set to include ```team3_env```

- The activation command is appended to ```.bashrc``` to activate the environment

```bash
RUN echo "source activate team3_env" >> ~/.bashrc
```

![image](https://github.com/user-attachments/assets/dc16e840-0186-4ce2-85ba-6e369f708381)

  **Image 5: Activate the environment**

- This Dockerfile snippet sets up a Python environment using Conda (specifically Miniconda) and installs packages specified in a ```requirements.txt``` file:
- ```ENV PATH```: Adds the ```team3_env``` conda environment's binaries to the system's ```PATH```, so tools installed in that environment can be used directly
- ```SHELL```: Changes the shell to bash, allowing bash commands to be executed in the following steps
- ```RUN echo```: Appends a command to activate the ```team3_env``` environment to the ```.bashrc``` file, so the environment is activated whenever a shell session starts
- ```COPY```: Copies the ```requirements.txt``` file (which lists Python dependencies) into the container at ```/app/requirements.txt```
- ```RUN /bin/bash -c```: Activates the environment, installs the Python packages listed in ```requirements.txt``` using Mamba (a faster Conda alternative), and then cleans up unnecessary files to reduce the image size
- This process ensures that all necessary dependencies for the project are installed in a controlled environment within the container

- Setting up environment variables correctly is essential for the Docker container's smooth operation. By adding the environment variables to the ```.bashrc``` or ```.bash_profile``` files, you ensure that the environment is consistently activated during container runs.


2. ### Jupyter configuration

Create a configuration directory and set configurations:

- Create a configuration directory and set configurations:

```bash

RUN mkdir -p /root/.jupyter && \
    echo "c.NotebookApp.allow_root = True" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.ip = '0.0.0.0'" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.port = 6003" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.open_browser = False" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.token = ''" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.password = ''" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.log_level = 'DEBUG'" >> /root/.jupyter/jupyter_notebook_config.py
```
- Note: The above commands configure Jupyter Notebook to run without authentication and to listen on all network interfaces.

- Creates a directory at ```/root/.jupyter.``` The ```-p``` option ensures that no error is thrown if the directory already exists, and it will also create any necessary parent directories
- This appends a configuration line to the ```jupyter_notebook_config.py``` file that allows the Jupyter notebook to be run as the root user

![image](https://github.com/user-attachments/assets/f55dbbaa-8065-4834-b241-9fca09e7f15d)
  **Image 6: Steps to configure Jupyter Notebook within a Docker file** 

- The config lines ensure Jupyter is accessible from outside the container that it runs on port ```6004```, and that the browser doesn't auto-open
- ```RUN mkdir -p /root/.jupyter```: Creates the ```.jupyter directory``` under the root user's home directory. The ```-p``` flag ensures that the directory is created if it doesn't already exist

- ```echo "c.NotebookApp.allow_root = True"```: Allows Jupyter Notebook to run as the root user, which is often necessary when running inside a container

- ```echo "c.NotebookApp.ip = '0.0.0.0'"```: Configures Jupyter Notebook to listen on all network interfaces (not just localhost), making it accessible externally

- ```echo "c.NotebookApp.port = 6003"```: Sets the port for Jupyter Notebook to 6003 

- ```echo "c.NotebookApp.open_browser = False"```: Prevents Jupyter Notebook from trying to open a web browser automatically when it starts, which is useful for a containerized environment where there's no GUI

- ```echo "c.NotebookApp.token = ''"```: Disables the authentication token, so users don't need to provide a token to access the notebook (not recommended in production without securing it in other ways)

- ```echo "c.NotebookApp.password = ''"```: Disables password protection for the Jupyter Notebook (also not secure, but useful in a development or trusted environment)
- These commands configure Jupyter Notebook to run without authentication, on a specific port, and accessible from outside the container, making it easier to connect to from a browser

![image](https://github.com/user-attachments/assets/392fe41f-b163-4ade-99f5-fd8df6899d12)
  **Image 7: Logging level of jupyter**
- This command modifies the Jupyter Notebook configuration to set the logging level for the application
- This sets the logging level of Jupyter Notebook to ```DEBUG``` mode by adding a line to the configuration file ```(jupyter_notebook_config.py)```
- ```RUN echo "c.NotebookApp.log_level = 'DEBUG'"```: Appends the configuration to set the logging level to ```DEBUG``` in Jupyter Notebook
- The file path ```/root/.jupyter/jupyter_notebook_config.py``` refers to the configuration file for Jupyter Notebook located in the ```.jupyter``` directory within the home directory of the root user ```(/root)```

- Enhanced logging: Configuring Jupyter's logging level to ```DEBUG``` mode is useful for development. You can capture detailed logs of the Jupyter server’s activity, which can help in troubleshooting errors.

- Logs are typically written to ```stdout``` and ```stderr``` in Docker, so you can view them using:

```bash
docker logs <container_id>
```
This is especially useful when debugging startup failures or issues related to the notebook execution

- Setting Up a Password: Configure Jupyter to require a password or token, which is essential for security outside of development.

```bash
jupyter notebook password
```
 This command prompts you to set a password and creates a ```jupyter_notebook_config.json``` file under ```~/.jupyter``` with your hashed password.

- Customizing Jupyter Port: To specify a custom port, add the following to your Dockerfile’s CMD command:

```bash
# Launch Jupyter on a custom port, e.g., 6003
CMD ["jupyter", "notebook", "--port=6003", "--no-browser", "--ip=0.0.0.0"]
```
Note: The ```--ip=0.0.0.0``` flag allows Jupyter to be accessed from outside the container, while ```--no-browser``` prevents Jupyter from attempting to open a browser window inside the container.

- After installation, you can configure Jupyter by modifying the jupyter_notebook_config.py file. This file can typically be found in the ```.jupyter``` directory in home folder.

- Configuration Options:

Notebook Directory: Set the default directory for notebooks.
Password Protection: Enable password protection for enhanced security.

Example configuration:

```bash
c.NotebookApp.notebook_dir = '/path/to/your/notebooks'
c.NotebookApp.password = 'your_password_hash'
```

# Implementation

### Jupyter implementation

![image](https://github.com/user-attachments/assets/6f6efd2e-bec4-45f3-91fb-884c57415009)

  **Image 8: Jupyter implementation in docker file**
- The line ensures that JupyterLab and Jupyter Notebook are implemented in the specified Conda environment ```(team3_env).```
- This command performs several tasks in a Dockerfile to set up a Jupyter Notebook environment and install Nginx, a web server. Here’s a breakdown of the command

```bash
RUN /bin/bash -c "source ~/.bashrc && mamba install -c conda-forge jupyter"
```

- ```/bin/bash -c```: Executes the following command string in a new bash shell
- ```source ~/.bashrc```: Loads the environment settings defined in the ```.bashrc file```. This is essential to ensure that the Conda environment and any custom settings are applied before running subsequent commands
- ```mamba install -c conda-forge jupyter```: ```mamba```: A fast alternative to conda for package management, specifically designed to speed up installation processes
- ```install -c conda-forge jupyter```: Installs Jupyter Notebook from the conda-forge channel, which is a community-maintained repository for ```Conda``` packages. This command ensures that Jupyter and its dependencies are properly installed in the active ```Conda``` environment
- ```&& apt-get update && apt-get install -y nginx```: ```&&```: Ensures that the next command only runs if the previous command was successful
- ```apt-get update```: Updates the package list for the Advanced Package Tool (APT), allowing the installation of the latest versions of packages and their dependencies
- ```apt-get install -y nginx```:
- ```install -y```: Installs the Nginx web server without prompting for confirmation (the ```-y``` flag automatically answers "yes" to any prompts)
- ```nginx```: The name of the package being installed, which is a popular open-source web server known for its high performance and scalability

![image](https://github.com/user-attachments/assets/10c525cb-e571-4c8a-8ffb-f3fcddf11348)

**Image 9: Steps to setup Jupyter Notebook**
- These steps collectively set up Jupyter notebook within a conda environment in the docker container
- This Dockerfile snippet outlines several commands to set up a Conda environment with Jupyter Notebook and Nginx

1. ### Installing Jupyter and IPython Kernel

- To install Jupyter and IPython kernel, add this to Dockerfile:

```bash
RUN /bin/bash -c "source ~/.bashrc && mamba install -c conda-forge jupyter ipykernel"
```

- ```/bin/bash -c```: Executes the command within a new bash shell.
- ```source ~/.bashrc```: Loads the user's Bash configuration to ensure that the ```Conda``` environment is activated properly
- ```mamba install -c conda-forge jupyter ipykernel```: Installs both Jupyter Notebook and the IPython kernel (needed to run Python code in Jupyter) from the conda-forge channel. Mamba is used for faster package management

2. ### Installing the kernel for the environment

```bash
RUN /root/miniconda3/envs/team3_env/bin/python -m ipykernel install --name team3_env --display-name "Python (team3_env)"
```

- ```/root/miniconda3/envs/team3_env/bin/python```: Specifies the Python interpreter from the ```team3_env``` Conda environment

- ```m ipykernel install```: Uses the ipykernel module to install the IPython kernel

- ```--name team3_env```: Sets the kernel name to ```team3_env```, which will be used internally

- ```--display-name "Python (team3_env)"```: Sets the display name that will appear in the Jupyter Notebook interface. This helps users easily identify the correct kernel to use when running notebooks

- Expose the necessary ports in Dockerfile:

```bash
EXPOSE 6003
```
- Launching Jupyter:

```bash
jupyter notebook
```
Set the default command to run Jupyter:

```bash
CMD ["jupyter", "notebook", "--port=6003", "--no-browser", "--ip=0.0.0.0"]
```

3. ### Installing Nginx

```bash
RUN apt-get update && apt-get install -y nginx
```
- ```apt-get update```: Updates the package list for APT, ensuring that you can install the latest available packages.
- ```apt-get install -y nginx```: Installs the Nginx web server without prompting for confirmation. Nginx is often used to serve web content and can act as a reverse proxy for Jupyter Notebook

4.
 ```bash
RUN /bin/bash -c "source ~/.bashrc && mamba install -c conda-forge jupyter" \
    && apt-get update && apt-get install -y nginx
```

- This line repeats the installation of Jupyter Notebook using Mamba and updates and installs Nginx again

5. Here’s a snippet to add Jupyter with security and port configuration:

```bash
# Install Jupyter
RUN pip install jupyter

#Set up Jupyter notebook with password and port
COPY jupyter_notebook_config.json /root/.jupyter/jupyter_notebook_config.json
EXPOSE 6003

# Default command to run Jupyter Notebook
CMD ["jupyter", "notebook", "--port=6003", "--no-browser", "--ip=0.0.0.0"]
```

6. Port mapping: To make Jupyter accessible on a different port outside the container, use Docker’s `-p` flag

```bash
docker run -d -p 5003:5003 -p 6003:6003 pavankunchala/team3-app
```

7. Using Jupyter in Docker: 

Launching the Jupyter Container: Run the Docker container with Jupyter using:

```bash
docker run -d -p 5003:5003 -p 6003:6003 pavankunchala/team3-app
```

- Accessing Jupyter: After running the container, access Jupyter by navigating to http://localhost:6003 on your host machine. 


##
###

# Usage

**Usage of Jupyter for the documentation of Swebok chatbot:**
- Jupyter documentation is a comprehensive guide for the SWEBOK textbook chatbot, providing clear, structured documentation.
- The notebook serves as both a development environment and a documentation resource, integrating code, explanatory markdown, and interactive elements to demonstrate the chatbot's workflow. 
- The documentation is organized into the following sections:

1. Introduction

Purpose:
- Provides an overview of the chatbot project.
- Explains its educational goal of querying SWEBOK content.
- Describes the use of Mistral 7B and the Retrieval-Augmented Generation (RAG) approach
![image](https://github.com/user-attachments/assets/0c5e4a17-4c4e-48e1-b032-fb4391e83d6d)

2. Setup
- Details the installation of dependencies like LangChain and FAISS.
- Specifies environment requirements, including Python version and essential libraries.
- Prepares the development environment by loading necessary configurations.

3. Building the Chatbot
- Document Loading: Explains how to load SWEBOK documents as the chatbot's corpus using Python scripts.
- Embeddings: Outlines the process of generating vector embeddings using Alibaba’s HuggingFace embedding model.
- FAISS Vector Store: Details the storage and retrieval system for embedding vectors to enhance query efficiency.

4. Improvement of chatbot with Inference
- Helper Functions: Introduces similarity search and response generation methods for efficiently retrieving context-relevant information.
- Prompt Engineering: Defines a structured system prompt for the chatbot to guide its behavior and response generation.

5. Testing the Chatbot
- Demonstrates the integration of interactive widgets to test user queries directly within the Jupyter Notebook.
- Highlights the ability to refine and debug chatbot interactions interactively.
![image](https://github.com/user-attachments/assets/0e2ee321-2ed8-4929-974c-ccb82b9b5118)

6. Conclusion
- Summarizes the steps taken to develop, test, and enhance the chatbot.









##
###

# Troubleshooting

## Common Issues and Troubleshooting Steps

- If you encounter issues while using Jupyter, consider the following troubleshooting tips:

1. ### Jupyter notebook not starting
  If Jupyter Notebook fails to start, there are several possible causes. Here are some troubleshooting steps:

- Check logs: Review the terminal output when starting the container for any error messages related to Jupyter
- Verify CMD: Ensure that the command to start Jupyter Notebook is correctly specified in the Dockerfile

![image](https://github.com/user-attachments/assets/55d2b9ed-fb17-43d9-a99e-75a7e7643f87)

 **Image 12: Start NGINX, Streamlit, and Jupyter with Port Verification for Jupyter**

- Ensure this command specified to start Jupyter Notebook is correct, confirm that:

- ```Nginx``` is starting successfully before the Streamlit app and Jupyter Notebook

- ```Streamlit``` is not blocking the execution of Jupyter Notebook. The command runs sequentially, so if the Streamlit app encounters an issue, it may prevent Jupyter from starting

- The options used for Jupyter Notebook ```--ip=0.0.0.0, --port=6003, --no-browser, --allow-root``` are appropriate for your container setup


2. ### Unable to access Jupyter in browser
   If you cannot access Jupyter Notebook from your browser, try the following steps:

- Check port exposure: Ensure that port ```6003``` is exposed and mapped correctly in your Docker run command
- Firewall settings: Ensure that no firewall rules are blocking access to port ```6003```
- IP address: Verify that you are using the correct IP address (or localhost if running locally)

3. ### Kernel not starting
- Check installed kernels: Ensure that the necessary Python kernel is installed in the Conda environment. You can install it using:
```bash
mamba install ipykernel
```
- Recreate kernel: If there are issues with the existing kernel, recreate it:

![image](https://github.com/user-attachments/assets/cedc90dd-e428-401e-a084-6c993ee1e662)
**Image 13: Check kernel**

```bash
pip install ipykernel
python -m ipykernel install --user --name=your_env_name
```
- This line creates and installs a new Jupyter kernel for the ```team3_env``` Conda environment, allowing users to select it in Jupyter Notebook as ```Python (team3_env)``` 
- This ensures that the correct environment and dependencies are used when running Python code in Jupyter

4. ### Package installation errors
- Requirements file: Ensure the ```requirements.txt``` file is present and correctly specified. Any missing packages might lead to runtime errors.
- Dependency conflicts: Check for any dependency conflicts in the installed packages. Consider specifying compatible versions in the ```requirements.txt```

5. ### Configuration issues
- Jupyter config file: If Jupyter fails to start with the desired configurations, check the generated configuration file at for any misconfigurations.
```bash
/root/.jupyter/jupyter_notebook_config.py
``` 
- Re-generate configuration: If necessary, re-generate the Jupyter configuration and ensure it contains the correct settings.

6. Runtime errors and kernel failures:

- Occasionally, kernel failures may arise due to misconfigured environments or missing dependencies. 
- Installing ipykernel properly, as discussed, mitigates some of these issues, but it’s important to monitor logs for errors related to the kernel.
- If you're running into issues where the kernel is not starting, manually checking the installed kernels within Jupyter's interface can help ensure that the right environment is active

7. Docker image optimization
- Image size reduction: Reducing the Docker image size can help speed up deployment and minimize resource usage. After package installation, use the following to clean up unnecessary files:

```bash
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
```
8. Layer caching: Docker caches image layers, so ordering commands logically (e.g., placing ```COPY requirements.txt``` before ```RUN pip install```) ensures that layers don't need to be rebuilt unless something changes.

9. Container rebuild: If Jupyter changes aren’t reflected after modifying the Dockerfile, rebuild the image:

```bash
docker build -t team3-app .
```

10.Port conflicts: If the port is already in use on your host, change the host port:

```bash
docker run -d -p 5003:5003 -p 6003:6003 pavankunchala/team3-app
```

11.Error logs: For troubleshooting specific issues, check Docker container logs:

```bash 
docker logs <container_id>
```

12. File persistence: If files within Jupyter are not saving or accessible, use Docker volumes to map directories:

```bash
docker run -v $(pwd):/app -p 6003:6003 <image_name>
```
13. Notebook Not Found: Double-check the directory from which you launched Jupyter Notebook.

14. FAQs:

- How do I reset my Jupyter Notebook? Restart the kernel from the menu: ```Kernel -> Restart```.

- Can I share my notebooks? Yes, you can share your notebooks by exporting them as ```HTML``` or ```PDF``` from the File menu.

- Quick fixes 

```bash
- **Container Not Starting**: Ensure your Docker daemon is running and accessible.
- **Port in Use**: If port 8888 is in use, specify another port with `-p 8889:8888`.
```

##
###



