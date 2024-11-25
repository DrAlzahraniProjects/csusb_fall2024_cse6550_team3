import os
import subprocess
import platform
import socket
import sys

# Function to create .env file from .env.template and insert the API key
def create_env_file_from_template(template_filepath=".env.template", output_filepath=".env"):
    api_key = None
    if os.path.exists(template_filepath):
        with open(template_filepath, "r") as template_file:
            content = template_file.read()
            for line in content.splitlines():
                if line.startswith("MISTRAL_API_KEY=") and "MISTRAL_API_KEY=your_actual_api_key_here" not in line:
                    api_key = line.split("=", 1)[1].strip()
                    break
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
                    print(f"Loaded {key} from {filepath}")  # Debug statement
    else:
        print(f"Warning: {filepath} not found.")

# Function to navigate to the project directory
def navigate_to_project_directory(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"The specified project directory does not exist: {path}")
    os.chdir(path)

# Function to ensure the Python version is 3.10 or above
def check_python_version():
    if sys.version_info < (3, 10):
        raise EnvironmentError("Python 3.10 or above is required.")

# Function to check if a port is available
def is_port_available(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) != 0

# Function to terminate the process using the specified port
def terminate_process_on_port(port):
    if platform.system() == "Windows":
        cmd = f"netstat -ano | findstr :{port}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            lines = result.stdout.strip().splitlines()
            for line in lines:
                pid = line.strip().split()[-1]
                try:
                    subprocess.run(["taskkill", "/F", "/PID", pid], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Failed to kill process with PID {pid}: {e}")
    else:
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
    notebook_path = os.path.join(os.getcwd(), "jupyter", "main.ipynb")
    port = 6003
    if not os.path.exists(notebook_path):
        print(f"Warning: The specified notebook does not exist: {notebook_path}. Starting Jupyter Notebook in the default location.")
    if not is_port_available(port):
        terminate_process_on_port(port)
    else:
        print(f"Port {port} is available. Starting Jupyter Notebook...")

    python_executable = sys.executable
    subprocess.run([
        python_executable, "-m", "notebook",
        f"--port={port}", "--ip=127.0.0.1", "--NotebookApp.base_url=/team3/jupyter", "--NotebookApp.notebook_dir=/jupyter"
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    project_path = os.path.dirname(os.path.realpath(__file__))  # Set project path to the current directory
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
