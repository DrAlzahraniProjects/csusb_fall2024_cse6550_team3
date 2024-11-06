import os
import subprocess

def setup_environment():
    corpus_source = "swebok"  # default corpus
    if corpus_source not in ["swebok", "default"]:
        corpus_source = "swebok"
    corpus_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"data/{corpus_source}")
    os.environ["CORPUS_SOURCE"] = corpus_path
    print(f"Corpus source set to: {corpus_path}")

def start_streamlit():
    streamlit_cmd = [
        "streamlit", "run", __file__,
        "--server.port=5003",
        "--server.address=0.0.0.0",
        "--server.baseUrlPath=/team3"
    ]
    subprocess.Popen(streamlit_cmd)
    print("Streamlit started...")

def start_jupyter():
    jupyter_cmd = [
        "jupyter", "notebook",
        "--ip=0.0.0.0",
        "--port=6003",
        "--no-browser",
        "--allow-root",
        "--NotebookApp.base_url=/team3/jupyter",
        "--NotebookApp.token=''",
        "--NotebookApp.password=''"
    ]
    subprocess.run(jupyter_cmd)
    print("Jupyter Notebook started...")

def main():
    setup_environment()
    from backend.statistics import init_db
    from frontend import streamlit

    # Initialize the database
    init_db()

    # Check if Streamlit is running to prevent multiple instances
    if os.environ.get("STREAMLIT_RUNNING") != "1":
        os.environ["STREAMLIT_RUNNING"] = "1"
        start_streamlit()
        start_jupyter()
    else:
        # Main application logic
        streamlit.main()

if __name__ == "__main__":
    main()
