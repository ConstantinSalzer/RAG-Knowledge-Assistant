import streamlit as st
from views import history
from views import chat

views = {
    chat.PAGE_NAME: chat.render_chat,
    history.PAGE_NAME: history.render_history
}

def render_sidebar():
    with st.sidebar:
        st.title("Sidebar")
        st.write("This is the sidebar content.")

        st.divider()

        st.subheader("Navigation")

        # Checkbox: zeigt Namen der Seiten an und gibt Funktion für dessen Ausführung zurück
        selected_page = st.radio(
            "", 
            options = list(views.keys()),
            label_visibility="collapsed"
        )

    return views[selected_page]