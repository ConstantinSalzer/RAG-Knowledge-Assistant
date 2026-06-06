import streamlit as st
from pathlib import Path

from services.frontend_actions import save_current_chat, start_new_chat
from views.pages import views

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
    col_logo, col_title = st.columns([1.5, 4])

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

    recent_chats = [
        "Erstletzter Chat",
        "Zweitletzter Chat",
        "Drittletzter Chat",
        "Viertletzter Chat",
        "Fünftletzter Chat"
    ]

    for index, chat_title in enumerate(recent_chats):

        if st.button(
            f"💬 {chat_title}",
            key=f"recent_chat_{index}",
            use_container_width=True
        ):
            st.toast(f"{chat_title} geöffnet (Dummy)")