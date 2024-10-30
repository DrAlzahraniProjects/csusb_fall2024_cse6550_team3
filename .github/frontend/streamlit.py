import os
import time
import streamlit as st
import yake
from backend.statistics import (
    init_user_session, 
    update_user_session, 
    insert_conversation, 
    get_statistics,
    toggle_correctness
)
from backend.inference import chat_completion
from .pdf import serve_pdf

def load_css():
    """Load CSS styles and set theme attribute based on dark mode"""
    css_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles", "style.css")
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    # Detect theme and set data-theme attribute
    theme = "dark" if st.get_option("theme.base") == "dark" else "light"
    st.markdown(f'<html data-theme="{theme}"></html>', unsafe_allow_html=True)

def update_and_display_statistics():
    """Updates statistics report in the left sidebar based on selected period (Daily/Overall)"""

    # Add the title with dynamic color handling in CSS
    st.sidebar.markdown("<h1 class='title-stat'>Statistics Reports</h1>", unsafe_allow_html=True)
    
    # Centered Daily/Overall toggle buttons within a container div
    st.sidebar.markdown("<div class='stat-period-radio-container'>", unsafe_allow_html=True)
    stat_period = st.radio(
        "Statistics period (Daily or Overall)",
        ('Daily', 'Overall'),
        key="stats_period",
        label_visibility="collapsed",
        horizontal=True
    )
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    # Get statistics based on the selected period
    stats = get_statistics(stat_period)
    st.session_state.statistics = stats

    # List of statistics to display as plain text with framed background
    statistics = [
        f"Number of questions: {stats['num_questions']}",
        f"Number of correct answers: {stats['num_correct']}",
        f"Number of incorrect answers: {stats['num_incorrect']}",
        f"User engagement metrics: {stats['user_engagement']:.2f} seconds",
        f"Response time analysis: {stats['avg_response_time']:.2f} seconds",
        f"Accuracy rate: {stats['accuracy_rate']:.2f}%",
        f"Satisfaction rate: {stats['satisfaction_rate']:.2f}%",
        f"Common topics or keywords: {stats['common_topics']}",
        f"Improvement over time",
        f"Feedback summary"
    ]
    
    # Display each statistic as framed text (non-interactive)
    for stat in statistics:
        st.sidebar.markdown(f"""
            <div class='stat-item'>{stat}</div>
        """, unsafe_allow_html=True)

def handle_feedback(conversation_id):
    """Handle feedback button click"""
    feedback_value = st.session_state.get(f"feedback_{conversation_id}", None)
    if feedback_value is not None:
        toggle_correctness(conversation_id, feedback_value == 1)
        update_user_session(st.session_state.user_id)

def extract_keywords(texts):
    """Extract top N keywords from text using YAKE"""
    # Create a YAKE extractor
    extractor = yake.KeywordExtractor(lan="en", n=1, features=None)
    ignore_words = {
        'pdf', 'education', 'engineering', 'software', 'practitioner', 'bruce', 'file', 'maxim', 'roger', 'view',
        'details', 'level', 'target', 'blank', 'page', 'href', 'pressman', 'detail', 'system', 'systems'
    }
    # Extract keywords for each text
    keywords = set()  # Use a set to avoid duplicates
    for text in texts:
        extracted = dict(extractor.extract_keywords(text)).keys()
        # Convert extracted keywords to lowercase before filtering
        filtered_keywords = {word.lower() for word in extracted if word.lower() not in ignore_words}
        keywords.update(filtered_keywords)
    return ", ".join(list(keywords))

def main():
    """Main Streamlit app logic"""
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
        
        # Create sidebar
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

                # Extract keywords from the prompt and response
                conversation_texts = [prompt + " " + response]  # Combine prompt and response
                keywords = extract_keywords(conversation_texts)
                print(f"Extracted Keywords: {keywords}")

            # Insert conversation to database
            conversation_id = insert_conversation(
                question=prompt,
                response=response,
                citations="",
                model_name=model_name,
                response_time=response_time, # seconds
                correct=None,  # No feedback by default
                user_id=st.session_state.user_id,
                common_topics=keywords
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
