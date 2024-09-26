# Use Python as the base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y wget && apt-get install -y nginx

# Determine system architecture and install the corresponding version of Mambaforge
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
        wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh; \
    elif [ "$ARCH" = "aarch64" ]; then \
        wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-aarch64.sh; \
    else \
        echo "Unsupported architecture: $ARCH" && exit 1; \
    fi && \
    bash Mambaforge-Linux-*.sh -b && \
    ls -la /root/mambaforge && \
    rm Mambaforge-Linux-*.sh && \
    apt-get clean

# Set environment path to use Mambaforge
ENV PATH="/root/mambaforge/bin:$PATH"

# Create a new environment with Python 3.11 using mamba
RUN /root/mambaforge/bin/mamba create -n team3_env python=3.11 -y \
    && /root/mambaforge/bin/mamba clean --all -f -y

# Set environment path to use team3_env and ensure bash is used
ENV PATH="/root/mambaforge/envs/team3_env/bin:$PATH"

# Activate the environment and install packages from requirements.txt
SHELL ["/bin/bash", "-c"]
RUN echo "source /root/mambaforge/bin/activate team3_env" >> ~/.bashrc

# Copy requirements.txt into the container
COPY requirements.txt /app/requirements.txt

RUN mamba install -c conda-forge jupyter ipykernel

# Install Python packages from requirements.txt
RUN /bin/bash -c "source ~/.bashrc && mamba install --yes --file /app/requirements.txt && mamba clean --all -f -y"

# Copy NGINX config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the current directory contents into the container
COPY . /app

# Expose ports for NGINX, Streamlit, and Jupyter
EXPOSE 83
EXPOSE 5003
EXPOSE 6003

CMD service nginx start && \
    streamlit run app.py --server.port=5003 & \
    jupyter notebook --ip=0.0.0.0 --port=6003 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password='' & \
    wait
