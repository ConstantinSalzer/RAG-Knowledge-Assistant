import streamlit as st
from datetime import datetime
from ui.render_functions import (
    render_assistant_actions,
    render_user_message,
    render_assistant_message,
    render_chunk_message,
    render_chat_settings_panel,
    render_web_search_confirmation,
)
from ui.css_styling import load_chat_styles
from shared.schemas import ChatConversation, ChatMessage, MAX_HISTORY_MESSAGES, Settings
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
        st.session_state.chat_settings = Settings()
    

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
            render_assistant_message(message.content, message_index, used_web_search=message.used_web_search)

            # Last message asking whether to search the web: show a confirmation button instead of the usual actions
            is_last_message = message_index == len(st.session_state.current_chat_conversation.messages) - 1
            if message.needs_confirmation and is_last_message:
                if render_web_search_confirmation(message_index):
                    st.session_state.confirm_web_search = True
                    st.rerun()
                continue

            show_sources = render_assistant_actions(
                message_index,
                format_message_time(message.created_at),
                message.content,
                has_chunks=bool(message.chunks),
                tokens_used=message.tokens_used
            )

            if show_sources:
                for chunk_index, chunk in enumerate(message.chunks or []):
                    render_chunk_message(chunk, message_index, chunk_index)

            
# Fügt die User-Nachricht hinzu, holt die KI-Antwort und lädt die Seite neu, um die Konversation zu aktualisieren
def handle_user_input():

    user_input = st.chat_input("Type your message here...")

    rerun_query = st.session_state.pop("rerun_query", None)
    if rerun_query:
        user_input = rerun_query

    # Nutzer hat im vorherigen Lauf auf "Im Web suchen" geklickt
    if st.session_state.pop("confirm_web_search", False):
        handle_web_search_confirmation()
        return

    if user_input:

        if st.session_state.current_chat_conversation.title == "Neuer Chat":
            st.session_state.current_chat_conversation.title = create_conversation_title_from_message(user_input)

        # Letzte Nachrichten der bisherigen Konversation als Kontext für den Pipeline-Service
        history = st.session_state.current_chat_conversation.messages[-MAX_HISTORY_MESSAGES:]

        # User-Nachricht zum Session State hinzufügen
        st.session_state.current_chat_conversation.messages.append(
            ChatMessage(
                role="user",
                content=user_input,
                created_at=datetime.now().isoformat(timespec="seconds")
            )
        )

        # Anfrage an den Pipeline-Service senden
        backend_client = BackendClient()
        response = backend_client.send_chat_message(
            user_input,
            st.session_state.chat_settings,
            history
        )

        append_assistant_response(backend_client, response)
        st.rerun()

# Entfernt die "nichts gefunden"-Nachricht und stellt dieselbe Frage erneut, dieses Mal mit Websuche
def handle_web_search_confirmation():

    messages = st.session_state.current_chat_conversation.messages

    # Entfernt die zuletzt angezeigte "nichts in der Wissensbasis gefunden"-Nachricht
    messages.pop()

    # Die vorangehende User-Nachricht enthält die ursprüngliche Frage
    query = messages[-1].content
    history = messages[:-1][-MAX_HISTORY_MESSAGES:]

    backend_client = BackendClient()
    response = backend_client.send_chat_message(
        query,
        st.session_state.chat_settings,
        history,
        confirm_web_search=True
    )

    append_assistant_response(backend_client, response)
    st.rerun()

# Fügt die Antwort des Pipeline-Service zum Session State hinzu und speichert die Konversation
def append_assistant_response(backend_client, response):

    st.session_state.current_chat_conversation.messages.append(
        ChatMessage(
            role="assistant",
            content=response.answer,
            chunks=response.source_documents,
            created_at=datetime.now().isoformat(timespec="seconds"),
            needs_confirmation=response.needs_confirmation,
            used_web_search=response.used_web_search,
            tokens_used=response.tokens_used
        )
    )

    st.session_state.current_chat_conversation.updated_at = datetime.now().isoformat(timespec="seconds")

    backend_client.save_chat_conversation(
        st.session_state.current_chat_conversation
    )

def format_message_time(created_at):
    if not created_at:
        return ""

    return datetime.fromisoformat(created_at).strftime("%H:%M")