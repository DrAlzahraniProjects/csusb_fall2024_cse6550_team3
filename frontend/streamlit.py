
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

def main():
    """Main Streamlit app logic"""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # # Show the title only if there are no messages
    # if not st.session_state.messages:
    st.markdown("<h1 style='text-align: center;'>Textbook Chatbot</h1>", unsafe_allow_html=True)

    # Load PDF
    if "view" in st.query_params and st.query_params["view"] == "pdf":
        serve_pdf()
    else:
        load_css()

        # Create user session
        if "user_id" not in st.session_state:
            st.session_state.user_id = init_user_session()
            print(f"Creating user#{st.session_state.user_id}")

        st.sidebar.empty()
        display_confusion_matrix()
        # update_and_display_statistics()

        # Display messages
        for message in st.session_state.messages:for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.markdown(f"<div class='assistant-message'>{message['content']}</div>", unsafe_allow_html=True)
            conversation_id = message.get("conversation_id", None)
        if conversation_id:
            # Find the corresponding user question
            user_message = next((msg for msg in st.session_state.messages if msg["role"] == "user" and msg["conversation_id"] == conversation_id), None)

            # Initialize is_answerable and set the feedback question appropriately
            is_answerable = None
            if user_message and user_message["content"] in baseline_questions:
                is_answerable = baseline_questions[user_message["content"]]

            feedback_question = "Was this response helpful?"
            if is_answerable is not None:
                feedback_question = (
                    "Did the chatbot correctly answer this answerable question?" if is_answerable
                    else "Did the chatbot correctly answer this unanswerable question?"
                )
            
            st.caption(feedback_question)
            
            # Display feedback option if applicable
            feedback = st.feedback(
                "thumbs",
                key=f"feedback_{conversation_id}",
                on_change=handle_feedback,
                kwargs={"conversation_id": conversation_id}
            )
    else:
        st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)

        # Handle user input
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

                conversation_texts = [prompt + " " + response]
                keywords = extract_keywords(conversation_texts)
                print(f"Extracted Keywords: {keywords}")

            conversation_id = insert_conversation(
                question=prompt,
                response=response,
                citations="",
                model_name=model_name,
                source=os.getenv("CORPUS_SOURCE").split("/")[-1],
                response_time=response_time,
                correct=None,
                user_id=st.session_state.user_id,
                answerable = baseline_questions.get(prompt, None),
                common_topics=keywords
            )

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

            update_user_session(st.session_state.user_id)
            st.rerun()
