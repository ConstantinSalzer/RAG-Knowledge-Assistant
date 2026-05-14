import streamlit as st
from components.sidebar import render_sidebar


st.set_page_config(
    page_title="My Streamlit App", 
    page_icon=":sparkles:", 
    layout="wide"
)


selected_view = render_sidebar()

selected_view()