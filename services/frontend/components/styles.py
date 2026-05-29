import streamlit as st

def load_chat_styles():
    
    st.markdown("""
        <style>
                
        /* Chat User Box Settings */
        .chat-user-box {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 10px;
        }
        
        /* Chat User Bubble Styling */
        .chat-user-bubble {
            background-color: #007bff;
            color: white;
            padding: 10px 15px;
            border-radius: 20px;
            max-width: 60%;
        }

        /* Chat Assistant Box Settings */
        .chat-assistant-box {
            display: flex;
            justify-content: flex-start;
            margin-bottom: 10px;
        }

        /* Chat Assistant Bubble Styling */
        .chat-assistant-bubble {
            background-color: #F1F0F0;
            color: black;
            padding: 10px 15px;
            border-radius: 20px;
            max-width: 60%;
        }
                
        </style>
        """,
        unsafe_allow_html=True
    )