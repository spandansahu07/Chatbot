import streamlit as st
import requests
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="Smarty AI", page_icon="🤖", layout="centered", initial_sidebar_state="auto")

# Custom CSS for dark & white theme and chat bubbles
st.markdown("""
    <style>
    .bg-video {
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100vw;
        min-height: 100vh;
        z-index: -1;
        object-fit: cover;
        opacity: 0.25;
    }
    body, .stApp {
        background: linear-gradient(135deg, #181818 60%, #fff 100%);
        color: #222;
    }
    .user-bubble {
        background: #343541;
        color: #fff;
        border-radius: 12px;
        padding: 10px 16px;
        margin-bottom: 8px;
        width: fit-content;
        max-width: 80%;
        align-self: flex-end;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    .ai-bubble {
        background: #fff;
        color: #222;
        border-radius: 12px;
        padding: 10px 16px;
        margin-bottom: 8px;
        width: fit-content;
        max-width: 80%;
        align-self: flex-start;
        box-shadow: 0 2px 8px rgba(0,0,0,0.10);
        border: 1px solid #444654;
    }
    .tab-label {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 12px;
        color: #343541;
    }
    </style>
    <video autoplay loop muted playsinline class="bg-video">
        <source src="public/chatbotbg.mp4" type="video/mp4">
    </video>
""", unsafe_allow_html=True)

st.title("🤖 Smarty AI")

if "user_name" not in st.session_state:
    st.session_state["user_name"] = ""
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Page logic
if not st.session_state["user_name"]:
    st.markdown('<div class="tab-label">Welcome! Please enter your name to start chatting:</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([5,1])
    with col1:
        name = st.text_input("Your Name", value="", label_visibility="visible")
    with col2:
        enter_clicked = st.button("Enter", use_container_width=True)
        st.markdown("<style>.stButton button {margin-top: 28px !important;}</style>", unsafe_allow_html=True)
    if enter_clicked and name:
        st.session_state["user_name"] = name
        st.success(f"Hello, {name}! Redirecting to chat...")
        st.rerun()
else:
    url = "https://api.groq.com/openai/v1/chat/completions"
    model = "llama3-8b-8192"  # Free model
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-bubble">{st.session_state["user_name"]}: {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-bubble">AI: {msg["content"]}</div>', unsafe_allow_html=True)

    user_input = st.chat_input("Type your message...")
    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": model,
            "messages": st.session_state["messages"],
            "temperature": 0.7
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            ai_message = response.json()["choices"][0]["message"]["content"]
            st.session_state["messages"].append({"role": "assistant", "content": ai_message})
            st.rerun()
        except Exception as e:
            st.error(f"❌ API call failed: {e}")
