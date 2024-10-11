# app.py
import os
import time
import subprocess
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from inference import chat_completion

TEXTBOOK_PATH = os.path.join(os.path.dirname(__file__), "data", "textbook")
def serve_pdf():
	"""Display Textbook"""
    file = st.query_params.get("file")
    page = int(st.query_params.get("page", 1))

    if file:
        pdf_path = os.path.join(TEXTBOOK_PATH, file)
        if os.path.exists(pdf_path):
            with st.spinner(f"Loading page {page} of the PDF..."):
                pdf_viewer(
                    pdf_path,
                    width=700,
                    height=1000,
                    pages_to_render=[page],
                    scroll_to_page=page
                )
        else:
            st.error(f"PDF file not found at {pdf_path}")
    else:
        st.error("No PDF file specified in query parameters")

def main():
	"""Main Streamlit app logic."""
	if "view" in st.query_params and st.query_params["view"] == "pdf":
		serve_pdf()
	else:
		header = st.container()

		def load_css(file_name):
			with open(file_name) as f:
				st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

		# Load the CSS file
		load_css("Styles/style.css")

		header.title("Textbook Chatbot")
		header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

		# Sidebar for chat history and statistics
		st.sidebar.markdown(f'<h1 class="title-stat">Statistics Reports</h1>', unsafe_allow_html=True)

		# List of statistics to display
		statistics = [
			"Number of correct answers",
			"Number of incorrect answers",
			"User engagement metrics",
			"Response time analysis",
			"Accuracy rate",
			"Common topics or keywords",
			"User satisfaction ratings",
			"Improvement over time",
			"Feedback summary",
			"Statistics per day and overall"
		]

		# Display statistics in the sidebar
		for stat in statistics:
			st.sidebar.markdown(f"""
				<div class='btn-stat-container'>
					<a href="#" class="btn-stat">{stat}</a>
				</div>
			""", unsafe_allow_html=True)

		if "messages" not in st.session_state:
			st.session_state.messages = []

		# Render existing messages
		for message in st.session_state.messages:
			if message["role"] == "assistant":
				st.markdown(f"<div class='assistant-message'>{message['content']}</div>", unsafe_allow_html=True)
			else:
				st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)

		# Handle user input
		if prompt := st.chat_input("Ask your question?"):
			st.session_state.messages.append({"role": "user", "content": prompt})
			st.markdown(f"<div class='user-message'>{prompt}</div>", unsafe_allow_html=True)

			# Show spinner while generating response
			with st.spinner("Generating response..."):
				time.sleep(2)  # Increase this value to extend the spinner display time
				response = chat_completion(prompt) # Get response using chat_completion

			st.session_state.messages.append({"role": "assistant", "content": response})

			st.markdown(f"""
				<div class='assistant-message'>
					{response}
					<div class='feedback-buttons'>
						<span class='feedback-icon'>👍</span>
						<span class='feedback-icon'>👎</span>
					</div>
				</div>
			""", unsafe_allow_html=True)

if __name__ == "__main__":
	if os.environ.get("STREAMLIT_RUNNING") == "1":
		main()
	else:
		os.environ["STREAMLIT_RUNNING"] = "1"  # Set the environment variable to indicate Streamlit is running
		subprocess.run(["streamlit", "run", __file__, "--server.port=5003", "--server.address=0.0.0.0", "--server.baseUrlPath=/team3"])

		# # Check if PROD environment variable is not set to 1
		# if os.environ.get("PROD") != "1":
		#     jupyter_process = subprocess.Popen(["jupyter", "notebook", "--ip=0.0.0.0", "--port=6003", "--no-browser", "--allow-root", "--NotebookApp.token=''" ,"--NotebookApp.password=''"])