import streamlit as st

from services.backend_client import BackendClient

PAGE_KEY = "history"
PAGE_NAME = "Chat History"
PAGE_PATH = "/views/chat_history.py"
PAGE_ICON = "⏳"

def render_history():
    st.title("Chat History")

    backend_client = BackendClient()
    chat_conversations = backend_client.get_chat_conversations()

    for conversation in chat_conversations:
        st.write(conversation["title"])