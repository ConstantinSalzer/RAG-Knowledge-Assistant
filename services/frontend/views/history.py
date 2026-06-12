import streamlit as st
from datetime import datetime, timedelta

from services.backend_client import BackendClient
from services.frontend_actions import load_chat_conversation
from ui.css_styling import load_history_styles
from ui.render_functions import render_chat_history_preview

PAGE_KEY = "history"
PAGE_NAME = "Chat History"
PAGE_PATH = "/views/history.py"
PAGE_ICON = "⏳"

# Hauptfunktion, die die Seite rendert
def render_history():

    init_session_state()
    load_history_styles()

    backend_client = BackendClient()
    chat_conversations = backend_client.get_chat_conversations()

    with st.container(key="history_page_container"):
        render_history_header()

    with st.container(key="history_conversation_list_container"):
        grouped_conversations = group_chat_conversations_by_updated_at(chat_conversations)

        for group_title, conversations in grouped_conversations.items():
            render_chat_history_group(group_title, conversations)


# Initialisiert den Session State für (notwendig für den Button der jeweiligen Chat-Ansicht)
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

    st.markdown(
        f"""
        <div class='history-group-header'>
            <div class='history-group-title'>{group_title}</div>
            <div class='history-group-line'></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Rendert jeden einzelnen Chatverlauf in der Gruppe nach bestimmten Schema
    for conversation in conversations:
        render_chat_history_item(conversation)


# Rendert jeden einzelnen Chatverlauf als Item in der Historie: Zeigt Titel, Aktualisierungszeitpunkt 
# und Buttons zum Laden der Konversation bzw. Anzeigen einer Vorschau an
def render_chat_history_item(conversation):
    conversation_id = conversation["id"]
    updated_at = format_datetime(conversation["updated_at"])
    title = conversation["title"]

    is_open = st.session_state.open_history_conversation_id == conversation_id

    with st.container(key=f"history_item_container_{conversation_id}"):
        item_col, load_col = st.columns([10, 1.6])

        button_label = f"{updated_at}  |  {title}"

        with item_col:
            with st.container(key=f"history_item_toggle_container_{conversation_id}"):
                if st.button(
                    button_label,
                    key=f"toggle_history_item_{conversation_id}",
                    use_container_width=True
                ):
                    toggle_history_conversation(conversation_id)

        with load_col:
            with st.container(key=f"history_item_load_container_{conversation_id}"):
                if st.button(
                    "Laden",
                    key=f"load_chat_{conversation_id}",
                    use_container_width=True
                ):
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


def format_datetime(value: str) -> str:
    if not value:
        return ""

    return datetime.fromisoformat(value).strftime("%d.%m.%Y %H:%M")