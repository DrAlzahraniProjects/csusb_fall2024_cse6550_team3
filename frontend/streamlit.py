import os
import time
import streamlit as st
from .pdf import serve_pdf, serve_pdf_with_highlight
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
    display_confusion_matrix
)

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
    st.markdown(f"<div class='assistant-message'>{message['content']}</div>",unsafe_allow_html=True,)

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
            user_message["content"] if user_message else ""
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
    response_container = st.empty()
    with st.spinner("Generating response..."):
        try:
            response = generate_response(prompt, response_container)
            conversation_id = save_conversation_to_db(prompt, response)
            update_session_messages(prompt, response, conversation_id)
            update_user_session(st.session_state.user_id)
            st.rerun()
        except Exception as e:
            st.error(f"Error generating or saving response. Please try again. \nError: {e}")


def generate_response(prompt: str, response_container):
    """Generate response for a given user prompt."""
    start_time = time.time()
    response = ""
    for partial_response, model_name in chat_completion(prompt):
        response += partial_response
        response_container.markdown(
            f"<div class='assistant-message'>{response}</div>", unsafe_allow_html=True
        )
    end_time = time.time()
    st.session_state.response_time = int(end_time - start_time)
    return response


def save_conversation_to_db(prompt: str, response: str) -> int:
    """Save conversation to the database."""
    answerable = check_baseline_answerable(prompt)
    return insert_conversation(
        question=prompt,
        response=response,
        citations="",
        model_name="open-mistral-7b",
        source=os.getenv("CORPUS_SOURCE", "unknown source").split("/")[-1],
        response_time=st.session_state.response_time,
        correct=None,
        user_id=st.session_state.user_id,
        answerable=answerable
    )


def update_session_messages(prompt: str, response: str, conversation_id: int):
    """Update session state with user and assistant messages."""
    st.session_state.messages.append(
        {"role": "user", "content": prompt, "conversation_id": conversation_id}
    )
    st.session_state.messages.append(
        {"role": "assistant", "content": response, "conversation_id": conversation_id}
    )


def main():
    """Main application logic."""
    st.markdown("<h1 style='text-align: center;'>Textbook Chatbot</h1>", unsafe_allow_html=True)

    # Check for PDF query parameters
    if "view" in st.query_params and st.query_params["view"] == "pdf":
        pdf_path = st.query_params.get("file")
        page = int(st.query_params.get("page", 1))
        text_to_highlight = st.query_params.get("highlight", "")

        if text_to_highlight:
            serve_pdf_with_highlight(text_to_highlight, pdf_path, page)
        else:
            serve_pdf()
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
