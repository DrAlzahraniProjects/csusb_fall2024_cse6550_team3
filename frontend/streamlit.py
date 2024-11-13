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
    "What is software quality?": True,
    "What is agile approach?": True,
    "How does the Agile approach impact software quality?": True,
    "What is software testing process?": True,
    "What is ROI?": True,
    "What is a Quality Management System (QMS) in software?": True,
    "What are some key challenges to ensuring software quality?": True,
    "How do risk management and SQA interact in projects?": True,
    "How does testability affect software testing processes?": True,

    # 10 Unanswerable Questions
    "How many defects will occur in a specific software project?": False,
    "What is the cost of nonconformance for a project?": False,
    "How will a new process affect software defect rates?": False,
    "What is the probability of a defect reoccurring in software?": False,
    "How long will it take to resolve defects from an audit?": False,
    "What level of software quality is `good enough` for stakeholders?": False,
    "What is the future impact of AI on software quality standards?": False,
    "What ROI will be achieved through additional SQA measures?": False,
    "What specific changes improve software quality across all projects?": False,
    "How many resources are needed to achieve a quality level?": False
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
