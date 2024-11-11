import os
import time
import streamlit as st
from .pdf import serve_pdf
from backend.inference import chat_completion
from backend.statistics import (
    init_user_session,
    update_user_session,
    insert_conversation,
    get_confusion_matrix,
    reset_confusion_matrix
)
from .utils import (
    baseline_questions,
    load_css,
    handle_feedback,
    extract_keywords
)

def display_custom_confusion_matrix(matrix, metrics):
    """Displays the confusion matrix and metrics in the sidebar with standardized labels."""
    st.sidebar.markdown("## Confusion Matrix")
    
    # Highlighted labels for Sensitivity and Specificity above the table
    st.sidebar.markdown(
        f"""
        <div class="highlight-label">
            <p><strong>Sensitivity:</strong> {metrics['Sensitivity']:.2f}</p>
            <p><strong>Specificity:</strong> {metrics['Specificity']:.2f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Display confusion matrix
    st.sidebar.markdown(
        """
        <table class="confusion-matrix-table">
            <tr>
                <th></th>
                <th>Pred. Ans</th>
                <th>Pred. Unans</th>
            </tr>
            <tr>
                <th>Actual Ans</th>
                <td>{tp} (TP)</td>
                <td>{fn} (FN)</td>
            </tr>
            <tr>
                <th>Actual Unans</th>
                <td>{fp} (FP)</td>
                <td>{tn} (TN)</td>
            </tr>
        </table>
        """.format(
            tp=matrix['tp'],
            fn=matrix['fn'],
            fp=matrix['fp'],
            tn=matrix['tn']
        ),
        unsafe_allow_html=True
    )

    # Display remaining metrics below the table
    st.sidebar.markdown(
        f"""
        <div class="metrics-label">
            <p><strong>Accuracy:</strong> {metrics['Accuracy']:.2f}</p>
            <p><strong>Precision:</strong> {metrics['Precision']:.2f}</p>
            <p><strong>F1 Score:</strong> {metrics['F1 Score']:.2f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Reset button
    if st.sidebar.button("Reset"):
        reset_confusion_matrix()
        st.experimental_rerun()

def main():
    """Main Streamlit app logic"""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show the title at the top of the app
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

        # Fetch and display the custom confusion matrix with actual data
        confusion_matrix_data = get_confusion_matrix()
        display_custom_confusion_matrix(confusion_matrix_data['matrix'], confusion_matrix_data['metrics'])

        # Display the conversation history
        for message in st.session_state.messages:
            if message["role"] == "assistant":
                st.markdown(f"<div class='assistant-message'>{message['content']}</div>", unsafe_allow_html=True)
                conversation_id = message.get("conversation_id", None)
                if conversation_id:
                    # Find the corresponding user message
                    user_message = next((msg for msg in st.session_state.messages if msg["role"] == "user" and msg["conversation_id"] == conversation_id), None)
                    
                    # Determine if the question is answerable
                    is_answerable = None
                    if user_message and user_message["content"] in baseline_questions:
                        is_answerable = baseline_questions[user_message["content"]]

                    # Set the feedback question based on whether the question is answerable
                    feedback_question = "Was this response helpful?"
                    if is_answerable is not None:
                        feedback_question = (
                            "Did the chatbot correctly answer this answerable question?" if is_answerable
                            else "Did the chatbot correctly identify this as an unanswerable question?"
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

        # Handle user input and generate responses
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

                # Extract keywords
                conversation_texts = [prompt + " " + response]
                keywords = extract_keywords(conversation_texts)
                print(f"Extracted Keywords: {keywords}")

            # Add conversation to database
            conversation_id = insert_conversation(
                question=prompt,
                response=response,
                citations="",
                model_name=model_name,
                source=os.getenv("CORPUS_SOURCE").split("/")[-1] if os.getenv("CORPUS_SOURCE") else "unknown",
                response_time=response_time,
                correct=None,
                user_id=st.session_state.user_id,
                answerable=baseline_questions.get(prompt, None),
                common_topics=keywords
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
