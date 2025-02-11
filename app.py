import streamlit as st
import requests

st.title("Resume-aware Chatbot 🤖📄")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
query = st.text_input("Ask about my experience:", key="user_input")

if st.button("Send") and query:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": query})

    # Send request to FastAPI backend
    response = requests.post("http://127.0.0.1:8000/chat", params={"query": query})
    bot_response = response.json().get("response")

    # Store bot response
    st.session_state.messages.append({"role": "bot", "content": bot_response})

    # Refresh UI
    st.rerun()

