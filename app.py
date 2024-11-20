corpus_source = "swebok" # Guide to the Software Engineering Body of Knowledge
# corpus_source = "default" # "Software Engineering: A PRACTITIONER’S APPROACH"

import os

# Add corpus source to enviroment variables
CORPUS_SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"data/{corpus_source}")
os.environ["CORPUS_SOURCE"] = CORPUS_SOURCE
print(f"\nCorpus source: ", CORPUS_SOURCE)

import subprocess
from frontend import streamlit
from backend.statistics import init_db

# Application entrypoint
if __name__ == "__main__":
    # If Streamlit instance is running
    if os.environ.get("STREAMLIT_RUNNING") == "1":
        # Initialize the database
        init_db()
        # Start the Streamlit frontend
        streamlit.main()
    else:
        # Set the environment variable to indicate Streamlit is running
        os.environ["STREAMLIT_RUNNING"] = "1"    
        # Start Streamlit as a background process
        subprocess.Popen(["streamlit", "run", __file__,"--server.port=5003", "--server.address=0.0.0.0", "--server.baseUrlPath=/team3"])
        # Start Jupyter Notebook
        subprocess.run(["jupyter", "notebook","--ip=0.0.0.0", "--port=6003","--no-browser", "--allow-root","--NotebookApp.base_url=/team3/jupyter","--NotebookApp.token=''", "--NotebookApp.password=''", "--notebook-dir=/app/jupyter"])
