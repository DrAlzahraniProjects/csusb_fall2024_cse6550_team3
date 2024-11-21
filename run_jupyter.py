import os
import subprocess
import platform
import socket
import __main__ as main

try:
    import psutil
except ModuleNotFoundError:
    subprocess.run(["pip", "install", "psutil"], check=True)
    import psutil

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    subprocess.run(["pip", "install", "python-dotenv"], check=True)
    from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Initialize the API key variable
api_key = os.getenv("MISTRAL_API_KEY")

# Check if the script is running as a standalone program (i.e., not in Jupyter Notebook)
if not hasattr(main, '__file__'):
    # Running in an interactive environment like Jupyter Notebook
    if not api_key:
        raise ValueError("MISTRAL API KEY not found in environment variables. Please set it in the .env file.")
else:
    # Running in a terminal or script
    if not api_key:
        api_key = input("MISTRAL API KEY not found in environment variables. Please enter your API key: ")
        if not api_key:
            raise ValueError("MISTRAL API KEY not provided.")

# 1. Navigate to your project directory
def navigate_to_project_directory(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"The specified project directory does not exist: {path}")
    os.chdir(path)

# 2. Create a virtual environment
def create_virtual_environment():
    if not os.path.exists("venv"):
        subprocess.run(["python3", "-m", "venv", "venv"], check=True)

# 3. Activate the virtual environment
def activate_virtual_environment():
    system = platform.system()
    if system == "Windows":
        activate_script = ".\\venv\\Scripts\\activate"
    elif system == "Linux" or system == "Darwin":  # Darwin is for macOS
        activate_script = "source venv/bin/activate"
    else:
        raise EnvironmentError("Unsupported operating system.")

# 4. Ensure Python version is 3.10 or above
def check_python_version():
    result = subprocess.run(["python3", "--version"], capture_output=True, text=True, check=True)
    version = result.stdout.strip()
    if not (version.startswith("Python 3.10") or version.startswith("Python 3.11") or version.startswith("Python 3.12")):
        raise EnvironmentError("Python 3.10 or above is required.")

# 5. Install dependencies
def install_dependencies():
    subprocess.run(["venv/bin/pip" if platform.system() != "Windows" else "venv\\Scripts\\pip", "install", "-r", "requirements.txt"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Check if a port is available
def is_port_available(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) != 0

# Terminate the process using the specified port
def terminate_process_on_port(port):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for conn in proc.connections(kind='inet'):
                if conn.laddr.port == port:
                    proc.terminate()
                    proc.wait()  # Ensure the process is terminated before proceeding
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue

# 7. Start Jupyter Notebook on port 6003
def start_jupyter_notebook():
    notebook_path = "jupyter/main.ipynb"
    if not os.path.exists(notebook_path):
        raise FileNotFoundError(f"The specified notebook does not exist: {notebook_path}")

    port = 6003
    if not is_port_available(port):
        terminate_process_on_port(port)

    subprocess.run([
        "venv/bin/jupyter" if platform.system() != "Windows" else "venv\\Scripts\\jupyter", 
        "notebook", 
        notebook_path, 
        f"--port={port}", 
        "--ip=127.0.0.1"
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    project_path = os.path.abspath(".")  # Set project path to the current directory
    try:
        navigate_to_project_directory(project_path)
        create_virtual_environment()
        activate_virtual_environment()
        check_python_version()
        install_dependencies()
        start_jupyter_notebook()
    except Exception as e:
        print(f"An error occurred: {e}")
