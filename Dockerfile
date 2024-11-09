# Use Python as the base image
FROM python:3.11-slim

# Suppress apt prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Set environment variables to prevent bytecode writing and ensure unbuffered logging
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

# Add MISTRAL API key to .env file for app use
ARG MISTRAL
RUN echo "MISTRAL_API_KEY=$MISTRAL" > /app/.env

# Update and install necessary system packages
RUN apt-get update && apt-get install -y \
    wget \
    bzip2 \
    ca-certificates \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Install Mambaforge for appropriate architecture (x86_64 or aarch64)
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

# Add Mambaforge to PATH
ENV PATH=/opt/miniforge/bin:$PATH

# Create a new conda environment named 'team3_env' with Python 3.11
RUN mamba create -n team3_env python=3.11 -y

# Use the new environment's shell for subsequent commands
SHELL ["mamba", "run", "-n", "team3_env", "/bin/bash", "-c"]

# Copy requirements.txt into the container
COPY requirements.txt /app/requirements.txt

# Install Python packages from requirements.txt using Mamba
RUN mamba install --yes --file requirements.txt && mamba clean --all -f -y

# Install cython, NeMo toolkit with curator, and other dependencies
RUN /opt/miniforge/envs/team3_env/bin/pip install cython
RUN /opt/miniforge/envs/team3_env/bin/pip install nemo_toolkit[all]  # Installs core toolkit
RUN /opt/miniforge/envs/team3_env/bin/pip install nemo_toolkit[curator]  # Installs curator specifically

# Install additional Python packages directly with pip
RUN /opt/miniforge/envs/team3_env/bin/pip install rank_bm25 streamlit-pdf-viewer

# Copy all application code into the container's /app directory
COPY . /app

# Expose port 5003 for Streamlit access
EXPOSE 5003

# Expose port 6003 for Jupyter access
EXPOSE 6003

# Set the environment’s bin directory as default PATH
ENV PATH=/opt/miniforge/envs/team3_env/bin:$PATH

# Set entrypoint to Python, default command to run app.py
ENTRYPOINT ["python"]
CMD ["app.py"]
