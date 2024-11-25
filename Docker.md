## Dockerfile Documentation
## Table of Contents
1.⁠ ⁠[Installation](#installation)

2.⁠ ⁠[Configuration](#configuration)

3.⁠ ⁠[Implementation](#implementation)

4.⁠ ⁠[Usage](#usage)

5.⁠ ⁠[Troubleshooting](#troubleshooting)

----------

## Installation
### Steps for Installation
#### macOS:

1.  **Download Docker Desktop**: Begin by visiting the official  [Docker Hub](https://hub.docker.com/editions/community/docker-ce-desktop-mac). Here, you will find Docker Desktop specifically designed for macOS. Choose the latest version to ensure you have the newest features and fixes.
    
2.  **Install Docker**: Once the download completes, open the downloaded  `.dmg`  file. This action will mount a disk image and open a new window displaying the Docker icon. Drag the Docker icon into the Applications folder. This step copies all necessary files into your Applications directory, making Docker easily accessible.
    
3.  **Launch Docker**: After installation, navigate to your Applications folder and double-click the Docker icon to launch Docker Desktop. The first time you start Docker, it may request your system password to allow changes necessary for operation.
    
4.  **Initial Setup**: When Docker Desktop starts, it may perform some initial setup tasks and show you a tutorial or tips for usage. If you’re new to Docker, take the time to review these resources to familiarize yourself with the interface.
    

**Verify Installation**: After completing the installation and setup, open your terminal and verify that Docker is installed correctly by executing:
```
docker --version
```
![image](https://github.com/user-attachments/assets/65f8c1cb-cec6-4f1d-a8b7-afc445eff636)

*Figure 1: Screenshot showing the output of docker --version command, confirming Docker installation.*


You should see the version number of Docker displayed in your terminal, confirming that the installation was successful.

#### Linux:

1.  **Update your package index**: Open a terminal and run the following command to ensure your package manager has the latest information about available packages:
```
sudo apt-get update
```
This step is critical for a smooth installation process, as it refreshes the list of available packages.

2.  **Install Docker using APT**: Execute the following command to install Docker along with its necessary components, including the Docker engine and command-line interface:
```
sudo apt-get install docker-ce docker-ce-cli containerd.io
```
During the installation, you may be prompted to confirm the installation of additional packages. Type  `Y`  and press enter to proceed.

**Verify Installation**: After the installation is complete, confirm that Docker is functioning correctly by running:
```
docker --version
```
If successful, this command will display the version number, indicating that Docker is ready to use.

#### Windows:

1.  **Download Docker Desktop**: Go to Docker Hub and download Docker Desktop for Windows. Be sure to select the version compatible with your Windows edition, particularly if you are using Windows 10 Home or Pro.
    
2.  **Install Docker**: Open the downloaded installer and follow the installation wizard's prompts. You may need to enable the Windows Subsystem for Linux (WSL) feature during the installation, especially if you’re using Windows 10 or later. Enabling WSL allows for a more seamless Docker experience.
    
3.  **Launch Docker**: Once the installation is complete, start Docker Desktop from your Start menu or by searching for it. Docker will initialize and run in the background.
    

**Verify Installation**: To confirm the installation, open PowerShell or Command Prompt and execute:
```
docker --version
``` 

This command should output the Docker version, verifying that the software is properly installed.

----------

## Configuration

### macOS and Windows:

Docker Desktop provides a user-friendly graphical interface for configuring its settings. This customization helps users optimize their experience based on the resources available on their machines.

1.  **Access Preferences/Settings**: Launch Docker Desktop, then click on the Docker icon in the menu bar (for macOS) or system tray (for Windows). Select "Preferences" (macOS) or "Settings" (Windows) from the dropdown menu.
    
2.  **Configure Resources**: Navigate to the "Resources" tab within the settings. Here, you can allocate a specific amount of memory, CPU cores, and disk space to Docker. For instance, if you are running resource-intensive applications, you may want to increase the memory limit. It’s essential to balance these settings to avoid starving your host machine of necessary resources.
    
    -   **Memory**: The memory allocation defines how much RAM Docker can utilize. Allocating too little may cause containers to crash or run slowly, while allocating too much may impact the performance of other applications on your host.
    -   **CPU**: This setting allows you to specify how many CPU cores Docker can use. If you're running multiple containers or demanding applications, increasing the CPU allocation can improve performance.
    -   **Disk Space**: Manage how much disk space Docker is allowed to use for its images and containers.
3.  **File Sharing**: You may also need to configure file sharing, allowing Docker containers to access files on your host machine. Navigate to the "File Sharing" section and add directories you wish to make accessible to your containers. This is particularly useful for development, enabling you to edit code on your host while the container uses the latest version.
    

### Linux:

For Linux systems, Docker's daemon configuration can be adjusted via the  `/etc/docker/daemon.json`  file. This file enables advanced users to set various parameters for the Docker daemon.

1.  **Edit the Daemon Configuration**: Open the daemon configuration file using a text editor of your choice. For example:
```
sudo nano /etc/docker/daemon.json
```

If the file does not exist, you can create it.

2.  **Sample Configuration**: Below is a sample configuration you might consider:
```
{
  "log-level": "info",
  "storage-driver": "overlay2",
  "data-root": "/mnt/docker-data",
  "insecure-registries": ["my-insecure-registry.com"]
}
```

In this example:

-   **log-level**: Controls the verbosity of logs generated by the Docker daemon. Options include  `debug`,  `info`,  `warn`,  `error`, etc. Setting it to  `debug`  can provide detailed information during troubleshooting.
-   **storage-driver**: Specifies the storage driver to use;  `overlay2`  is recommended for most modern systems due to its performance and efficiency.
-   **data-root**: Defines the root directory for all Docker data, which can be helpful for managing disk space effectively. Changing this allows you to specify a partition or drive with ample space for your containers and images.
-   **insecure-registries**: Lists any registries that should be treated as insecure, which is useful for local development when you might not have SSL certificates set up.

**Restart Docker**: After editing the configuration, restart the Docker service to apply the changes:

```
sudo systemctl restart docker
```

### Network Configuration:

By default, Docker uses a bridge network, which allows containers to communicate with each other. However, you can create custom networks to manage connections more effectively and enhance security.

1.  **Create a Custom Network**: If you want to create a network with specific configurations, use the following command:

```
docker network create my_network
```
![image](https://github.com/user-attachments/assets/6054d720-a318-46de-ac8f-9075486734de)

*Figure 2: Illustration showing Docker network creation using the docker network create command.*


This command creates a new network named  `my_network`.

2.  **Use the Custom Network**: When running containers, specify the network to use:

```
docker run --network my_network my_container
```

Using custom networks helps isolate different applications, control how they interact, and can improve security by limiting visibility and access between services.

3.  **Inspecting Networks**: To view details about existing networks, you can run:

```
docker network ls
```
![image](https://github.com/user-attachments/assets/9db8b354-de5f-4004-90b7-b9e142ebb86f)

*Figure 3: Example output of the docker network ls command, listing available Docker networks.*


This command lists all Docker networks. To inspect a specific network and view its settings and connected containers, use:
```
docker network inspect <network_name>
```

----------

## Implementation

### Creating a Dockerfile

A Dockerfile is a text document containing all the commands needed to assemble an image. Docker reads this file line by line, executing each command to create the final image. Below is a basic example of a Dockerfile for a Python application.
```
# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5003 available to the outside world
EXPOSE 5003

# Run the application
CMD ["python", "app.py"]
```
![image](https://github.com/user-attachments/assets/50fefba4-f696-46d4-9194-15265a7eab40)

*Figure 4: Example of a Dockerfile for a Python application.*

### Breakdown of the Dockerfile:

1.  **FROM**: This instruction specifies the base image for your application. Using  `python:3.9-slim`  pulls a minimal Python image, which reduces the size of your final image and improves performance. Selecting an appropriate base image is crucial as it determines the environment your application runs in.
    
2.  **WORKDIR**: This command sets the working directory inside the container. All subsequent commands (like  `COPY`,  `RUN`, etc.) will be executed in this directory. By specifying a working directory, you ensure that the application can find its files without requiring full path specifications.
    
3.  **COPY**: This instruction copies files from your local machine into the container. The command  `COPY . .`  copies everything from the current directory on your host to the current directory in the container. It’s important to structure your application files logically for ease of copying.
    
4.  **RUN**: This command executes a command inside the container. Here, it installs the required Python packages specified in  `requirements.txt`. Using  `--no-cache-dir`  helps reduce the image size by not storing cache files from the installation.
    
5.  **EXPOSE**: This instruction informs Docker that the container listens on the specified network ports at runtime. While it does not actually publish the port (that’s done at runtime), it serves as documentation and can help others understand which ports the application uses.
    
6.  **CMD**: This specifies the command to run when the container starts. Here, it runs the Python application  `app.py`. Only one  `CMD`  instruction is allowed in a Dockerfile; if multiple are specified, only the last one takes effect.
    

### Building and Running Containers

Once you have created your Dockerfile, you can build an image from it.

**Build the Image**: To build your Docker image, navigate to the directory containing your Dockerfile and run:
```
docker build -t team3-app .
```
![image](https://github.com/user-attachments/assets/32c782b4-04c1-48f7-a1ad-06532d77d449)

*Figure 5: Example output of the docker build -t team3-app . command, showing successful image creation.*


The  `-t`  flag tags your image with a name (`team3-app`), making it easier to reference later. The  `.`  specifies the build context, which is the current directory.

**Run the Container**: After building the image, you can run it with the following command:
```
docker run -d -p 5003:5003 team3-app
```
![image](https://github.com/user-attachments/assets/2a5b9f01-fa11-441f-923f-506d9d005178)

*Figure 6: Output of the docker run -d -p 5003:5003 team3-app command, showing container execution.*


Here, the  `-d`  flag runs the container in detached mode, allowing it to run in the background. The  `-p`  flag maps port 5003 on your host to port 5003 on the container, enabling you to access the application via your host's IP address.
![image](https://github.com/user-attachments/assets/6fb29643-8a5d-4ab3-bc9e-85ccab2c8583)

*Figure 7: Docker container with a link mapping to specific port.*
**Verify the Container is Running**: You can confirm that your container is running by executing:
```
docker ps
```
![image](https://github.com/user-attachments/assets/d8e119a7-6ad2-401e-905d-98a2b7c98b8e)

*Figure 8: Example output of the docker ps command, listing running Docker containers.*


This command lists all currently running containers, displaying their IDs, names, and the ports they’re using.

### Using Docker Compose

Docker Compose is a tool for defining and running multi-container Docker applications. It allows you to configure services, networks, and volumes in a single file, making management simpler.

#### Sample  `docker-compose.yml`:

Here’s a sample  `docker-compose.yml`  file that sets up a web application alongside a Redis service:

```
version: '3'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/code
    depends_on:
      - redis
  redis:
    image: "redis:alpine"
   ```

#### Explanation of the Compose File:

-   **version**: Specifies the version of the Docker Compose file format. This ensures compatibility with the Docker Compose tool.
    
-   **services**: This section defines the different services in your application.
    
    -   **web**: This defines the web service.
        -   **build**: Indicates that Docker should build the image using the Dockerfile in the current directory.
        -   **ports**: Maps port 5000 of the host to port 5000 of the container.
        -   **volumes**: Mounts the current directory into the container at  `/code`, enabling live code updates. This allows changes made on your host machine to reflect immediately in the container, which is particularly useful during development.
        -   **depends_on**: Specifies that the  `web`  service depends on the  `redis`  service. This ensures that Redis starts before the web application, helping to avoid connection errors during initialization.
-   **redis**: This section defines the Redis service, which is essential for caching and session storage. It uses the official Redis image from Docker Hub, ensuring a stable and secure implementation.
    

To run the services defined in your  `docker-compose.yml`, execute:
```
docker-compose up
```

This command builds and starts the defined services. If you want to run it in detached mode, add the  `-d`  flag:
```
docker-compose up -d
```

To stop and remove the containers and associated networks defined in the Compose file, use:
```
docker-compose down
```

This command cleans up all resources created by  `docker-compose up`, making it easy to reset your environment.

----------

## Usage

### Basic Commands

Once Docker is up and running, you can manage your containers and images through a variety of commands. Familiarizing yourself with these commands will greatly enhance your efficiency when working with Docker.

#### List Running Containers

To see a list of all currently running containers, use:
```
docker ps
```
![image](https://github.com/user-attachments/assets/60e2fff7-4e4d-4520-b6cf-f64842ececd9)

*Figure 9: Example output of the docker ps command, showing running containers.*

This command displays useful information, including container IDs, names, status, and the ports they are using. If you want to see all containers, including those that are stopped, you can use:
```
docker ps -a
```

This command provides a more comprehensive view of your Docker environment.

#### Stop a Container

To stop a running container, execute:
```
docker stop <container_id>
```
![image](https://github.com/user-attachments/assets/49b5a258-b68a-44d7-a5a1-c1dfb774c7b5)

*Figure 10: Example of stopping a container using the docker stop command.*

You can find the  `<container_id>`  from the output of  `docker ps`. This command sends a SIGTERM signal to the container, allowing it to shut down gracefully. If the container does not stop after a grace period, you can forcefully terminate it using:
```
docker kill <container_id>
```

#### Remove a Container

If you need to remove a container that is no longer running, use:
```
docker rm <container_id>
```

This command permanently deletes the container from your system. You can remove all stopped containers in one command by using:

```
docker container prune
```

This command cleans up unused containers, helping to free up system resources.

#### List Images

To view all Docker images currently on your system, run:
```
docker images
```
![image](https://github.com/user-attachments/assets/e5e6fdb3-b744-4d42-aa04-49988a810e6c)

*Figure 11: Example output of the docker images command, listing available images.*

This will show the repository, tag, image ID, and size of each image, helping you manage storage.

#### Remove an Image

If you want to delete an unused image, you can do so with:
```
docker rmi <image_id>
```

Be cautious when removing images; ensure that no containers are using them, or you may encounter an error. To remove all unused images, you can use:
```
docker image prune
```

### Accessing a Running Container

To access a shell inside a running container for debugging or administration, use the command:
```
docker exec -it <container_id> /bin/bash
```

This command opens an interactive terminal session inside the specified container, allowing you to run commands directly in that environment. If the container does not have Bash installed, you may need to use  `/bin/sh`  instead.

### Logging

Monitoring logs is crucial for debugging. To view logs from a running container, use:
```
docker logs <container_id>
```
![image](https://github.com/user-attachments/assets/3a228e0e-ea6b-41da-a437-b1a383a6208b)

*Figure 12: Example output of docker logs command showing logs from a running container.*

This command outputs the logs generated by the application running inside the container, providing insights into its behavior and errors. You can also use the  `-f`  option to follow the logs in real-time:
```
docker logs -f <container_id>
```

----------

## Troubleshooting

### Common Issues

As with any technology, Docker users may encounter various issues. Here’s a guide to resolving some common problems.

#### Docker Daemon Not Starting

If the Docker daemon fails to start, it can be due to several reasons. Check its status with:
```
sudo systemctl status docker
```

This command provides information about whether the Docker service is active and running. If it’s not running, start the Docker service with:
```
sudo systemctl start docker
```

If you continue experiencing issues, check system logs for potential errors related to Docker. On Linux, you can view logs with:
```
journalctl -u docker.service
```

#### Permission Issues

Sometimes, you may face permission issues when running Docker commands. This is common if you do not have the necessary permissions to execute Docker without  `sudo`. To resolve this, add your user to the Docker group:
```
sudo usermod -aG docker $USER
```

After running this command, log out of your session and log back in, or restart your machine for the changes to take effect. You can verify group membership with:
```
groups
```

#### Container Not Starting

If a container fails to start, the logs can provide valuable information. Use the following command to check for error messages:
```
docker logs <container_id>
```
![image](https://github.com/user-attachments/assets/5f93976d-1dac-4d8d-bff3-6a2b636421ee)

*Figure 13: Output of logs in the Docker app*
If the logs indicate a misconfiguration or an issue with dependencies, address those errors accordingly. You can also inspect the container for further diagnostics:
```
docker inspect <container_id>
```

![image](https://github.com/user-attachments/assets/9e78e050-ce00-4c47-9fc8-117523eb522b)

*Figure 14: Docker inspections for running container*

This command provides a detailed JSON output of the container’s configuration and status, helping you pinpoint the issue.

#### Network Issues

If containers cannot communicate with each other, it may be due to network misconfiguration. First, check that all containers are on the same network:

```
docker network ls
```
![image](https://github.com/user-attachments/assets/eac49948-d3fc-4b69-9fd4-89edaf1bb1bc)

*Figure 15: Example of inspecting a Docker network using the docker network inspect command.*

To inspect a specific network and see which containers are connected, use:
```
docker network inspect <network_name>
```

Ensure your containers are correctly connected to the intended network, especially when using custom networks.

#### Image Build Failing

If your image fails to build, it’s often due to syntax errors in the Dockerfile or unresolved dependencies. Double-check the Dockerfile for any mistakes. You can also build the image with verbose logging to gain more insights:
```
docker build --progress=plain -t <image_name> .
```

This command provides detailed output during the build process, helping you identify where the failure occurs.