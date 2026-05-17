import requests
import streamlit as st
from components.render import render_user_message, render_assistant_message
from components.styles import load_chat_styles
from models.chat_settings import ChatSettings
from services.backend_client import BackendClient

PAGE_NAME = "Chat"
PAGE_PATH = "/views/chat.py"
PGAE_ICON = "💬"

# Hauptfunktion, die die Seite rendert, indem sie den Titel setzt, den Session State 
# initialisiert, die aktuelle Chat-Historie rendert und die Benutzereingabe handhabt
def render_chat():
    st.title("Chat")
    
    load_chat_styles()
    init_session_state()
    render_conversation()
    handle_user_input()
    render_sidebar_settings()


# Initialisiert den Session State für die aktuelle Konversation (nicht persistente Speicherung im frontend)
def init_session_state():

    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "chat_settings" not in st.session_state:
        st.session_state.chat_settings = ChatSettings()


# Rendert die aktuelle Konversation, indem sie durch die gespeicherten Nachrichten im Session State iteriert und sie entsprechend darstellt
def render_conversation():

    for message in st.session_state.messages:
            
            if message["role"] == "user":
                render_user_message(message["content"])

            elif message["role"] == "assistant":
                render_assistant_message(message["content"])

                if "chunks" in message:

                    for chunk in message["chunks"]:

                        render_assistant_message(
                            f"""
                📄 {chunk['file_name']}

                👤 {chunk['author']}

                ⭐ Confidence Score: {chunk['confidence_score']}

                {chunk['content']}
                """
                            )


# Handhabt die Benutzereingabe, indem sie die Nachricht des Benutzers zum Session State hinzufügt, eine KI-Antwort generiert 
# (hier als Platzhalter) und diese ebenfalls zum Session State hinzufügt, bevor die Seite neu geladen wird, um die aktualisierte Konversation anzuzeigen
def handle_user_input():

    user_input = st.chat_input("Type your message here...")

    if user_input:

        #User-Nachricht zum Session State hinzufügen
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        # Anfrage an FastAPI senden
        backend_client = BackendClient()
        response = backend_client.send_chat_message(
            user_input,
            st.session_state.chat_settings
        )

        ai_response = response.get("response")
        chunks = response.get("chunks", [])

        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_response,
            "chunks": chunks
        })

        st.rerun()


# Rendert Einstellungen für die aktuelle Konversation. Diese werden in der Sidebar angezeigt und können per Button an das Backend gesendet werden
def render_sidebar_settings():

    st.sidebar.divider()

    st.sidebar.subheader("Chat Settings")

    chat_settings = st.session_state.chat_settings

    top_k = st.sidebar.slider(
        "Top-K Chunks",
        chat_settings.MIN_TOP_K,
        chat_settings.MAX_TOP_K,
        value=chat_settings.top_k
    )

    with st.sidebar.expander("Advanced Settings"):

        selected_llm = st.selectbox(
            "LLM",
            chat_settings.LLM_OPTIONS,
            index=chat_settings.LLM_OPTIONS.index(chat_settings.llm)
        )

        prompting_strategy = st.selectbox(
            "Prompting Strategy",
            chat_settings.PROMPT_STRATEGIES,
            index=chat_settings.PROMPT_STRATEGIES.index(chat_settings.prompting_strategy)
        )

    apply_button = st.sidebar.button(
        "Apply Settings",
        use_container_width=True,
        type="primary"
    )

    if apply_button:

        chat_settings.top_k = top_k
        chat_settings.llm = selected_llm
        chat_settings.prompting_strategy = prompting_strategy

        st.sidebar.success("Settings applied!")