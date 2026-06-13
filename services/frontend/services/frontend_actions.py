import streamlit as st
import streamlit.components.v1 as components
import json

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
    st.session_state.selected_page = "chat"


def load_chat_conversation(chat_conversation):
    save_current_chat()

    if isinstance(chat_conversation, ChatConversation):
        conversation = chat_conversation
    else:
        conversation = ChatConversation.model_validate(chat_conversation)

    st.session_state.current_chat_conversation = conversation
    st.session_state.selected_page = "chat"


def create_conversation_title_from_message(message: str, max_length: int = 50) -> str:
    clean_message = message.strip()

    if len(clean_message) <= max_length:
        return clean_message

    return clean_message[:max_length] + "..."


# Copy to Clipboard Button mit KI erstellt
def copy_to_clipboard_button(text: str, key: str):
    escaped_text = json.dumps(text)

    components.html(
        f"""
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                overflow: hidden;
            }}

            body {{
                height: 1.35rem;
                display: flex;
                align-items: center;
            }}
        </style>

        <button id="{key}" title="Kopieren" style="
            border: none;
            background: transparent;
            cursor: pointer;
            padding: 0;
            width: 1.35rem;
            height: 1.35rem;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: #666666;
            line-height: 1;
        ">
            <svg xmlns="http://www.w3.org/2000/svg"
                width="0.9rem"
                height="0.9rem"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
        </button>

        <script>
        const button = document.getElementById("{key}");
        const originalIcon = button.innerHTML;

        button.addEventListener("click", async () => {{
            await navigator.clipboard.writeText({escaped_text});
            button.innerHTML = "✓";
            setTimeout(() => button.innerHTML = originalIcon, 1200);
        }});
        </script>
        """,
        height=22,
    )


# Übergibt die in der Dokumentenview hochgeladenen Dokumente an den Backend-Client zum Upload an das Backend
def upload_documents(uploaded_files):

    backend_client = BackendClient()

    try:
        with st.spinner("Dokumente werden hochgeladen..."):
            result = backend_client.upload_documents(uploaded_files)

    except Exception as error:
        st.error(f"Upload fehlgeschlagen: {error}")
        return None

    return result