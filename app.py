corpus_source = "swebok" # Guide to the Software Engineering Body of Knowledge
# corpus_source = "default" # "Software Engineering: A PRACTITIONER’S APPROACH"

import os
# Add corpus source to enviroment variables
if corpus_source != "swebok" and corpus_source != "default":
    corpus_source = "swebok"
CORPUS_SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"data/{corpus_source}")
os.environ["CORPUS_SOURCE"] = CORPUS_SOURCE
print(f"\nCorpus source: ", CORPUS_SOURCE)

import subprocess
from frontend import streamlit
from backend.statistics import init_db

# Application entrypoint
if __name__ == "__main__":
    init_db() # Initialize the database 
    if os.environ.get("STREAMLIT_RUNNING") == "1":
        streamlit.main()
    else:
        os.environ["STREAMLIT_RUNNING"] = "1"
        subprocess.run(["streamlit", "run", __file__, "--server.port=5003", "--server.address=0.0.0.0", "--server.baseUrlPath=/team3"])