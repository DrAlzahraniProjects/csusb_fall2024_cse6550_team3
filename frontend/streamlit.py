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
    load_css,
    update_and_display_statistics,
    handle_feedback,
    display_confusion_matrix,
)

# Define constants for baseline questions
BASELINE_QUESTIONS = {
    # 10 Answerable questions
    "Who is Hironori Washizaki?": True,
    "What is software quality?": True,
    "What is the agile methodology?": True,
    "How does the agile methodology impact software quality?": True,
    "What is software testing process?": True,
    "What is the purpose of a task network in project scheduling?": True,
    "What is a Quality Management System (QMS) in software?": True,
    "What are some key challenges to ensuring software quality?": True,
    "How do risk management and SQA interact in projects?": True,
    "How does testability affect software testing processes?": True,

    # 10 Unanswerable Questions
    "How many developers are ideal for any given software project?": False,
    "Can all software bugs be prevented with enough testing?": False,
    "What is the exact ROI of refactoring legacy code?": False,
    "How long should code reviews ideally take for maximum effectiveness?": False,
    "Is there a universally best way to measure developer productivity?": False,
    f"Can software be made 100% secure?": False,
    "Is there a way to build a fully self-sustaining human colony on Mars with current technology?": False,
    "What's the upper limit of computational power for classical computers?": False,
    "How could we fully eliminate all types of noise in wireless communications?": False,
    "Is there a way to completely avoid all cyber threats in interconnected global networks?": False

}

def get_feedback_question(prompt: str) -> str:
    """Return feedback question based on baseline questions."""
    if prompt in BASELINE_QUESTIONS:
        is_answerable = BASELINE_QUESTIONS[prompt]
        return (
            "Did the chatbot correctly answer this answerable question?"
            if is_answerable
            else "Did the chatbot correctly answer this unanswerable question?"
        )
    return "Was this response helpful?"

def initialize_session():
    """Initialize user session and handle errors."""
    if "user_id" not in st.session_state:
        try:
            st.session_state.user_id = init_user_session()
            print(f"Creating user#{st.session_state.user_id}")
        except Exception as e:
            st.error("Unable to initialize user session. Please try again later.")
            st.stop()

def render_conversation_history():
    """Render conversation history from session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        if message["role"] == "assistant":
            render_assistant_message(message)
        else:
            st.markdown(
                f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True
            )

def render_assistant_message(message):
    """Render assistant's message and feedback options."""
    st.markdown(
        f"<div class='assistant-message'>{message['content']}</div>", unsafe_allow_html=True
    )
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
    """Process user input, generate response, and update session state."""
    response_container = st.empty()
    with st.spinner("Generating response..."):
        try:
            response = generate_response(prompt, response_container)
            conversation_id = save_conversation_to_db(prompt, response)
            update_session_messages(prompt, response, conversation_id)
            update_user_session(st.session_state.user_id)
            st.rerun()
        except Exception as e:
            st.error("Error generating or saving response. Please try again.")

def generate_response(prompt: str, response_container):
    """Generate chatbot response and update UI in real-time."""
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
    """Save conversation to the database and return conversation ID."""
    return insert_conversation(
        question=prompt,
        response=response,
        citations="",
        model_name="open-mistral-7b",
        source=os.getenv("CORPUS_SOURCE", "unknown source").split("/")[-1],
        response_time=st.session_state.response_time,
        correct=None,
        user_id=st.session_state.user_id,
        answerable=BASELINE_QUESTIONS.get(prompt, None),
    )

def update_session_messages(prompt: str, response: str, conversation_id: int):
    """Update session state with new conversation."""
    st.session_state.messages.append(
        {"role": "user", "content": prompt, "conversation_id": conversation_id}
    )
    st.session_state.messages.append(
        {"role": "assistant", "content": response, "conversation_id": conversation_id}
    )

def main():
    """Main Streamlit app logic."""
    st.markdown(
        "<h1 style='text-align: center;'>Textbook Chatbot</h1>", unsafe_allow_html=True
    )

    if "view" in st.query_params and st.query_params["view"] == "pdf":
        serve_pdf()
        return

    load_css()
    initialize_session()
    st.sidebar.empty()
    display_confusion_matrix()
    render_conversation_history()

    if prompt := st.chat_input("Ask your question?"):
        st.markdown(
            f"<div class='user-message'>{prompt}</div>", unsafe_allow_html=True
        )
        handle_user_input(prompt)