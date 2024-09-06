# Use the official Conda image as the base
FROM continuumio/miniconda3:latest

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./src /app

# Install mamba
RUN conda install -c conda-forge mamba

# Create a new environment with Python 3.11 using mamba
RUN mamba create -n myenv python=3.11

# Activate the new environment
SHELL ["mamba", "run", "-n", "myenv", "/bin/bash", "-c"]

# Install any needed packages specified in requirements.txt
COPY src/requirements.txt /app/
RUN mamba install --yes --file requirements.txt

# Make ports available to the world outside this container
EXPOSE 5003

# Set the default command to run when starting the container
CMD ["mamba", "run", "--no-capture-output", "-n", "myenv", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]