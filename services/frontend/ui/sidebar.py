import streamlit as st
from pathlib import Path

from services.backend_client import BackendClient
from services.frontend_actions import save_current_chat, start_new_chat, load_chat_conversation

from views import chat
from views import history
from views import documents
from views import statistics

views = {
    chat.PAGE_KEY: {
        "label": chat.PAGE_NAME,
        "icon": chat.PAGE_ICON,
        "render": chat.render_chat,
    },
    history.PAGE_KEY: {
        "label": history.PAGE_NAME,
        "icon": history.PAGE_ICON,
        "render": history.render_history,
    },
    documents.PAGE_KEY: {
        "label": documents.PAGE_NAME,
        "icon": documents.PAGE_ICON,
        "render": documents.render_documents,
    },
    statistics.PAGE_KEY: {
        "label": statistics.PAGE_NAME,
        "icon": statistics.PAGE_ICON,
        "render": statistics.render_statistics,
    },
}

def render_sidebar():
    
    with st.sidebar:

        render_sidebar_header()

        st.divider()

        selected_page = render_sidebar_navigation()

        st.divider()

        render_sidebar_actions()

        st.divider()

        render_sidebar_chat_history()

    return views[selected_page]["render"]


def render_sidebar_header():

    # Pfad zum Logobild (relativ gesetzt, also zweimal nach oben und dann in assets-Ordner)
    logo_path = Path(__file__).parent.parent / "assets" / "rag-logo-variant-21.svg"

    LOGO_SIZE = 48

    #Legt zwei Spalten an (links Logo, rechts Titel)
    col_logo, col_title = st.columns([1.5, 5])

    # Zeigt das Logo da, sofern die Datei existiert, 
    # Der Fallback verhindert Fehler bei fehlendem Bild (-> Anzeige leerer String)
    with col_logo:
        if logo_path.exists():
            st.image(str(logo_path), width=LOGO_SIZE)
        else:
            st.write("")

    # Zeigt den Titel vertikal zentriert zum Logo an.
    with col_title:
        st.markdown(
            f"""
            <div style="
                height: {LOGO_SIZE}px;
                line-height: {LOGO_SIZE}px;
                font-size: 1.25rem;
                font-weight: 600;
            ">
                RAG Assistant
            </div>
            """,
            unsafe_allow_html=True
        )


def render_sidebar_navigation():

    # Initialisiert den Session State für die ausgewählte Seite, falls noch nicht vorhanden
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "chat"

    # Iteriert durch die definierten Views (Seiten) und erstellt für jede einen Button in der Sidebar
    for page_key, page in views.items():

        is_active = st.session_state.selected_page == page_key

    # Der Klammerteile definiert die einzelnen Buttons. Der Teil danach speichert die ausgewählte Seite im Session State
        if st.button(
            f"{page['icon']} {page['label']}",
            key = f"nav_{page_key}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.selected_page = page_key
            st.rerun()
    
    return st.session_state.selected_page


def render_sidebar_actions():

    # Button: Neuer Chat
    if st.button(
        "➕ Neuer Chat",
        key="new_chat",
        use_container_width=True
    ):
        save_current_chat()
        start_new_chat()
        st.toast("Aktueller Chat gespeichert")
        st.rerun()

    # Button: Chat durchsuchen
    if st.button(
        "🔍 Chat durchsuchen",
        key="search_chat",
        use_container_width=True
    ):
        st.toast("Chat-Suche geöffnet (Dummy)")

    # Button: Dokument hochladen
    if st.button(
        "📄 Dokumente hochladen",
        key="upload_docs",
        use_container_width=True
    ):
        st.toast("Dokument-Upload geöffnet (Dummy)")


def render_sidebar_chat_history():
    backend_client = BackendClient()
    recent_chats = backend_client.get_chat_conversations()[:10]

    for chat_conversation in recent_chats:
        conversation_id = chat_conversation["id"]
        chat_title = format_sidebar_chat_title(chat_conversation["title"])

        if st.button(
            f"💬 {chat_title}",
            key=f"recent_chat_{conversation_id}",
            use_container_width=True
        ):
            load_chat_conversation(chat_conversation)
            st.rerun()


def format_sidebar_chat_title(title, max_length=18):
    if len(title) <= max_length:
        return title

    return title[:max_length] + "..."