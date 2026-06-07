import streamlit as st
from ui.sidebar import render_sidebar
from ui.css_styling import load_sidebar_styles


st.set_page_config(
    page_title="My Streamlit App", 
    page_icon=":sparkles:", 
    layout="wide"
)

load_sidebar_styles()

selected_view = render_sidebar()

selected_view()