# Use Python as the base image
FROM python:3.11-slim

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

# Update and install necessary packages
RUN apt-get update && apt-get install -y \
	wget \
	bzip2 \
	ca-certificates \
	build-essential \
	cmake \
	&& rm -rf /var/lib/apt/lists/*

# Install Mambaforge for the appropriate architecture
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

# Create a new environment with Python 3.11
RUN mamba create -n team3_env python=3.11 -y

# Activate the new environment
SHELL ["mamba", "run", "-n", "team3_env", "/bin/bash", "-c"]

# Copy requirements.txt into the container
COPY requirements.txt /app/requirements.txt

# Install Python packages from requirements.txt
RUN mamba install --yes --file requirements.txt && mamba clean --all -f -y
RUN pip install rank_bm25 streamlit-pdf-viewer jupyter

# Copy the current directory contents into the container at /app
COPY . /app

# Expose Streamlit port
EXPOSE 5003

# Expose Jupyter port
EXPOSE 6003

# Add the conda environment's bin directory to PATH
ENV PATH=/opt/miniforge/envs/team3_env/bin:$PATH

# Set entry point and default command
ENTRYPOINT ["python"]
CMD ["app.py"]
