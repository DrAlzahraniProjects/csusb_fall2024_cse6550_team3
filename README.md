# Textbook Chatbot (Team 3)

CSE 6550: Software Engineer Concepts, Fall 24

California State University, San Bernardino
## Description
The Textbook Chatbot project for CSE 6550 is designed to assist with queries related to the textbook."Software Engineering: A Practitioner's Approach." The chatbot serves as an educational tool, helping users by providing information, answering questions, and possibly retrieving content from the textbook.

The project involves building a Python-based web application, containerized using Docker for easy deployment. GitHub is used for version control, and GitHub Actions automate Docker publishing. The aim is to streamline access to textbook material, enhancing the learning experience for software engineering students.

## Textbook Reference
Pressman, R. S., & Maxim, B. R. (2020). Software engineering: A practitioner's approach (9th ed.). McGraw-Hill Education.
## Setup
To get started, first clone the repository to your local machine:
```
git clone https://github.com/DrAlzahraniProjects/csusb_fall2024_cse6550_team3.git
```

After cloning the repository, navigate to the project directory:
```
cd csusb_fall2024_cse6550_team3
```

Update Local Repository
```
git pull origin main
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
cd csusb_fall2024_cse6550_team3
```

Pull Changes Directly (Fetch and Merge in one command): 
```
git pull origin main
```
 Force Update (if necessary): Ensures your local repository exactly matches the remote one by discarding any local changes
```
git reset --hard origin/main
```
Verify Your Changes
```
git status
```
To View Recent Commit History:
```
git log
```
