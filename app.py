import streamlit as st
import requests

API_URL = "https://rajattech02-resume-aware-bot.hf.space/chat"

st.title("Resume-aware Chatbot 🤖📄")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

query = st.text_input("Ask about my experience:", key="user_input")

if st.button("Send") and query:
    st.session_state.messages.append({"role": "user", "content": query})

    try:
        response = requests.post(
            API_URL,
            json={"query": query},
            timeout=10  # Set a timeout to avoid hanging requests
        )

        if response.status_code == 200:
            bot_response = response.json().get("response", "I'm not sure how to answer that.")
        else:
            bot_response = f"Error {response.status_code}: {response.text}"

    except requests.exceptions.RequestException as e:
        bot_response = f"Request Error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.rerun()
