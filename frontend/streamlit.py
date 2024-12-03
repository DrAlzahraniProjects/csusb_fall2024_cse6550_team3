import os
import time
import streamlit as st
from .pdf import serve_pdf
from .questions import check_baseline_answerable
from backend.inference import chat_completion
from backend.statistics import (
    init_user_session,
    update_user_session,
    insert_conversation,
)
from .utils import (
    load_css,
    handle_feedback,
    get_feedback_question,
    display_confusion_matrix,
)

# Add rate limit constants
MAX_REQUESTS_PER_MINUTE = 10  # 10 requests per minute
BLOCK_DURATION_SECONDS = 3 * 60  # 3 minutes

def check_rate_limit():
    """Check if the user has exceeded the rate limit."""
    now = time.time()
    if "request_timestamps" not in st.session_state:
        st.session_state.request_timestamps = []

    # Remove timestamps older than a minute
    st.session_state.request_timestamps = [
        t for t in st.session_state.request_timestamps if now - t <= 60
    ]

    # Check if the rate limit has been exceeded
    if len(st.session_state.request_timestamps) >= MAX_REQUESTS_PER_MINUTE:
        if "block_until" in st.session_state and st.session_state.block_until > now:
            st.error(
                "You've reached the limit of 10 questions per minute because the server has limited resources. Please try again in 3 minutes."
            )
            st.stop()
        else:
            st.session_state.block_until = now + BLOCK_DURATION_SECONDS
            st.error(
                "You've reached the limit of 10 questions per minute because the server has limited resources. Please try again in 3 minutes."
            )
            st.stop()

    # Add current timestamp to the list
    st.session_state.request_timestamps.append(now)

def initialize_session():
    """Initialize user session if not already initialized."""
    if "user_id" not in st.session_state:
        try:
            st.session_state.user_id = init_user_session()
        except Exception as e:
            st.error("Unable to initialize user session. Please try again later.")
            st.stop()


def render_conversation_history():
    """Render conversation history from the session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        if message["role"] == "assistant":
            render_assistant_message(message)
        else:
            st.markdown(
                f"<div class='user-message'>{message['content']}</div>",
                unsafe_allow_html=True,
            )

def render_assistant_message(message):
    """Render assistant message and feedback options."""
    st.markdown(f"<div class='assistant-message'>{message['content']}</div>", unsafe_allow_html=True)

    # Provide feedback interface
    conversation_id = message.get("conversation_id")
    if conversation_id:
        user_message = next(
            (
                msg
                for msg in st.session_state.messages
                if msg["role"] == "user" and msg.get("conversation_id") == conversation_id
            ),
            None,
        )
        feedback_question = get_feedback_question(
            user_message["answerable"] if user_message else None
        )
        st.caption(feedback_question)
        st.feedback(
            "thumbs",
            key=f"feedback_{conversation_id}",
            on_change=handle_feedback,
            kwargs={"conversation_id": conversation_id},
        )

def handle_user_input(prompt: str):
    """Process user input, generate a response, and update session state."""
    check_rate_limit()
    response_container = st.empty()
    with st.spinner("Generating response..."):
        try:
            response, answerable = generate_response(prompt, response_container)
            conversation_id = save_conversation_to_db(prompt, response, answerable)
            update_session_messages(prompt, response, conversation_id, answerable)
            update_user_session(st.session_state.user_id)
            st.rerun()
        except Exception as e:
            print(f"{e}")
            st.success(f"Our systems are overloaded. Please try again.")


def generate_response(prompt: str, response_container):
    """Generate response for a given user prompt."""
    start_time = time.time()
    response = ""
    answerable = check_baseline_answerable(prompt)
    for partial_response, model_name in chat_completion(prompt):
        response += partial_response
        response_container.markdown(
            f"<div class='assistant-message'>{response}</div>", unsafe_allow_html=True
        )
    end_time = time.time()
    st.session_state.response_time = int(end_time - start_time)
    return response, answerable


def save_conversation_to_db(prompt: str, response: str, answerable: bool) -> int:
    """Save conversation to the database."""
    return insert_conversation(
        question=prompt,
        response=response,
        citations="",  # No need to include highlighting data
        model_name="open-mistral-7b",
        source=os.getenv("CORPUS_SOURCE", "unknown source").split("/")[-1],
        response_time=st.session_state.response_time,
        correct=None,
        user_id=st.session_state.user_id,
        answerable=answerable,
    )


def update_session_messages(prompt: str, response: str, conversation_id: int, answerable: bool):
    """Update session state with user and assistant messages."""
    st.session_state.messages.append(
        {"role": "user", "content": prompt, "conversation_id": conversation_id, "answerable": answerable}
    )
    st.session_state.messages.append(
        {"role": "assistant", "content": response, "conversation_id": conversation_id}
    )


def main():
    """Main application logic."""
    # Initialize session state for tracking whether the app has loaded
    if "app_loaded" not in st.session_state:
        st.session_state.app_loaded = False

    # Display the loading message only if the app has not yet loaded
    if not st.session_state.app_loaded:
        loading_message = st.empty()
        loading_message.markdown("<h2 style='text-align: center;'>Loading the app, please wait...</h2>", unsafe_allow_html=True)
        time.sleep(2) # Simulate a delay for demo purposes (you can remove or adjust this)
        st.session_state.app_loaded = True # Mark the app as loaded in session state
        loading_message.empty() # Clear the loading message

    # Once the app is loaded, display the normal app interface
    st.markdown("<h1 style='text-align: center;'>Textbook Chatbot</h1>", unsafe_allow_html=True)

    # Check for PDF query parameters
    if "view" in st.query_params and st.query_params["view"] == "pdf":
        pdf_path = st.query_params.get("file")
        page = int(st.query_params.get("page", 1))
        serve_pdf(pdf_path, page)
        return

    # Load UI components
    load_css()
    initialize_session()
    st.sidebar.empty()
    display_confusion_matrix()
    render_conversation_history()

    # Process user input
    if prompt := st.chat_input("Ask your question?"):
        st.markdown(f"<div class='user-message'>{prompt}</div>", unsafe_allow_html=True)
        handle_user_input(prompt)
