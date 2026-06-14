from datetime import datetime, timedelta

import streamlit as st

from services.backend_client import BackendClient
from services.frontend_actions import load_chat_conversation
from ui.css_styling import load_history_styles
from ui.render_functions import render_section_header, render_list_item, render_chat_history_preview

PAGE_KEY = "history"
PAGE_NAME = "Chat History"
PAGE_PATH = "/views/history.py"
PAGE_ICON = "⏳"

# Hauptfunktion, die die Seite rendert
def render_history():

    init_session_state()

    load_history_styles()

    backend_client = BackendClient()
    
    try:
        chat_conversations = backend_client.get_chat_conversations()

    except Exception as error:
        st.error(f"Chatverläufe konnten nicht geladen werden: {error}")
        return

    with st.container(key="history_page_container"):
        render_history_header()

    with st.container(key="history_conversation_list_container"):
        grouped_conversations = group_chat_conversations_by_updated_at(chat_conversations)

        for group_title, conversations in grouped_conversations.items():
            render_chat_history_group(group_title, conversations)


# Initialisiert den Session State (notwendig für den Button der jeweiligen Chat-Ansicht)
def init_session_state():
    if "open_history_conversation_id" not in st.session_state:
        st.session_state.open_history_conversation_id = None


# Rendert den Chat-Header mit dem Titel und einem Button zur Suche im Chatverlauf
def render_history_header():

    header = st.container(key="history_header_container")

    with header:
        title_col, button_col = st.columns([10, 3.9])

        with title_col:
            st.subheader("Historische Chatverläufe")

        with button_col:
            if st.button("🔍 Chat durchsuchen", key="search_history"):
                st.toast("Chat-Suche geöffnet (Dummy)")


# Rendert eine Gruppe von Chatverläufen: Jede Gruppe hat einen Titel und eine Liste von Chatverläufen
def render_chat_history_group(group_title, conversations):
    if not conversations:
        return

    render_section_header(group_title)

    # Rendert jeden einzelnen Chatverlauf in der Gruppe nach bestimmten Schema
    for conversation in conversations:
        render_chat_history_item(conversation)


# Rendert ein Chatverlauf-Item: Titel, Aktualisierungszeitpunkt, Buttons zum Laden/Anzeigen einer Vorschau
def render_chat_history_item(conversation):

    conversation_id = conversation["id"]
    updated_at = format_history_datetime(conversation["updated_at"])
    title = conversation["title"]

    is_open = (st.session_state.open_history_conversation_id == conversation_id)

    item_label = f"{updated_at}  |  {title}"

    toggle_clicked, load_clicked = render_list_item(
        item_label=item_label,
        item_key=f"history_{conversation_id}",
        action_label="Laden"
    )

    if toggle_clicked:
        toggle_history_conversation(conversation_id)

    if load_clicked:
        load_chat_conversation(conversation)
        st.rerun()

    if is_open:
        render_chat_history_preview(conversation)


# -----HILFSFUNKTIONEN-----

def group_chat_conversations_by_updated_at(chat_conversations):
    now = datetime.now()

    groups = {
        "Letzte 7 Tage": [],
        "Letzte 30 Tage": [],
        "Letztes Jahr": [],
        "Älter als ein Jahr": [],
    }

    for conversation in chat_conversations:
        updated_at = datetime.fromisoformat(conversation["updated_at"])
        age = now - updated_at


        if age <= timedelta(days=7):
            groups["Letzte 7 Tage"].append(conversation)
        elif age <= timedelta(days=30):
            groups["Letzte 30 Tage"].append(conversation)
        elif age <= timedelta(days=365):
            groups["Letztes Jahr"].append(conversation)
        else:
            groups["Älter als ein Jahr"].append(conversation)

    return groups

def toggle_history_conversation(conversation_id):
    if st.session_state.open_history_conversation_id == conversation_id:
        st.session_state.open_history_conversation_id = None
    else:
        st.session_state.open_history_conversation_id = conversation_id

    st.rerun()


def format_history_datetime(value: str) -> str:
    if not value:
        return ""

    return datetime.fromisoformat(value).strftime("%d.%m.%Y %H:%M")