This wiki provides guide to setting up and running nemo guardrails inside the docker contatiner

For your textbook chatbot project, you can explore how to use NeMo Guardrails to enhance the chatbot's capabilities. Here's a summary of how to integrate it into your GitHub project

# Table of Contents
1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Implementation](#implementation)
4. [Usage](#usage)
5. [Troubleshooting](#troubleshooting)
---

## Installation
### Prerequisites:
Our Docker container's base image is ```Python 3.11-slim```. Specifically designed for reduced sizes and quicker performance, this lightweight image is based on the official Python images.
```bash
FROM python:3.12-slim
ENV DEBIAN_FRONTEND=noninteractive
```
<img width="492" alt="Screenshot 2024-10-13 at 12 36 36 PM" src="https://github.com/user-attachments/assets/4297fe70-e356-4da7-8596-b7051445f329">

**Figure 1: The base image python:3.11-slim used for the Docker container.**

**Advantages of Using a Slim Base image**
- **Efficiency:** Pulling an image from a container registry takes less time since slim pictures are far smaller than their full-sized equivalents. Build times are crucial in continuous integration/continuous deployment (CI/CD) pipelines, where this is very helpful. In cloud systems, a reduced picture size might result in cost savings because it not only speeds up the initial draw but also lowers overall storage needs. Additionally, development agility is improved by the faster transmission of smaller pictures across environments.

- **Security:** Vulnerabilities are less likely when a thin image has fewer packages. It is simpler to manage security fixes when there are fewer possible security vulnerabilities due to a smaller attack surface. The probability of running into security flaws is also reduced by reducing the amount of dependencies and components. Teams may maintain a stronger security posture throughout the application lifetime by focusing on key components, which makes auditing and compliance procedures easier.

- **Speed of Deployment:** For applications that need to scale quickly in cloud settings, containers based on thin images start up more quickly than those based on bigger images. Quicker container provisioning and more effective resource use are made possible by the lower overhead. For serverless apps and microservices architectures, where responsiveness and agility are essential, this quick deployment feature is essential. Additionally, because apps can react to requests more quickly, quicker startup times might result in better user experiences.

- **Simplicity and Maintainability:** Because slim base images only include the components required to execute applications, they encourage a simpler design. The development process is streamlined by this simplicity, which also makes maintaining the graphics simpler. Without the extra hassle of superfluous packages, developers can concentrate on the essential features of their apps. New team members can swiftly grasp the application's structure and dependencies without having to sift through unnecessary material, which results in better documentation and faster onboarding.

- **Consistency:** It is possible to maintain consistency between the development and production environments by using thin base images. Slim images reduce inconsistencies that could result from extra software or dependencies found in bigger images since they are intended to contain just the most necessary packages. Developers may spend more time creating features and less time resolving deployment problems because of this consistency, which lowers the possibility of running into environment-specific defects.

To check if Git is installed on your system and to confirm its version, you can run the following command in the terminal.
```bash
git --version
```
<img width="564" alt="Screenshot 2024-10-11 at 1 37 22 PM" src="https://github.com/user-attachments/assets/1768f3ec-48d5-49a0-9650-393cff8b0052">

**Figure 2: Git Installation**

### Steps:
Clone the project repository:
```bash
git clone https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3.git
```
<img width="570" alt="Screenshot 2024-10-13 at 12 41 02 PM" src="https://github.com/user-attachments/assets/a9b0d752-9f20-4fe3-af37-f5dcd79317c4">

**Figure 3: Cloning the git repository**

Install the required dependencies: 
```bash
RUN apt-get update && apt-get install -y \
	wget \
	bzip2 \
	ca-certificates \
	build-essential \
	cmake \
	&& rm -rf /var/lib/apt/lists/*
```
<img width="502" alt="Screenshot 2024-10-13 at 12 42 36 PM" src="https://github.com/user-attachments/assets/91f12937-bc91-4284-9a7f-ac53e566b09c">

**Figure 4: Installing system dependencies using apt-get in the Docker container.**

**apt-get update && apt-get install**
- **Apt-get update:** The list of available packages and their versions is updated by this command using the system's specified repositories. To make sure you are obtaining the most recent versions of the packages accessible in the repositories, it is imperative that you use this command prior to installing any packages. A speedier installation procedure and fewer possible conflicts with already installed software are ensured by retrieving the most recent package information, which also helps avoid problems that might result from out-of-date dependencies. You may also keep up with any security updates and improvements for the packages you use by using this command on a frequent basis.
- **Apt-get install -y wget:** The -y option ensures that the command runs without human intervention by automatically responding "yes" to any prompts during installation. For automated programs where user contact is impractical, this is very helpful. With support for HTTP, HTTPS, and FTP protocols, wget is a tool for getting files from the internet. It is a vital tool for retrieving files needed for your application or environment setup since it is frequently used to get datasets or other resources during the build process. Wget is flexible for effectively downloading complicated file structures or big datasets since it can also manage recursive downloads and restart interrupted downloads.


We install the NeMo toolkit and all of its dependencies once the base image and system requirements are set up:
```bash
pip3 install 'nemo_toolkit[all]'
```
<img width="570" alt="Screenshot 2024-10-13 at 12 44 52 PM" src="https://github.com/user-attachments/assets/42617976-5a45-4fac-9e5c-5ef3aad40088">

**Figure 5: Installing the NeMo toolkit and its dependencies using pip.**

**How to Use the NeMo Toolkit:**

**What is NeMo?**
- NVIDIA created the open-source NeMo (NVIDIA Neural Modules) toolbox, which offers parts for creating conversational AI models. It is appropriate for a number of applications, such as text-to-speech synthesis, natural language processing (NLP), and voice recognition, since it makes it simple for users to create, train, and implement models.

**Why is NeMo Beneficial?**
- Because of NeMo's modular architecture, users may build sophisticated models without having to start from scratch by combining different parts, such encoders and decoders. Users may save a significant amount of time and computing resources by fine-tuning the pre-trained models included in the toolbox for their particular applications.

## Configuration
Once the required software has been installed, we must set up our environment for best performance. Setting up environment variables that NeMo Guardrails will use during runtime is one of the initial tasks.
``` bash
ENV NEMO_DATA_PATH=/data
```
<img width="391" alt="Screenshot 2024-10-13 at 1 17 15 PM" src="https://github.com/user-attachments/assets/8f50a4f5-1e24-484d-9ed8-f658ed9c12f7">

**Figure 6: Setting environment variables for NeMo, specifying the data path.**

**Importance of Environment Variables**

**NEMO_DATA_PATH:** This variable specifies the path where the data used by NeMo will be stored. By setting this variable, you help the toolkit locate the necessary datasets and files during model training and evaluation.

**Additional Environment Variables**
In addition to NEMO_DATA_PATH, you might want to define additional environment variables that can enhance the configuration:
```bash
ENV NEMO_MODEL_PATH=/models
ENV NEMO_LOG_LEVEL=INFO
```

- **ENV NEMO_MODEL_PATH:** The directory from which trained models can be loaded or saved is indicated by the variable NEMO_MODEL_PATH. This division facilitates the management of model files by keeping your container's structure orderly.
- **NEMO_LOG_LEVEL:** This option regulates how verbose the logs generated by NeMo are. You may get comprehensive logging information while it's running by setting it to ```INFO```, which is useful for troubleshooting and monitoring.

### Optional Configuration

Think about adding more environment variables for hardware utilization and performance customization to further improve the container. For instance, if your program calls for it, you may wish to put up memory management settings or GPU settings.

```bash
ENV CUDA_VISIBLE_DEVICES=0
```
**CUDA Variable**

- **CUDA_VISIBLE_DEVICES:** The GPUs that the program executing in the container may access are controlled by this variable. You may make sure your program makes use of the host computer's GPU resources by setting this variable.

## Implementation
Effective file and resource management requires a clearly defined directory structure. To arrange data and application code, we establish the required folders.

```bash
RUN mkdir -p /data /app
```
<img width="508" alt="Screenshot 2024-10-13 at 1 21 48 PM" src="https://github.com/user-attachments/assets/0c904993-af28-4dd8-b91e-faf8bde6a8e3">

**Figure 7: Creating a structured directory layout for data and application code.**

**Benefits of a Structured Directory Layout**

- **Clarity:** Clarity is maintained by grouping files into designated folders, particularly when the quantity of information and resources increases. Developers and operators can find the required files more easily and rapidly as a result.
- **Scalability:** The project may grow with a well-designed directory structure. New features or datasets may be added as your project develops without interfering with the current structure.
- **Maintainability:** Errors during development or deployment are less likely when files are maintained and updated with ease thanks to a clear directory structure.

Copy Configuration Files If you have configuration files for NeMo Guardrails, copy them into the container:
```bash
COPY config.yaml /app/config.yaml
````
<img width="581" alt="Screenshot 2024-10-13 at 1 28 34 PM" src="https://github.com/user-attachments/assets/0369f0c1-9913-406e-99e2-e11fbcfa2b43">

**Figure 8: Copying configuration files into the container for NeMo.**

**Why Use Configuration Files?**
- **Flexibility:** Configuration files allow you to easily change settings without modifying the application code. This separation of configuration from code enhances flexibility and maintainability.
- **Version Control:** Keeping configuration files in version control enables tracking of changes over time, making it easier to revert to previous settings if necessary.

**Explanation of Configuration Parameters**

- **model.type:** Specifies the type of model being used. In this case, it is an Automatic Speech Recognition (ASR) model.
- **model.params:** Contains parameters specific to the model. For example, ```sample_rate``` sets the audio sample rate, and ```num_classes``` defines the number of output classes for the model's predictions.
## Usage
### Running NeMo Guardrails

Using NeMo Guardrails Depending on the model and job, use a command similar to the one below to launch NeMo Guardrails.
```bash
python -m nemo.collections.asr.models.automatic_speech_recognition --config-path /app/config.yaml
```
<img width="862" alt="Screenshot 2024-10-13 at 1 32 21 PM" src="https://github.com/user-attachments/assets/56db7bd9-0378-41a1-a8cf-9c2b286736de">

**Figure 9: Running Nemo guardrails using python.**

**Understanding the Execution Command**
- **-m:** This flag instructs Python to run a module as a script. The specified module is the ASR model within the NeMo toolkit.
- **--config-path:** This argument allows you to specify the path to your configuration file, ensuring that NeMo has all the necessary parameters to execute your task effectively.

### Ports
To allow communication between your application and external systems, it's essential to expose the necessary ports. If you are running a server or API, include the following command:
```bash
Expose 5003
```
<img width="570" alt="Screenshot 2024-10-13 at 1 38 03 PM" src="https://github.com/user-attachments/assets/bd75b9d3-2d47-4ed6-b3c6-1910eb2f44c8">

**Figure 10: Exposing port 5003 for external access to the application.**

**Why Expose Ports?**

- **Client Access:** Exposing ports allows external clients to communicate with the application running inside the container. This is especially important for web applications or APIs that need to interact with other services.
- **Documentation:** The EXPOSE command serves as a form of documentation, indicating which ports are intended to be published when the container is run. This can be helpful for users or developers working with the container.

### Launching the Program To use Python to run your application

<img width="523" alt="Screenshot 2024-10-13 at 1 40 23 PM" src="https://github.com/user-attachments/assets/aa3d324e-36b2-4122-842e-bd447662849a">

**Figure 11: Setting the default command for the container to run the ASR model.**

**Explanation of ENTRYPOINT and CMD**

- **ENTRYPOINT:** This command defines the primary executable that will run when the container starts. In this case, we set it to python, ensuring that the Python interpreter is always used to run our application.
- **CMD:** This command specifies the default parameters for the ENTRYPOINT. Here, we set app.py as the default script to run, which can be overridden at runtime if needed.

### Running the Container

To run the container based on your Dockerfile, use the following command:

```bash
docker run -it --rm -p 5003:5003 team3-app
```

**Explanation of the Run Command**
- **-it:** This flag runs the container in interactive mode, allowing you to interact with it directly through the terminal.
- **--rm:** This option automatically removes the container when it exits, which is useful for keeping your environment clean, especially during development.
- **-p 5003:5003:** This option maps port 5003 on the host machine to port 5003 on the container, enabling external access to any services running on that port inside the container.
# Troubleshooting
- NeMo Installation Issues
If you encounter issues with the installation of NeMo, it's essential to check for package conflicts and permissions. Use the following command to verify package dependencies:
```bash
pip check
```
**Understanding pip check**

- **pip check:** This command checks the installed packages for dependencies that are not satisfied. It helps identify any package conflicts that may prevent NeMo from functioning correctly.

### Testing Installed Libraries

To verify that NeMo is correctly installed, enter the container and attempt to import the library:

Examining the Installed Libraries Import the library and access the container to confirm that NeMo is installed correctly:
```bash
docker exec -it <container_name> /bin/bash
python -c "import nemo"
```
**Why Testing the Installation is Important**

- **Verification:** Verifying that the library imports successfully guarantees that no essential dependencies are missing and that the installation was successful.

- **Immediate Feedback:** You can debug the installation before launching the application since you get quick feedback if the import fails.

### Troubleshooting Steps

If you encounter issues while running your application, consider the following steps:

- **Check Logs:** Check the logs for problems at all times. You may get important information about what went wrong by using the command docker logs <container_name>. Error messages or warnings that might help you identify the precise source of the problem—such as missing files, dependency issues, or runtime exceptions—are frequently seen in the logs.

- **Rebuild the Image:** Remember to use the command docker build -t <image_name> to rebuild the Docker image whenever you make changes to the Dockerfile or your application. This guarantees that the updated picture incorporates your modifications. Using a version tag for the picture is also a smart idea because it makes it simple to go back to an earlier version if necessary.

- **Resource Allocation:** Ensure that the container has sufficient resources (CPU, memory) allocated. You can adjust these settings in your Docker settings or specify them when starting the container. Inadequate resources may lead to performance degradation or application crashes, particularly for resource-intensive applications like those utilizing the NeMo toolkit.

- **Network Configuration:** Verify your network settings to make sure the right ports are open and mapped to your host computer if you're experiencing problems with external access. Additionally, as this is frequently the cause of connectivity problems, confirm that any firewalls or security groups permit traffic on these ports.

- **Version Compatibility:** Ensure that the versions of Python, NeMo, and other libraries are compatible with each other. Checking the official documentation or community forums can provide guidance on compatible versions. Using incompatible versions can lead to unexpected behavior or runtime errors, so it’s important to verify compatibility before deployment.

- **Container Permissions:** Make that the container has the required permissions if the program needs access to host files or directories. It might be necessary to execute the container with elevated rights or modify file permissions. When working with mounted disks or data directories, where the program must read from or write to specified paths, this is very important.

- **Testing with Minimal Setup:** If the problem persists, try doing a rudimentary setup using only the most basic instructions. By doing so, you may determine whether the issue is related to the environment, code, or settings. To ensure that the essential features perform, you might begin with a straightforward script or command and then progressively add more complexity.

- **Consult the Community:** Consider contacting the NeMo community if you are unable to fix the problem. For troubleshooting advice and direction from seasoned users, forums, GitHub bugs, and chat channels can be excellent resources. Interacting with the community can yield information on prevalent problems and helpful practices that might not be well known.

- **Document the Issue:** Keep track of any faults you run across and the actions you take to fix them while you troubleshoot. Documenting problems will help future development attempts go more smoothly and benefit others who might have similar difficulties. Additionally, your team or community may find this material to be a useful resource that facilitates cooperative problem-solving.

#### Documenting:

It's crucial to record any problems you run across during troubleshooting, along with the actions you take to fix them. Maintaining a record of issues and fixes might facilitate future development initiatives and aid anyone who might have comparable difficulties.

