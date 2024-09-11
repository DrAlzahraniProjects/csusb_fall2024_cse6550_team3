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
docker build -t textbookrag .
```

Now, run the Docker container:
```
docker run -p 5003:8501 textbookrag
```
The application will be available at: http://127.0.0.1:5003/ or http://localhost:5003/

---
## Project Structure

- `.gitignore`: List files that Git should ignore
- `app.py`: Application entry point
- `Dockerfile`: Defines instructions to build the Docker image
- `environment.yml`: Specifies the Mamba environment for the project
- `requirements.txt`: Lists Python package dependencies

---
## To update local repository

Navigate to Your Local Repository:

```
cd path/to/your/repo
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

