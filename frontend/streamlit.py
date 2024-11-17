import os
import time
import streamlit as st
from .pdf import serve_pdf
from backend.inference import chat_completion
from backend.statistics import (
    init_user_session,
    update_user_session,
    insert_conversation
)
from .utils import (
    load_css,
    update_and_display_statistics,
    handle_feedback,
    display_confusion_matrix
)

baseline_questions = {
    # 10 Answerable questions
    "Who is Hironori Washizaki?": True,
    "How does software testing impact the overall software development lifecycle?": True,
    "What is the agile methodology?": True,
    "What are the different types of software models, and when should each be used?": True,
    "How does software configuration management ensure project success?": True,
    "What role do user requirements play in software design and architecture?": True,
    "How can software engineering practices be adapted for agile development?": True,
    "How does project management in software engineering differ from traditional project management?": True,
    "What strategies can be used for effective risk management in software engineering projects?": True,
    "What is software testing process?": True,

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

def main():
    """Main Streamlit app logic"""
    # Application Title
    st.markdown("<h1 style='text-align: center;'>Textbook Chatbot</h1>", unsafe_allow_html=True)

    # Load PDF if requested
    if "view" in st.query_params and st.query_params["view"] == "pdf":
        serve_pdf()
    else:
        load_css()

        # Create a new user session if one doesn't already exist
        if "user_id" not in st.session_state:
            st.session_state.user_id = init_user_session()
            print(f"Creating user#{st.session_state.user_id}")

        st.sidebar.empty()
        display_confusion_matrix()

        # Display the conversation history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        for message in st.session_state.messages:
            if message["role"] == "assistant":
                st.markdown(f"<div class='assistant-message'>{message['content']}</div>", unsafe_allow_html=True)
                conversation_id = message.get("conversation_id", None)
                if conversation_id:
                    # Find the corresponding user question
                    user_message = next((msg for msg in st.session_state.messages if msg["role"] == "user" and msg["conversation_id"] == conversation_id), None)
                    # Set feedback question based on baseline question type
                    feedback_question = "Was this response helpful?"
                    if user_message and user_message["content"] in baseline_questions:
                        is_answerable = baseline_questions[user_message["content"]]
                        feedback_question = (
                            "Did the chatbot correctly answer this answerable question?" if is_answerable
                            else "Did the chatbot correctly answer this unanswerable question?"
                        )
                    # Display feedback caption
                    st.caption(feedback_question)
                    # Display feedback option
                    feedback = st.feedback(
                        "thumbs",
                        key=f"feedback_{conversation_id}",
                        on_change=handle_feedback,
                        kwargs={"conversation_id": conversation_id}
                    )
            else:
                st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)

        # Handle user input and display response
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

                # Extract keywords (Not required)
                # conversation_texts = [prompt + " " + response]
                # keywords = extract_keywords(conversation_texts)
                # print(f"Extracted Keywords: {keywords}")

            # Add conversation to database
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
            )

            # Append the new conversation to session state
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

            # Update the user session
            update_user_session(st.session_state.user_id)
            st.rerun()
