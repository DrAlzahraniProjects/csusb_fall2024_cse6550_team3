import os
import time
import subprocess
import streamlit as st
from roman import toRoman
from streamlit_pdf_viewer import pdf_viewer
from inference import chat_completion
from interface import (
    init_db, 
    init_user_session, 
    update_user_session, 
    insert_conversation, 
    get_statistics,
    toggle_correctness
)

init_db()  # Initialize the database


def serve_pdf():
    TEXTBOOK_PATH = os.path.join(os.path.dirname(__file__), "data", "textbook")
    file = st.query_params.get("file")
    page = max(int(st.query_params.get("page", "1")), 1)
    adjusted_page = page - 33
    if adjusted_page < 1:
        adjusted_page = toRoman(page)

    if file:
        pdf_path = os.path.join(TEXTBOOK_PATH, file)
        if os.path.exists(pdf_path):
            with st.spinner(f"Loading page {adjusted_page} of the PDF..."):
                pdf_viewer(
                    pdf_path,
                    width=700,
                    height=1000,
                    pages_to_render=[page],
                    scroll_to_page=page
                )
        else:
            st.error(f"PDF file not found at {pdf_path}")
    else:
        st.error("No PDF file specified in query parameters")


def update_and_display_statistics():
    stats = get_statistics()
    st.session_state.statistics = stats

    statistics = [
        f"Number of questions: {stats['num_questions']}",
        f"Number of correct answers: {stats['num_correct']}",
        f"Number of incorrect answers: {stats['num_incorrect']}",
        f"User engagement metrics: {stats['user_engagement']:.2f} seconds",
        f"Response time analysis: {stats['avg_response_time']:.2f} seconds",
        f"Accuracy rate: {stats['accuracy_rate']:.2f}%",
        f"Satisfaction rate: {stats['satisfaction_rate']:.2f}%"
    ]

    st.sidebar.markdown("<h1 class='title-stat'>Statistics Reports</h1>", unsafe_allow_html=True)
    for stat in statistics:
        st.sidebar.markdown(f"""
            <div class='btn-stat-container'>
                <a href="#" class="btn-stat">{stat}</a>
            </div>
        """, unsafe_allow_html=True)


def main():
    header = st.container()
    header.title("Textbook Chatbot")
    header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

    if "view" in st.query_params and st.query_params["view"] == "pdf":
        serve_pdf()

    else:
        def load_css(file_name):
            with open(file_name) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        load_css("Styles/style.css")

        if "user_id" not in st.session_state:
            st.session_state.user_id = init_user_session()
            print(f"Creating user#{st.session_state.user_id}")
        
        st.sidebar.empty()
        update_and_display_statistics()

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            if message["role"] == "assistant":
                st.markdown(f"<div class='assistant-message'>{message['content']}</div>", unsafe_allow_html=True)
                conversation_id = message.get("conversation_id", None)
                if conversation_id:
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("👍", key=f"correct_{conversation_id}"):
                            toggle_correctness(conversation_id, True)
                    with col2:
                        if st.button("👎", key=f"incorrect_{conversation_id}"):
                            toggle_correctness(conversation_id, False)
            else:
                st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)

        if prompt := st.chat_input("Ask your question?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.markdown(f"<div class='user-message'>{prompt}</div>", unsafe_allow_html=True)

            with st.spinner("Generating response..."):
                start_time = time.time()
                response, model_name = chat_completion(prompt)
                end_time = time.time()
                response_time = int((end_time - start_time))

            st.session_state.messages.append({"role": "assistant", "content": response})

            conversation_id = insert_conversation(
                question=prompt,
                response=response,
                citations="",
                model_name=model_name,
                response_time=response_time,
                correct=True,
                user_id=st.session_state.user_id,
                common_topics=""
            )

            st.markdown(f"""
                <div class='assistant-message'>
                    {response}
                    <div class='feedback-buttons'>
                        <span class='feedback-icon'>👍</span>
                        <span class='feedback-icon'>👎</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            update_user_session(st.session_state.user_id)


if __name__ == "__main__":
    if os.environ.get("STREAMLIT_RUNNING") == "1":
        main()
    else:
        os.environ["STREAMLIT_RUNNING"] = "1"
        subprocess.run(["streamlit", "run", __file__, "--server.port=5003", "--server.address=0.0.0.0", "--server.baseUrlPath=/team3"])
