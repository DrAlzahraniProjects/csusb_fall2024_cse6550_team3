import os
import subprocess
import platform
import socket
import __main__ as main
import sys

# Function to load environment variables from a .env file
def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath) as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

# Load environment variables from the .env file
load_env_file()

# Determine the correct Python command
def get_python_command():
    if platform.system() == "Windows":
        try:
            # Check if python3 can be called
            subprocess.run(["python3", "--version"], check=True)
            return "python3"
        except subprocess.CalledProcessError:
            return "python"  # Fallback if python3 is not available
    else:
        return "python3"  # Default to python3 on Unix-like systems

python_cmd = get_python_command()  # Use the system Python command

# Initialize the API key variable
api_key = os.getenv("MISTRAL_API_KEY")

# Debug statement to verify API key loading
print(f"Loaded MISTRAL_API_KEY: {api_key}")

# Ensure the API key is present in the environment variables
if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in environment variables. Please set it in the .env file.")

# Function to navigate to the project directory
def navigate_to_project_directory(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"The specified project directory does not exist: {path}")
    os.chdir(path)

# Function to ensure the Python version is 3.10 or above
def check_python_version():
    result = subprocess.run([python_cmd, "--version"], capture_output=True, text=True, check=True)
    version = result.stdout.strip()
    if not (version.startswith("Python 3.10") or version.startswith("Python 3.11") or version.startswith("Python 3.12")):
        raise EnvironmentError("Python 3.10 or above is required.")

# Function to install dependencies
def install_dependencies():
    subprocess.run([python_cmd, "-m", "pip", "install", "-r", "requirements.txt"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Function to check if a port is available
def is_port_available(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) != 0

# Function to terminate the process using the specified port
def terminate_process_on_port(port):
    cmd = f"lsof -t -i:{port}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        pid = result.stdout.strip()
        subprocess.run(["kill", "-9", pid], check=True)

# Function to start Jupyter Notebook on port 6003
def start_jupyter_notebook():
    notebook_path = "jupyter/main.ipynb"
    if not os.path.exists(notebook_path):
        raise FileNotFoundError(f"The specified notebook does not exist: {notebook_path}")

    port = 6003
    if not is_port_available(port):
        terminate_process_on_port(port)

    subprocess.run([
        python_cmd, "-m", "notebook", 
        notebook_path, 
        f"--port={port}", 
        "--ip=127.0.0.1"
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    project_path = os.path.abspath(".")  # Set project path to the current directory
    try:
        navigate_to_project_directory(project_path)
        check_python_version()
        install_dependencies()
        start_jupyter_notebook()
    except Exception as e:
        print(f"An error occurred: {e}")
