# Textbook Chatbot (Team 3)

CSE 6550: Software Engineer Concepts, Fall 24

California State University, San Bernardino

## Setup
To get started, first clone the repository to your local machine:
```
git clone https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3.git
```

After cloning the repository, navigate to the project directory:
```
cd csusb_fall2024_cse6550_team3
```

Once you are in correct folder, build the Docker image:
```
docker build -t team3-app .
```

Now, run the Docker container:
```
docker run -p 5003:5003 team3-app
```
The application will be available at: http://127.0.0.1:5003/ or http://localhost:5003/

---
## Project Structure

- `.github/workflows/docker-publish.yml`: Defines a GitHub Action workflow to automate Docker publishing
- `.gitignore`: Specifies which files and directories should be ignored by Git
- `Dockerfile`: Contains instructions to build the Docker image for the project
- `README.md`: Project documentation containing setup instructions and information about the project
- `app.py`: Main entry point for the application
- `requirements.txt`: Lists Python package dependencies required for the project

---
## To update local repository

Navigate to Your Local Repository:

```
cd path/to/your/local/repo
```
Fetch the Latest Changes from the Remote Repository
```
git fetch
```
(Optional) Pull Changes Directly
```
git pull
```
Resolve Any Merge Conflicts
```
git add <resolved-file>
git commit
```
Verify Your Changes
```
git status
git log
```

