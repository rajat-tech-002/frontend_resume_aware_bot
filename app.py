import streamlit as st
import requests

# FastAPI Backend URL on Hugging Face Spaces
API_URL = "https://huggingface.co/spaces/rajattech02/resume_aware_bot"  # Replace with actual URL

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

    try:
        # Send request to FastAPI backend
        response = requests.post(API_URL, json={"query": query})

        if response.status_code == 200:
            bot_response = response.json().get("response", "I'm not sure how to answer that.")
        else:
            bot_response = "Error: Could not get a response from the backend."

    except requests.exceptions.RequestException:
        bot_response = "Error: Unable to reach the backend. Check your connection."

    # Store bot response
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    # Refresh UI
    st.rerun()
