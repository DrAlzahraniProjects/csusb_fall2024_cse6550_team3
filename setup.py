import os
import subprocess
import platform
import sys
import time
import shutil

def run_command(command, error_message):
    """Run a shell command and handle errors."""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"{error_message}: {e}")
        sys.exit(1)

def stop_and_remove_containers(ports):
    """Stop and remove Docker containers running on specific ports."""
    print("Stopping and removing Docker containers on ports:", ports)
    for port in ports:
        try:
            # Find the container ID using the port
            result = subprocess.check_output(f"docker ps -q -f publish={port}", shell=True).decode().strip()
            if result:
                print(f"Stopping container on port {port}...")
                run_command(f"docker stop {result}", f"Failed to stop container on port {port}")
                print(f"Removing container on port {port}...")
                run_command(f"docker rm {result}", f"Failed to remove container on port {port}")
            else:
                print(f"No container found running on port {port}.")
        except subprocess.CalledProcessError as e:
            print(f"Error while checking containers on port {port}: {e}")
            sys.exit(1)

def clone_or_pull_repo(repo_url, repo_dir):
    """Clone the repository if not present; otherwise, pull the latest changes."""
    if not os.path.exists(repo_dir):
        print("Cloning the repository...")
        run_command(f"git clone {repo_url}", "Failed to clone the repository")
    else:
        print("Repository already exists. Pulling the latest changes...")
        os.chdir(repo_dir)
        run_command("git pull origin main", "Failed to pull the latest changes")
        os.chdir("..")

def build_docker_image(repo_dir, mistral_key):
    """Build the Docker image."""
    print("Building the Docker image...")
    os.chdir(repo_dir)
    run_command(f"docker build -t team3-app . --build-arg MISTRAL={mistral_key}", "Failed to build Docker image")
    os.chdir("..")

def display_loading_bar(duration):
    """Display a loading bar with time countdown for a specified duration."""
    print("Waiting for the application to fully load...")
    
    # Get terminal width for a dynamic progress bar
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    bar_width = min(50, terminal_width - 20)  # Adjust bar width dynamically
    
    start_time = time.time()
    while time.time() - start_time < duration:
        elapsed = time.time() - start_time
        progress = elapsed / duration
        completed = int(progress * bar_width)
        remaining = bar_width - completed
        time_left = duration - int(elapsed)
        
        # Build the loading bar
        bar = f"[{'#' * completed}{'.' * remaining}]"
        print(f"\r{bar} {int(progress * 100)}% | {time_left}s remaining", end="")
        time.sleep(0.1)  # Update every 100ms
    
    # Final clear and print
    print(f"\r{' ' * (bar_width + 30)}", end="\r")  # Clear the line
    print(f"[{'#' * bar_width}] 100% | 0s remaining")
    print("Application should now be ready!")

def run_docker_container():
    """Run the Docker container."""
    print("Running the Docker container...")
    run_command("docker run -d -p 5003:5003 team3-app", "Failed to run Docker container")
    print("Docker container started successfully!")
    display_loading_bar(30)  # 30 seconds duration
    print("You can now access the application:")
    print("Website: http://localhost:5003/team3")
    print("Wait 30 seconds more when accessing the webserver.")  # Additional message

def main():
    print("Starting cross-platform automation script.....")
    
    # Step 1: Stop and remove existing Docker containers
    ports = [5003]
    stop_and_remove_containers(ports)

    # Step 2: Clone or pull the repository
    repo_url = "https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3.git"
    repo_dir = "csusb_fall2024_cse6550_team3"
    clone_or_pull_repo(repo_url, repo_dir)

    # Step 3: Build the Docker image
    mistral_key = input("Enter your Mistral API key: ")
    build_docker_image(repo_dir, mistral_key)

    # Step 4: Run the Docker container
    run_docker_container()

if __name__ == "__main__":
    main()
