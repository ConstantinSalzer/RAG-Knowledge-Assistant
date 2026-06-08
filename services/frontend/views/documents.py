import streamlit as st

PAGE_KEY = "documents"
PAGE_NAME = "Dokumente"
PAGE_PATH = "/views/documents.py"
PAGE_ICON = "📄"

def render_documents():
    st.title("Dokumente")
    st.write("Hier kommen Dokumente.")