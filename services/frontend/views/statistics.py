import streamlit as st


PAGE_KEY = "statistics"
PAGE_NAME = "Statistiken"
PAGE_PATH = "/views/statistics.py"
PAGE_ICON = "📊"

def render_statistics():
    st.title("Statistiken")
    st.write("Hier kommen Statistiken.")
