import streamlit as st
import os
import subprocess
import sys

def main():
    st.title("Hello World! - Team 3")

if __name__ == "__main__":
    if 'STREAMLIT_RUN' in os.environ:
        main()
    else:
        # Set environment variable for Streamlit execution
        os.environ['STREAMLIT_RUN'] = 'true'
        
        # Run Streamlit as a subprocess
        subprocess.run(["streamlit", "run", __file__, "--server.port=5003"], check=True)
