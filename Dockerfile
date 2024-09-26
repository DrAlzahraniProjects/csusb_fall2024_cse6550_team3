# Use Python as the base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y wget curl bzip2 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Download and install Mambaforge
RUN wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh -O /tmp/Mambaforge.sh && \
    bash /tmp/Mambaforge.sh -b -p /root/mambaforge && \
    rm /tmp/Mambaforge.sh

# Set environment path to use Mambaforge
ENV PATH="/root/mambaforge/bin:$PATH"

# Install Mamba and create a new environment with Python 3.11
RUN /root/mambaforge/bin/conda install mamba -c conda-forge -y && \
    /root/mambaforge/bin/mamba create -n team3_env python=3.11 -y && \
    /root/mambaforge/bin/mamba clean --all -f -y

# Set environment path to use team3_env
ENV PATH="/root/mambaforge/envs/team3_env/bin:$PATH"

# Copy requirements.txt into the container
COPY requirements.txt /app/requirements.txt

# Install Python packages from requirements.txt
RUN mamba install --yes --file /app/requirements.txt

# Install Jupyter Notebook and necessary kernel
RUN mamba install -c conda-forge jupyter ipykernel

# Ensure kernel is installed for the environment
RUN python -m ipykernel install --name team3_env --display-name "Python (team3_env)"

# Install NGINX
RUN apt-get update && apt-get install -y nginx && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy NGINX config
COPY nginx.conf /etc/nginx/nginx.conf

# Expose ports for NGINX, Streamlit, and Jupyter
EXPOSE 83
EXPOSE 5003
EXPOSE 6003

CMD service nginx start && \
    streamlit run app.py --server.port=5003 & \
    jupyter notebook --ip=0.0.0.0 --port=6003 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password='' & \
    wait
