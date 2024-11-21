import os
import subprocess
import platform
import socket

# 1. Navigate to your project directory
def navigate_to_project_directory(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"The specified project directory does not exist: {path}")
    os.chdir(path)
    print(f"Navigated to project directory: {path}")

# 2. Create a virtual environment
def create_virtual_environment():
    if not os.path.exists("venv"):
        subprocess.run(["python3", "-m", "venv", "venv"], check=True)
        print("Virtual environment created.")
    else:
        print("Virtual environment already exists.")

# 3. Activate the virtual environment
def activate_virtual_environment():
    system = platform.system()
    if system == "Windows":
        activate_script = ".\\venv\\Scripts\\activate"
    elif system == "Linux" or system == "Darwin":  # Darwin is for macOS
        activate_script = "source venv/bin/activate"
    else:
        raise EnvironmentError("Unsupported operating system.")
    print(f"To activate the virtual environment, run: {activate_script}")

# 4. Ensure Python version is 3.10 or above
def check_python_version():
    result = subprocess.run(["python3", "--version"], capture_output=True, text=True, check=True)
    version = result.stdout.strip()
    print(f"Python version: {version}")
    if not (version.startswith("Python 3.10") or version.startswith("Python 3.11") or version.startswith("Python 3.12")):
        raise EnvironmentError("Python 3.10 or above is required.")

# 5. Install dependencies
def install_dependencies():
    subprocess.run(["venv/bin/pip" if platform.system() != "Windows" else "venv\\Scripts\\pip", "install", "-r", "requirements.txt"], check=True)
    print("Dependencies installed.")

# 6. Activate the virtual environment (again, just a note for the user)
def remind_activate_virtual_environment():
    system = platform.system()
    if system == "Windows":
        activate_script = ".\\venv\\Scripts\\activate"
    elif system == "Linux" or system == "Darwin":  # Darwin is for macOS
        activate_script = "source venv/bin/activate"
    else:
        raise EnvironmentError("Unsupported operating system.")
    print(f"Reminder: Activate the virtual environment by running: {activate_script}")

# Check if a port is available
def is_port_available(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) != 0

# 7. Start Jupyter Notebook on port 6003
def start_jupyter_notebook():
    notebook_path = "jupyter/main.ipynb"
    if not os.path.exists(notebook_path):
        raise FileNotFoundError(f"The specified notebook does not exist: {notebook_path}")

    port = 6003
    while not is_port_available(port):
        print(f"Port {port} is not available. Trying the next port...")
        port += 1

    subprocess.run([
        "venv/bin/jupyter" if platform.system() != "Windows" else "venv\\Scripts\\jupyter", 
        "notebook", 
        notebook_path, 
        f"--port={port}", 
        "--ip=127.0.0.1"
    ], check=True)

if __name__ == "__main__":
    project_path = os.path.abspath(".")  # Set project path to the current directory
    try:
        navigate_to_project_directory(project_path)
        create_virtual_environment()
        activate_virtual_environment()
        check_python_version()
        install_dependencies()
        remind_activate_virtual_environment()
        start_jupyter_notebook()
    except Exception as e:
        print(f"An error occurred: {e}")