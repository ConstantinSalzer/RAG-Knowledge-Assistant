import streamlit as st

from schemas import ChatConversation
from services.backend_client import BackendClient


def save_current_chat():
    if "current_chat_conversation" not in st.session_state:
        return

    if not st.session_state.current_chat_conversation.messages:
        return

    backend_client = BackendClient()
    backend_client.save_chat_conversation(
        st.session_state.current_chat_conversation
    )


def start_new_chat():
    st.session_state.current_chat_conversation = ChatConversation.create_new()


def create_conversation_title_from_message(message: str, max_length: int = 50) -> str:
    clean_message = message.strip()

    if len(clean_message) <= max_length:
        return clean_message

    return clean_message[:max_length] + "..."