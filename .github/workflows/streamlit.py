import os
import time
import streamlit as st
from backend.statistics import (
    init_user_session, 
    update_user_session, 
    insert_conversation, 
    get_statistics,
    toggle_correctness
)
from backend.inference import chat_completion
from app import corpus_source
from .pdf import serve_pdf

def load_css():
    """Load CSS styles"""
    css_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles", "style.css")
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def update_and_display_statistics():
    """Updates statistics report in the left sidebar based on selected period (Daily/Overall)"""
    
    st.sidebar.markdown("<h1 class='title-stat'>Statistics Reports</h1>", unsafe_allow_html=True)
    
    # Daily/Overall toggle buttons with centered alignment
    stat_period = st.sidebar.radio(
        "Statistics period (Daily or Overall)",
        ('Daily', 'Overall'),
        key="stats_period",
        label_visibility="hidden",
        horizontal=True
    )
    
    # Retrieve statistics based on selected period
    stats = get_statistics(stat_period)
    st.session_state.statistics = stats
    
    # List of statistics to display
    statistics = [
        f"Number of questions: {stats['num_questions']}",
        f"Number of correct answers: {stats['num_correct']}",
        f"Number of incorrect answers: {stats['num_incorrect']}",
        f"User engagement metrics: {stats['user_engagement']:.2f} seconds",
        f"Response time analysis: {stats['avg_response_time']:.2f} seconds",
        f"Accuracy rate: {stats['accuracy_rate']:.2f}%",
        f"Satisfaction rate: {stats['satisfaction_rate']:.2f}%",
        "Common topics or keywords",
        "Improvement over time",
        "Feedback summary"
    ]
    
    # Display each stat as simple text in the sidebar
    for stat in statistics:
        st.sidebar.markdown(f"<div class='stat-display'>{stat}</div>", unsafe_allow_html=True)

def handle_feedback(conversation_id):
    """Handle feedback button click"""
    feedback_value = st.session_state.get(f"feedback_{conversation_id}", None)
    if feedback_value is not None:
        toggle_correctness(conversation_id, feedback_value == 1)
        update_user_session(st.session_state.user_id)

def main():
    """Main Streamlit app logic."""
    # Create the title
    header = st.container()
    header.title("Textbook Chatbot")
    header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

    # Load PDF
    if "view" in st.query_params and st.query_params["view"] == "pdf":
        serve_pdf()
    # Load Homepage
    else:
        # Load the CSS file
        load_css()

        # Create user session
        if "user_id" not in st.session_state:
            st.session_state.user_id = init_user_session()
            print(f"Creating user#{st.session_state.user_id}")
        
        # Create sidebar with statistics
        st.sidebar.empty()
        update_and_display_statistics()

        # Load user/assistant messages and feedback icons when appropriate
        if "messages" not in st.session_state:
            st.session_state.messages = []
        for message in st.session_state.messages:
            if message["role"] == "assistant":
                st.markdown(f"<div class='assistant-message'>{message['content']}</div>", unsafe_allow_html=True)
                conversation_id = message.get("conversation_id", None)
                if conversation_id:
                    st.caption("Was this response helpful?")
                    feedback = st.feedback(
                        "thumbs",
                        key=f"feedback_{conversation_id}",
                        on_change=handle_feedback,
                        kwargs={"conversation_id": conversation_id}
                    )
            else:
                st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)

        # Handle user prompts
        if prompt := st.chat_input("Ask your question?"):
            st.markdown(f"<div class='user-message'>{prompt}</div>", unsafe_allow_html=True)

            # Model inference with streaming
            response_container = st.empty()  # Placeholder for the assistant's response
            with st.spinner("Generating response..."):
                start_time = time.time()
                response = ""  # To accumulate the response in pieces
                for partial_response, model_name in chat_completion(prompt):  # Streaming from the model
                    response += partial_response  # Accumulate partial responses
                    response_container.markdown(f"<div class='assistant-message'>{response}</div>", unsafe_allow_html=True)
                end_time = time.time()
                response_time = int((end_time - start_time))  # seconds

            # Add conversation to DB
            conversation_id = insert_conversation(
                question=prompt,
                response=response,
                citations="",
                model_name=model_name,
                response_time=response_time,  # seconds
                correct=None,  # No feedback by default
                user_id=st.session_state.user_id,
                common_topics=""
            )

            # Add conversation to streamlit session state
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

            # Update user session and rerun streamlit
            update_user_session(st.session_state.user_id)
            st.rerun()
