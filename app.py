import streamlit as st
import requests
from datetime import datetime

# Define API URL
API_URL = "https://rajattech02-resume-aware-bot.hf.space/chat"

# Set Page Config
st.set_page_config(page_title="Resume Chatbot", page_icon="🤖", layout="centered")

# Apply Custom Styling
st.markdown("""
    <style>
        /* Light & Dark Mode Adaptive Background */
        [data-testid="stAppViewContainer"] {
            background-color: var(--background);
        }

        /* Define color variables */
        :root {
            --background: #F7F7F7;
            --user-chat-bg: #DCF8C6;
            --bot-chat-bg: #E8E8E8;
            --text-color: #222222;
            --link-color: #007AFF;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --background: #1E1E1E;
                --user-chat-bg: #2A7E55;
                --bot-chat-bg: #333333;
                --text-color: #FFFFFF;
                --link-color: #4DA3FF;
            }
        }

        /* Title Styling */
        h1, h2 {
            color: var(--text-color);
            text-align: center;
        }

        /* Chat messages */
        .chat-bubble {
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 10px;
            width: fit-content;
            max-width: 80%;
            color: var(--text-color);
        }
        .user {
            background-color: var(--user-chat-bg);
            text-align: right;
            margin-left: auto;
        }
        .bot {
            background-color: var(--bot-chat-bg);
            text-align: left;
            margin-right: auto;
        }

        /* Clickable Links */
        a {
            color: var(--link-color);
            text-decoration: none;
            font-weight: bold;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# Add AI/ML Taglines at the Top
st.markdown("### 📝 Built using cutting-edge AI and ML technologies!", unsafe_allow_html=True)
st.markdown("### 📝 Meet Resume Aware Bot! Your AI assistant that instantly responds to HR queries about your resume, even when you're unavailable.", unsafe_allow_html=True)

# Title
st.title("💬 Resume-aware Chatbot by Rajat 🤖📄")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

import re

def convert_links_to_markdown(text):
    """Convert any URLs in text to clickable Markdown links."""
    url_pattern = r"(https?://[^\s]+)"
    return re.sub(url_pattern, r"[\1](\1)", text)  # Converts plain URLs into Markdown links

# Display previous messages with proper alignment
for message in st.session_state.messages:
    role = "👤 User" if message["role"] == "user" else "🤖 Bot"
    time_str = message["timestamp"]
    
    if message["role"] == "user":
        col1, col2 = st.columns([1, 5])  # Right-align user messages
        with col2:
            st.markdown(f"<div style='text-align: right;'><b>{role} ({time_str}):</b><br>{message['content']}</div>", unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([5, 1])  # Left-align bot messages
        with col1:
            st.markdown(f"<b>{role} ({time_str}):</b><br>{message['content']}", unsafe_allow_html=True)

# User input (Automatically submits on Enter)
query = st.chat_input("Ask about Rajat's experience:")

if query:
    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": query,
        "timestamp": datetime.now().strftime("%H:%M")
    })

    # Send request to FastAPI backend
    try:
        with st.spinner("Typing... 🤔"):
            response = requests.post(API_URL, json={"query": query}, timeout=50)

        if response.status_code == 200:
            bot_response = response.json().get("response", "⚠️ No response received.")
        else:
            bot_response = f"⚠️ Error {response.status_code}: {response.text}"

    except requests.exceptions.RequestException as e:
        bot_response = f"⚠️ Connection error: {str(e)}"

    # Store bot response
    st.session_state.messages.append({
        "role": "bot",
        "content": bot_response,
        "timestamp": datetime.now().strftime("%H:%M")
    })

    # Refresh UI
    st.rerun()
