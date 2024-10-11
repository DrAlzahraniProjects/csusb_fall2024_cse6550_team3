# Use a specific version of mambaforge
FROM condaforge/mambaforge:4.10.3-7

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt /app/requirements.txt

# Install base packages
RUN mamba install -y -c conda-forge \
    python=3.9 \
    pip \
    && mamba clean --all -f -y

# Install packages in smaller groups
# Adjust these package groups based on your specific requirements
RUN mamba install -y -c conda-forge \
    numpy \
    pandas \
    scipy \
    matplotlib \
    && mamba clean --all -f -y

RUN mamba install -y -c conda-forge \
    scikit-learn \
    statsmodels \
    seaborn \
    && mamba clean --all -f -y

# Install remaining packages from requirements.txt
RUN mamba install -y --file /app/requirements.txt \
    && mamba clean --all -f -y

# Copy your application code
COPY . /app

# Command to run your application
# Replace 'your_main_script.py' with your actual main script
CMD ["python", "your_main_script.py"]
