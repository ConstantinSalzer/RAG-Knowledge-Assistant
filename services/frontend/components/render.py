import streamlit as st

def render_user_message(message):

    st.markdown(
        f"""
        <div class='chat-user-box'>
            <div class='chat-user-bubble'>
                {message}
            </div>
        </div>""",
        unsafe_allow_html=True
    )

def render_assistant_message(message):

    st.markdown(
        f"""
        <div class='chat-assistant-box'>
            <div class='chat-assistant-bubble'>
                {message}
            </div>
        </div>""",
        unsafe_allow_html=True
    )