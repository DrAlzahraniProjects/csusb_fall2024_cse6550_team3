import os
import time
import streamlit as st
from .pdf import serve_pdf
from backend.inference import chat_completion
from backend.statistics import (
    init_user_session,
    update_user_session,
    insert_conversation,
)
from .utils import (
    baseline_questions,
    load_css,
    update_and_display_statistics,
    display_confusion_matrix,
    handle_feedback,
    extract_keywords
)

def load_css(file_name):
    """Load and apply CSS styles."""
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def display_statistics(stat_view):
    """Displays non-interactive statistics in the sidebar based on the selected view (Daily or Overall)."""
    st.sidebar.markdown("<h2>Statistics</h2>", unsafe_allow_html=True)
    
    # Example statistics data; replace with actual data retrieval if available
    stats = {
        "Number of questions": "100",
        "Number of correct answers": "85",
        "Number of incorrect answers": "15",
        "User engagement metrics": "High",
        "Response time analysis": "Average 1.2s",
        "Accuracy rate": "85%",
        "Common topics or keywords": "Physics, Chemistry, Mathematics",
        "User satisfaction ratings": "4.5/5",
        "Improvement over time": "Consistent",
        "Feedback summary": "Positive"
    }
    
    for label, value in stats.items():
        st.sidebar.markdown(
            f"<div class='stat-label'>{label}</div>"
            f"<div class='stat-value'>{value}</div>",
            unsafe_allow_html=True
        )
    
    st.sidebar.markdown(f"<h3>{stat_view} Statistics</h3>", unsafe_allow_html=True)

def main():
    """Main Streamlit app logic."""
    # Load custom CSS for styling
    load_css("style.css")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show the title only if there are no messages
    if not st.session_state.messages:
        st.markdown("<h1 style='text-align: center;'>Textbook Chatbot</h1>", unsafe_allow_html=True)

    # Load PDF view if specified
    if "view" in st.query_params and st.query_params["view"] == "pdf":
        serve_pdf()
    else:
        # Create a user session if it doesn't already exist
        if "user_id" not in st.session_state:
            st.session_state.user_id = init_user_session()
            print(f"Creating user#{st.session_state.user_id}")

        # Sidebar with toggle for statistics view
        stat_view = st.sidebar.radio("View Statistics", options=["Daily", "Overall"], index=0, key="stat_view")
        display_statistics(stat_view)  # Display non-interactive statistics based on selected view

        display_confusion_matrix()

        # Display chat messages
        for message in st.session_state.messages:
            if message["role"] == "assistant":
                st.markdown(f"<div class='assistant-message'>{message['content']}</div>", unsafe_allow_html=True)
                conversation_id = message.get("conversation_id", None)
                if conversation_id:
                    st.caption("Was this response helpful?")
                    st.feedback(
                        "thumbs",
                        key=f"feedback_{conversation_id}",
                        on_change=handle_feedback,
                        kwargs={"conversation_id": conversation_id}
                    )
            else:
                st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)

        # Handle user input and generate a response
        if prompt := st.chat_input("Ask your question?"):
            st.markdown(f"<div class='user-message'>{prompt}</div>", unsafe_allow_html=True)
            
            response_container = st.empty()
            with st.spinner("Generating response..."):
                start_time = time.time()
                response = ""
                for partial_response, model_name in chat_completion(prompt):
                    response += partial_response
                    response_container.markdown(f"<div class='assistant-message'>{response}</div>", unsafe_allow_html=True)
                end_time = time.time()
                response_time = int((end_time - start_time))

                # Extract keywords from the conversation for analysis
                conversation_texts = [prompt + " " + response]
                keywords = extract_keywords(conversation_texts)
                print(f"Extracted Keywords: {keywords}")

            # Insert conversation data into the database
            conversation_id = insert_conversation(
                question=prompt,
                response=response,
                citations="",
                model_name=model_name,
                source=os.getenv("CORPUS_SOURCE").split("/")[-1],
                response_time=response_time,
                correct=None,
                user_id=st.session_state.user_id,
                answerable=baseline_questions.get(prompt, None),
                common_topics=keywords
            )

            # Append messages to session state
            st.session_state.messages.append({
                "role": "user",
                "content": prompt,
                "conversation_id": conversation_id,
            })
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "conversation_id": conversation_id
            })

            # Update user session and rerun the app to display new messages
            update_user_session(st.session_state.user_id)
            st.rerun()

if __name__ == "__main__":
    main()
