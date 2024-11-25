# Mamba Dockerfile Documentation

## Table of Contents
1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Implementation](#implementation)
4. [Usage](#usage)
5. [Troubleshooting](#troubleshooting)

## Installation
### Base Image
The Dockerfile begins by specifying the base image, which acts as the foundation for your containerized environment. In this case, the base image is `python:3.11-slim`. This lightweight image provides a minimal environment for Python 3.11, ensuring efficient resource usage while including only essential components needed for running Python applications.
```
FROM python:3.11-slim
```
![image](https://github.com/user-attachments/assets/189b3dc7-90bb-44b9-9d2e-2c17ce27be68)

*Figure 1: Base image selection using python:3.10-slim in the Dockerfile.*

Why Choose Python 3.11-Slim?
### Why Choose Python 3.11-Slim?

Using the slim variant of Python as a base image is an excellent choice for production-ready Docker containers. Here's why:

**Minimized Image Size:** The slim version of Python is stripped down to the bare essentials, making it significantly smaller than the standard Python images. This reduction in size results in faster image builds, quicker pulls from container registries, and lower overall storage consumption. A smaller image size also enhances the speed of container startups, contributing to improved application responsiveness.

**Security Considerations:** By starting with a minimal image, you reduce the attack surface since it has fewer system packages. Fewer installed components mean fewer vulnerabilities to patch or update, making it easier to maintain security compliance. Additionally, it simplifies the process of scanning for vulnerabilities, allowing for a more streamlined security review.

**Customizability:** The slim image allows you to install only what you need. Instead of using a bloated image with unnecessary dependencies, you can precisely control the software stack, ensuring the Docker container has only what's necessary for your project. This customizability not only optimizes performance but also reduces potential conflicts between packages, enhancing the stability of your application.

By choosing this minimal image, you're preparing your application for an efficient and lean deployment environment, which is especially critical in production and resource-constrained cloud environments. Leveraging the slim variant of Python sets the stage for a more manageable and scalable application infrastructure, aligning with modern best practices in containerization.

### System Dependencies
After specifying the base image, the Dockerfile installs necessary system dependencies before proceeding to Mamba’s installation. These dependencies help ensure the system has the necessary tools to download and install the Mambaforge environment and other required software.
```
RUN apt-get update && apt-get install -y \
    wget \
    bzip2 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
```
![image](https://github.com/user-attachments/assets/cb518795-57e0-4f97-a3f3-068b725dac15)

*Figure 2: Installation of system dependencies using apt-get in the Dockerfile.*

Explanation:
apt-get update: This command updates the package list for the apt-get package manager, ensuring that the latest versions of packages are available.

apt-get install -y: This installs the listed packages. The -y flag ensures that the command runs non-interactively (without waiting for user confirmation).

wget: wget is a non-interactive network downloader. It is a key tool in downloading files from external URLs, which in this case is used to fetch the Mambaforge installation script.

bzip2: This compression utility is used for extracting files. It's often required when handling compressed archives downloaded during the installation process.

ca-certificates: These certificates ensure that secure HTTPS connections can be established when downloading external resources like Mambaforge.

Cleanup: The rm -rf /var/lib/apt/lists/* command clears out the apt-get cache to minimize the size of the Docker image. After installing the necessary packages, there's no need to retain the package lists, which can save space and improve the efficiency of the Docker build.

By only installing essential packages and removing unnecessary data, the Dockerfile ensures a lightweight container that's quick to deploy and secure.

### Mambaforge Installation
Mamba is a high-performance drop-in replacement for Conda. The Dockerfile includes instructions to download and install Mambaforge, a pre-built distribution that includes Mamba as well as the core Conda package management tools. Mamba offers faster environment solving and better performance than Conda, making it ideal for production use.

The installation steps are dynamic, detecting the system's architecture and installing the appropriate version of Mambaforge.
```
RUN arch=$(uname -m) && \
    if [ "${arch}" = "x86_64" ]; then \
        wget -q "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh" -O miniforge.sh; \
    elif [ "${arch}" = "aarch64" ]; then \
        wget -q "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh" -O miniforge.sh; \
    else \
        echo "Unsupported architecture: ${arch}"; \
        exit 1; \
    fi && \
    bash miniforge.sh -b -p /opt/miniforge && \
    rm miniforge.sh
 ```
![image](https://github.com/user-attachments/assets/db8207fc-cd87-4795-95d0-8bf34b1bc076)
*Figure 3: Dynamic installation of Mambaforge based on system architecture (x86_64 or aarch64) in the Dockerfile.*

Explanation:
Architecture Detection: The script dynamically checks the architecture of the system using the uname -m command. It then uses conditional logic to download the correct version of Mambaforge, depending on whether the system is x86_64 (64-bit architecture for Intel/AMD CPUs) or aarch64 (64-bit ARM architecture, often found in Raspberry Pi or some cloud servers).

Downloading Mambaforge: The wget command downloads the latest version of Mambaforge from the official GitHub releases page. The installation script is saved as miniforge.sh.
Installing Mambaforge: The bash miniforge.sh -b -p /opt/miniforge command runs the installer script in batch mode (-b), meaning that it doesn’t prompt for user input, and installs Mambaforge into the /opt/miniforge directory.

Cleanup: After installation, the script is removed to save space. This is a crucial step in Dockerfile best practices, as leaving unnecessary files (like installation scripts) increases the image size unnecessarily.
Mambaforge, once installed, provides an optimized environment manager, capable of creating Python environments, installing packages, and running applications efficiently.

# Configuration

### Environment Variables
The Dockerfile sets several environment variables that optimize the behavior of Python, the package manager, and the build process itself. These environment variables ensure smoother execution and reduce the overhead during container setup.

```
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
```
![image](https://github.com/user-attachments/assets/0de11157-f18a-40f2-b183-ea5ca6ec6474)

*Figure 4: Dockerfile setting environment variables to optimize Python behavior and reduce overhead during container setup.*

Explanation:
DEBIAN_FRONTEND=noninteractive: This environment variable ensures that the apt-get package manager runs in a non-interactive mode. In a Docker build context, interactive prompts are not ideal because there is no user to provide input. Setting this variable avoids interruptions during the build process, making it smooth and automated.

PYTHONUNBUFFERED=1: By default, Python buffers its output, which can be problematic in Docker environments when you need real-time logging. Setting PYTHONUNBUFFERED=1 forces Python to flush its output directly to the terminal without buffering. This is crucial for log visibility, especially in debugging or production environments where real-time log feedback is necessary.

PYTHONDONTWRITEBYTECODE=1: This variable prevents Python from generating .pyc files, which are compiled bytecode files. While .pyc files can improve performance in some cases, they take up disk space and aren't necessary in many containerized environments where the focus is on minimizing the image size and complexity.
Together, these environment variables streamline the build process, ensure smooth Python execution, and keep the Docker image lightweight.

### Environment Setup
After Mambaforge has been installed, the Dockerfile creates a dedicated Python environment named team3_env, which isolates the project’s dependencies from the base system. Using isolated environments like this is critical for preventing conflicts between different projects' dependencies.
```
RUN mamba create -n team3_env python=3.11 -y
```
![image](https://github.com/user-attachments/assets/cdba9c4e-fa9a-4737-8053-2a3ecab81d3f)

*Figure 5: Creating a dedicated Python environment, "team3_env", using Mamba to ensure isolated project dependencies in the Dockerfile.*


### Why Use an Isolated Environment?

In Python, package dependency conflicts are a common issue, particularly in large projects or when using multiple projects on the same system. By creating a dedicated environment for each project using tools like Mamba or Conda, you ensure that:

**Dependencies are isolated:** The environment keeps all installed packages separate from the base Python installation, effectively preventing version conflicts that can lead to runtime errors. This isolation simplifies the management of various dependencies, allowing developers to work on multiple projects without interference from conflicting package versions.

**Portability:** Since the environment includes all required dependencies, the application can be easily moved between systems without having to worry about different versions of libraries. This is particularly beneficial for teams collaborating across different platforms or for deploying applications in various environments, as the containerized setup provides a consistent runtime.

**Reproducibility:** When sharing code, other developers or automated systems, such as Continuous Integration (CI) services, can recreate the same environment with exact dependencies, ensuring that code runs consistently across different systems. This reproducibility is crucial for testing and validation, as it reduces the likelihood of "it works on my machine" scenarios, fostering a more reliable development workflow.

**Ease of Maintenance:** Managing dependencies within a dedicated environment makes it easier to update, remove, or add new packages without affecting other projects. This ensures that the project remains maintainable over time, allowing for smoother upgrades to newer versions of libraries while avoiding compatibility issues.

By leveraging environment management tools, developers can create a more robust and organized development ecosystem, ultimately leading to better software quality and a more efficient development process.

### Adding Conda Environment to PATH
To ensure that the executables from the team3_env environment are accessible system-wide, the Dockerfile modifies the system’s PATH variable to include the environment's bin directory.
```
ENV PATH=/opt/miniforge/envs/team3_env/bin:$PATH
```
![image](https://github.com/user-attachments/assets/e3723d8d-275b-4db7-b0d5-b3b77175d282)

*Figure 6: Adding team3_env's bin directory to the system PATH for global access to executables.*

Why is this important?
By adding the environment’s bin directory to PATH, you make it possible to execute commands like python, pip, or streamlit without specifying their full paths. This simplifies running your application and ensures that the correct versions of Python and other tools from the environment are used.

For example, without this line, you might have to run the application using the full path to Python:
```
/opt/miniforge/envs/team3_env/bin/python app.py
```
With the PATH modification, you can simply run:
```
python app.py
```
![image](https://github.com/user-attachments/assets/36681681-f285-4892-a8fc-b1ba81f885bd)

*Figure 7: Simplified command execution due to PATH modification, making Python accessible globally within the container.*

This small change significantly improves usability and reduces the chance of errors when running commands inside the container.

# Implementation

### Setting Up Environment
After installing Mambaforge and setting up the Python environment, the Dockerfile creates a new environment with Python 3.11.
```
RUN mamba create -n team3_env python=3.11 -y
```
![image](https://github.com/user-attachments/assets/ad5af895-c241-4cce-a0bc-0f3c90ccad41)

*Figure 8: Creation of a new isolated environment using Mambaforge with Python 3.11 to prevent dependency conflicts.*


This step is crucial to create an isolated environment, ensuring that the application and its dependencies are kept separate from the system-wide Python installation. This isolation reduces the risk of version conflicts and ensures that the environment can be reproduced across different machines.

### Installing Dependencies
Once the environment is created, the Dockerfile installs the Python dependencies specified in requirements.txt using Mamba.
```
COPY requirements.txt /app/requirements.txt
RUN mamba install --yes --file requirements.txt && mamba clean --all -f -y
```
![image](https://github.com/user-attachments/assets/72fc043d-c85e-4ab3-b10b-24a40396eb2c)
*Figure 9: Installation of Python dependencies from requirements.txt using Mamba to streamline package management.*


Why Use Mamba for Dependency Management?
Speed: Mamba is much faster than Conda when it comes to solving dependencies. For large projects with many dependencies, Mamba can resolve conflicts and install packages significantly faster than Conda.

Efficiency: Mamba optimizes the installation process by parallelizing the download and installation of packages, reducing the overall time to build the Docker image.

Cleaning: After installing the packages, the command mamba clean --all -f -y cleans up the package cache, reducing the size of the Docker image. This is a best practice in Docker image creation, as it ensures that the final image is as small and efficient as possible.

By using Mamba for dependency management, the Dockerfile speeds up the image-building process and reduces the chance of dependency conflicts.

# Usage

### Building the Docker Image
To build the Docker image, use the following command:
```
docker build -t team3-app .
```
![image](https://github.com/user-attachments/assets/e6db678d-c15c-4193-b0d7-d390a1815a13)
*Figure 10: Command to build the Docker image named team3-app from the Dockerfile.*


This command reads the instructions from the Dockerfile and creates an image named team3-app. Building a Docker image involves several steps, including:

Downloading the base image (python:3.11-slim).
Installing system dependencies (such as wget, bzip2, etc.).
Downloading and installing Mambaforge.
Setting up the Python environment and installing the necessary Python packages from requirements.txt.
Once the image is built, you have a fully contained, ready-to-run version of your application that can be deployed anywhere Docker is supported.

Why Is Containerization Important?

Portability: Docker images encapsulate all the software, libraries, and dependencies needed to run your application. This means you can move the container across different systems or cloud environments without worrying about compatibility issues.

Consistency: With Docker, the environment your application runs in is the same from development to production. This eliminates the classic "it works on my machine" problem, as the container ensures a consistent runtime environment.

Scalability: Docker makes it easy to scale applications by running multiple instances of the same container across different servers or cloud nodes.

By containerizing your application, you make it easier to deploy, scale, and maintain, particularly in complex production environments.

### Running the Container
After building the Docker image, you can run the container using the following command:
```
docker run -d -p 5003:5003 team3-app
```
![image](https://github.com/user-attachments/assets/9c10a760-6232-4588-92b6-6d7bb4359a55)
*Figure 11: Command to run the Docker container in detached mode, mapping port 5003 of the host to port 5003 of the container.*


Explanation:
docker run: This command starts a new container from the Docker image.
-d: The -d flag runs the container in detached mode, meaning it runs in the background, allowing you to continue using your terminal while the container runs.

-p 5003:5003: This flag maps port 5003 on the host machine to port 5003 inside the container. This is particularly important for web applications like Streamlit, which serve content over HTTP. By exposing and mapping this port, you make the application accessible from the host system.

With this command, the container starts, and your application becomes accessible at http://localhost:5003.
### Exposed Ports
To ensure that the application can be accessed from outside the container, the Dockerfile includes an EXPOSE instruction:
```
EXPOSE 5003
```
This instruction makes port 5003 available for external connections. Although EXPOSE does not automatically map the port to the host system, it documents which port the application is running on and makes it possible to bind this port to the host when running the container.

In this case, port 5003 is used for the Streamlit application.

# Troubleshooting

### Unsupported Architecture Error
If the system's architecture is neither x86_64 nor aarch64, the Dockerfile will exit with an error. This occurs because the Dockerfile is explicitly designed to handle only two architectures. To troubleshoot this issue:

Run 'uname -m' on your system to determine the architecture.
If your architecture isn’t supported, check whether a compatible version of Mambaforge exists, or consider using an alternative toolchain that supports your system’s architecture.
In cases where an unsupported architecture is detected, you may need to modify the Dockerfile to include a compatible Mambaforge installation for your system.

### Dependency Issues
One common issue when building Docker containers is dependency resolution failures. This can occur if:

There are conflicting versions of packages in requirements.txt.
The requirements.txt file includes packages that aren’t available on Conda-Forge.
To resolve dependency issues:

Check requirements.txt for conflicting package versions.
Manually search for the packages using mamba search <package_name> to verify that they exist in the Conda-Forge repository.
If conflicts are detected, you may need to adjust the versions specified in requirements.txt to ensure compatibility.

### Package Installation Failures
If certain packages fail to install, the issue may be related to package availability on Conda-Forge. To troubleshoot this issue:

Use the mamba search <package_name> command to check whether the package exists in the Conda-Forge repository.
If the package isn’t available, consider finding an alternative package or source the package from a different repository.
Package installation failures can often be resolved by adjusting requirements.txt or switching to an alternative package management strategy.

### Streamlit Not Running
If the Streamlit application doesn’t start or isn’t accessible, there are several potential issues to check:

Port Mapping: Ensure that port 5003 is correctly exposed and mapped in both the Dockerfile (EXPOSE 5003) and the docker run command (-p 5003:5003).

Streamlit Configuration: Check the Streamlit configuration to verify that it’s set to run on port 5003. Misconfigurations in the config.toml or other configuration files can prevent Streamlit from running on the correct port.
Viewing Logs: Use the following command to check the logs for any errors that might be preventing Streamlit from running:
```
docker logs <container_id>
```
The logs will provide detailed error messages if Streamlit isn’t running properly, helping you diagnose the issue.

