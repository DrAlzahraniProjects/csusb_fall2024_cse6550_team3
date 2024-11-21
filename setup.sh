#!/bin/bash

# Function to display progress bar
show_progress() {
  local duration=$1
  local interval=1
  local elapsed=0

  echo -ne "["
  while [ $elapsed -lt $duration ]; do
    echo -ne "#"
    sleep $interval
    ((elapsed+=interval))
  done
  echo -e "]"
}

# Step 1: Delete existing Docker containers running on port 5003 or 6003
echo "Stopping and removing existing Docker containers on ports 5003 and 6003..."
for port in 5003 6003; do
  container_id=$(docker ps -q --filter "publish=$port")
  if [ -n "$container_id" ]; then
    echo "Stopping container on port $port..."
    docker stop $container_id
    echo "Removing container on port $port..."
    docker rm $container_id
  else
    echo "No containers found running on port $port."
  fi
done

# Step 2: Download the repository from GitHub
repo_url="https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3.git"
repo_dir="csusb_fall2024_cse6550_team3"

if [ ! -d "$repo_dir" ]; then
  echo "Cloning the repository..."
  git clone $repo_url
else
  echo "Repository already exists. Pulling the latest changes..."
  cd $repo_dir || exit
  git pull origin main
  cd ..
fi

# Step 3: Build the Docker image
echo "Building the Docker image..."
read -p "Enter your Mistral API key: " mistral_key
cd $repo_dir || exit
docker build -t team3-app . --build-arg MISTRAL="$mistral_key"

# Step 4: Run the Docker container
echo "Running the Docker container..."
docker run -d -p 5003:5003 -p 6003:6003 team3-app
