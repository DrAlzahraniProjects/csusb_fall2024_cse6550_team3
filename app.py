import streamlit as st

# Set the title of the app

st.set_page_config(page_title="Team3ChatBot", layout="wide")

# chatbot Heading
st.title("Team3 Chatbot")

# Sidebar header for static report metrics
st.sidebar.header("10 Statistics Report")

add_box = st.sidebar.selectbox("select any of them",("Number of questions",
"Number of correct answers",
"Number of incorrect answers",
"User engagement metrics",
"Response time analysis",
"Accuracy rate",
"Common topics or keywords",
"User satisfaction ratings",
"Improvement over time",
"Feedback summary",
"Statistics per day",
"overall"))
# Initialize session state if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Function to handle user input
def handle_user_input_request(user_input):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    bot_response = user_input
    st.session_state.chat_history.append({"role": "bot", "content": bot_response})

# Display chat history
for message in st.session_state.chat_history:
    if message['role'] == 'user':
        st.markdown(f"<div style=' text-align: right;'>{message['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left; '> I am still learning!!</div>", unsafe_allow_html=True)


user_input = st.chat_input("Enter your question here")

if user_input:
    handle_user_input_request(user_input)

