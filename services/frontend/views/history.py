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
        search_query = render_history_header()

    # Suche läuft client-seitig auf den bereits geladenen Konversationen –
    # kein extra Request ans Backend nötig, da die Liste ohnehin komplett geladen wird.
    if search_query:
        query_lower = search_query.lower()
        chat_conversations = [
            c for c in chat_conversations
            if query_lower in c["title"].lower()
        ]

    with st.container(key="history_conversation_list_container"):
        grouped_conversations = group_chat_conversations_by_updated_at(chat_conversations)

        for group_title, conversations in grouped_conversations.items():
            render_chat_history_group(group_title, conversations)


# Initialisiert den Session State (notwendig für den Button der jeweiligen Chat-Ansicht)
def init_session_state():
    if "open_history_conversation_id" not in st.session_state:
        st.session_state.open_history_conversation_id = None


# Rendert den Chat-Header mit dem Titel und einem Suchfeld
def render_history_header() -> str:

    header = st.container(key="history_header_container")

    with header:
        title_col, search_col = st.columns([5, 5])

        with title_col:
            st.subheader("Historische Chatverläufe")

        with search_col:
            search_query = st.text_input(
                "Suche",
                placeholder="🔍 Chat durchsuchen...",
                label_visibility="collapsed",
                key="history_search",
            )

    return search_query


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