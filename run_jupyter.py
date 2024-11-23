import os
import subprocess
import platform
import socket
import __main__ as main
import sys

# Function to create .env file from .env.template and insert the API key
def create_env_file_from_template(template_filepath=".env.template", output_filepath=".env"):
    api_key = None
    if os.path.exists(template_filepath):
        with open(template_filepath, "r") as template_file:
            content = template_file.read()
            if "MISTRAL_API_KEY=" in content and "MISTRAL_API_KEY=your_actual_api_key_here" not in content:
                for line in content.splitlines():
                    if line.startswith("MISTRAL_API_KEY=") and line.strip() != "MISTRAL_API_KEY=":
                        api_key = line.split("=", 1)[1].strip()
            if not api_key:
                api_key = input("Enter your API key here: ")
                content = content.replace("MISTRAL_API_KEY=", f"MISTRAL_API_KEY={api_key}")
        
        with open(output_filepath, "w") as env_file:
            env_file.write(content)
    else:
        raise FileNotFoundError(f"The specified template file does not exist: {template_filepath}")

# Function to load environment variables from a .env file
def load_env_file(filepath=".env"):
    if os.path.exists(filepath):
        with open(filepath) as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

# Function to navigate to the project directory
def navigate_to_project_directory(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"The specified project directory does not exist: {path}")
    os.chdir(path)

# Function to ensure the Python version is 3.10 or above
def check_python_version():
    result = subprocess.run(["python", "--version"], capture_output=True, text=True, check=True)
    version = result.stdout.strip()
    if not (version.startswith("Python 3.10") or version.startswith("Python 3.11") or version.startswith("Python 3.12")):
        raise EnvironmentError("Python 3.10 or above is required.")

# Function to check if a port is available
def is_port_available(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) != 0

# Function to terminate the process using the specified port
def terminate_process_on_port(port):
    cmd = f"lsof -t -i:{port}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        pids = result.stdout.strip().split()
        for pid in pids:
            try:
                subprocess.run(["kill", "-9", pid], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Failed to kill process with PID {pid}: {e}")

# Function to start Jupyter Notebook on port 6003
def start_jupyter_notebook():
    notebook_path = "jupyter/main.ipynb"
    if not os.path.exists(notebook_path):
        raise FileNotFoundError(f"The specified notebook does not exist: {notebook_path}")

    port = 6003
    if not is_port_available(port):
        terminate_process_on_port(port)

    subprocess.run([
        "python", "-m", "notebook", 
        notebook_path, 
        f"--port={port}", 
        "--ip=127.0.0.1"
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    project_path = os.path.abspath(".")  # Set project path to the current directory
    try:
        navigate_to_project_directory(project_path)
        check_python_version()
        
        # Insert API key into the .env file from template if not present
        create_env_file_from_template()

        # Load environment variables
        load_env_file()
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY not found in environment variables. Please set it in the .env file.")
        
        # Print only the required messages
        print("Successfully loaded MISTRAL_API_KEY.")
        print("Jupyter Notebook will open in a while...")
        
        # Start Jupyter Notebook
        start_jupyter_notebook()
    except Exception as e:
        print(f"An error occurred: {e}")
