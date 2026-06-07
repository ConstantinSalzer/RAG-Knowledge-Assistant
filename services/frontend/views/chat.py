import streamlit as st
from datetime import datetime
from ui.render_functions import (
    render_assistant_actions,
    render_user_message,
    render_assistant_message,
    render_chunk_message,
    render_chat_settings_panel,
)
from ui.css_styling import load_chat_styles
from schemas import ChatConversation, ChatMessage, ChatSettings
from services.backend_client import BackendClient
from services.frontend_actions import create_conversation_title_from_message


PAGE_KEY = "chat"
PAGE_NAME = "Aktueller Chat"
PAGE_PATH = "/views/chat.py"
PAGE_ICON = "💬"

# Hauptfunktion, die die Seite rendert
def render_chat():

    load_chat_styles()
    init_session_state()

    # Legt einen Container fest, der Chat-Header, Chat-Verlauf und Chat-Input enthält
    with st.container(key="chat_page_container"):
        render_chat_header()

        with st.container(key="chat_conversation_container"):
            render_conversation()
    
        with st.container(key="chat_input_container"):
            handle_user_input()
        

# Initialisiert den Session State für die aktuelle Konversation (nicht persistente Speicherung im frontend)
def init_session_state():

    if "current_chat_conversation" not in st.session_state:
        st.session_state.current_chat_conversation = ChatConversation.create_new()
    
    if "chat_settings" not in st.session_state:
        st.session_state.chat_settings = ChatSettings()
    

# Rendert den Chat-Header mit dem Titel und einem Button, der die Chat-Einstellungen öffnet
def render_chat_header():

    header = st.container(key="chat_header_container")

    with header:
        title_col, button_col = st.columns([8, 1])

        with title_col:
            st.subheader("Aktueller Chat")

    with button_col:
        with st.popover("⚙️"):
            render_chat_settings_panel()




# Rendert die aktuelle Konversation, indem sie durch die gespeicherten Nachrichten im Session State iteriert und sie entsprechend darstellt
def render_conversation():

    for message_index, message in enumerate(st.session_state.current_chat_conversation.messages):
            
        if message.role == "user":
            render_user_message(
                message.content,
                message_index,
                format_message_time(message.created_at)
            )

        elif message.role == "assistant":
            render_assistant_message(message.content)

            show_sources = render_assistant_actions(
                message_index,
                format_message_time(message.created_at),
                message.content,
                has_chunks=bool(message.chunks)
            )

            if show_sources:
                for chunk_index, chunk in enumerate(message.chunks or []):
                    render_chunk_message(chunk, message_index, chunk_index)

            
# Handhabt die Benutzereingabe, indem sie die Nachricht des Benutzers zum Session State hinzufügt, eine KI-Antwort generiert 
# (hier als Platzhalter) und diese ebenfalls zum Session State hinzufügt, bevor die Seite neu geladen wird, um die aktualisierte Konversation anzuzeigen
def handle_user_input():

    user_input = st.chat_input("Type your message here...")

    if user_input:

        if st.session_state.current_chat_conversation.title == "Neuer Chat":
            st.session_state.current_chat_conversation.title = create_conversation_title_from_message(user_input)

        #User-Nachricht zum Session State hinzufügen
        st.session_state.current_chat_conversation.messages.append(
            ChatMessage(
                role="user",
                content=user_input,
                created_at=datetime.now().isoformat(timespec="seconds")
            )
        )

        # Anfrage an FastAPI senden
        backend_client = BackendClient()
        response = backend_client.send_chat_message(
            user_input,
            st.session_state.chat_settings
        )

        ai_response = response.get("response")
        chunks = response.get("chunks", [])

        st.session_state.current_chat_conversation.messages.append(
            ChatMessage(
                role="assistant",
                content=ai_response,
                chunks=chunks,
                created_at=datetime.now().isoformat(timespec="seconds")
            )
        )

        st.session_state.current_chat_conversation.updated_at = datetime.now().isoformat(timespec="seconds")

        backend_client.save_chat_conversation(
            st.session_state.current_chat_conversation
        )

        st.rerun()

def format_message_time(created_at):
    if not created_at:
        return ""

    return datetime.fromisoformat(created_at).strftime("%H:%M")