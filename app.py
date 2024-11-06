import os
import subprocess

# Setting the corpus source for the application
corpus_source = "swebok"  # Guide to the Software Engineering Body of Knowledge
# Alternate corpus source as a comment for easy switching
# corpus_source = "default"  # "Software Engineering: A PRACTITIONER’S APPROACH"

# Configure the corpus source as an environment variable
CORPUS_SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"data/{corpus_source}")
os.environ["CORPUS_SOURCE"] = CORPUS_SOURCE
print(f"\nCorpus source set to: ", CORPUS_SOURCE)

from frontend import streamlit
from backend.statistics import init_db

def main():
    # Initialize the database if it's the first time running
    init_db()

    # Start the Streamlit frontend
    streamlit.main()

if __name__ == "__main__":
    # Check if Streamlit is already running to avoid duplicate processes
    if os.environ.get("STREAMLIT_RUNNING") != "1":
        os.environ["STREAMLIT_RUNNING"] = "1"
        # Start Streamlit as a background process with Nginx-compatible configuration
        subprocess.Popen(["streamlit", "run", __file__, "--server.port=5003", "--server.address=0.0.0.0", "--server.baseUrlPath=/team3"])
        # Start Jupyter Notebook as a background process
        subprocess.run(["jupyter", "notebook", "--ip=0.0.0.0", "--port=6003", "--no-browser", "--allow-root", "--NotebookApp.base_url=/team3/jupyter", "--NotebookApp.token=''", "--NotebookApp.password=''"])
    else:
        # Directly run the Streamlit app if the instance is already running
        main()
