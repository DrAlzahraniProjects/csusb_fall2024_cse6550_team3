# Use Python 3.11 slim image as the base
FROM python:3.11-slim

# Set environment variables for Python behavior
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /app

# Update and install necessary system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    nginx \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Download and install Mambaforge based on the system architecture
RUN ARCH=$(dpkg --print-architecture) && \
    if [ "$ARCH" = "amd64" ]; then \
        wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh -O mambaforge.sh; \
    elif [ "$ARCH" = "arm64" ]; then \
        wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-aarch64.sh -O mambaforge.sh; \
    else \
        echo "Unsupported architecture: $ARCH" && exit 1; \
    fi && \
    bash mambaforge.sh -b -p /opt/mambaforge && \
    rm mambaforge.sh

# Add Mambaforge to PATH
ENV PATH=/opt/mambaforge/bin:$PATH

# Set bash as the default shell
SHELL ["/bin/bash", "-c"]

# Create a new mamba environment and activate it in .bashrc
RUN mamba create -n team3_env python=3.11 -y && \
    mamba clean --all -f -y && \
    echo "source /opt/mambaforge/bin/activate team3_env" >> ~/.bashrc

# Add the new environment to PATH
ENV PATH=/opt/mambaforge/envs/team3_env/bin:$PATH

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN mamba run -n team3_env mamba install --yes --file requirements.txt && \
    mamba clean --all -f -y

# Copy Nginx configuration and application files
COPY nginx.conf /etc/nginx/nginx.conf
COPY . /app

# Streamlit Port
EXPOSE 5003
# Jupyter Notebook Port
# EXPOSE 6003

# Set the entrypoint to run commands in the mamba environment
ENTRYPOINT ["mamba", "run", "-n", "team3_env"]

# Set the default command to run the Python application
CMD ["python", "app.py"]