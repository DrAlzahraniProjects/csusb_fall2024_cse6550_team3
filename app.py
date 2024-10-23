corpus_source = "swebook" # If empty, app will default to using the textbook PDF

import os
os.environ['CORPUS_SOURCE'] = corpus_source

import subprocess
from frontend import streamlit
from backend.statistics import init_db

# Application entrypoint
if __name__ == "__main__":
    if os.environ.get("STREAMLIT_RUNNING") == "1":
        init_db()  # Initialize the database 
        streamlit.main()
    else:
        os.environ["STREAMLIT_RUNNING"] = "1"
        subprocess.run(["streamlit", "run", __file__, "--server.port=5003", "--server.address=0.0.0.0", "--server.baseUrlPath=/team3"])
