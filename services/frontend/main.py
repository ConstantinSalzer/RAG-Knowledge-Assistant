import streamlit as st
from components.sidebar import render_sidebar
from components.styles import load_sidebar_styles


st.set_page_config(
    page_title="My Streamlit App", 
    page_icon=":sparkles:", 
    layout="wide"
)

load_sidebar_styles()

selected_view = render_sidebar()

selected_view()