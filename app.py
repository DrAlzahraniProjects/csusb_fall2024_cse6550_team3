import streamlit as st
import os
import subprocess

def main():
    """Main Streamlit app logic."""
    st.set_page_config(layout="wide")

    st.title("Hello from Team 3")
    
# Sidebar for chat history
    st.sidebar.title("10 statistics reports")
    chat_history = st.sidebar.empty()


    if 'user_input' not in st.session_state:
        st.session_state['user_input'] = ""

    # Display the entered text in a text area above the input field if text exists
    if st.session_state['user_input']:
        st.text_area("Your input:", value=st.session_state['user_input'], height=100, disabled=True)

    # Create a container for input and button to align them properly
    with st.container():
        # Create two columns for input field and button
        col1, col2 = st.columns([4, 1])

        # Place the input box in the first column
        with col1:
            user_input_new = st.text_input("", placeholder="Enter something here")

        # Place the button in the second column and set its position
        with col2:
            submit_button = st.button("Submit")

    # Handle button click event
    if submit_button and user_input_new:
        # Update session state with the new input
        st.session_state['user_input'] = user_input_new
    
if __name__ == "__main__":
    main()
