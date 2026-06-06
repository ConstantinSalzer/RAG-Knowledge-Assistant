import streamlit as st

def load_chat_styles():
    
    st.markdown("""
        <style>
        
        /* -----STYLING AUFBAU CHAT SEITE----- */
                                
        /* block-Klasse ist die übergeordnete Klasse für alle Blöcke auf einer Seite. Es handelt sich
        um eine von Streamlit vordefinierte Klasse. Die hier getroffenen Änderung sorghen dafür,
        dass der Inhalt direkt ganz oben beginnt und die maximale Breite begrenzt wird. */
                
        .block-container {
            max-width: 1000px;
            margin-left: auto;
            margin-right: auto;    
            
            padding-top: 3rem;
            padding-bottom: 0rem;
        }

        /* Übegeordneter Container für die drei Bestandteile: chat_header, chat_conversation, chat_input */           
        .st-key-chat_page_container {
            height: calc(100vh - 7rem);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }  

        .st-key-chat_header_container {
            border-bottom: 1px solid #d1d5db;
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
        }
                
        .st-key-chat_conversation_container {
            height: calc(100vh - 19rem);
            max-height: calc(100vh - 19rem);
            overflow-y: auto;
            border: none;
            padding-right: 0.5rem;
        }
                
        .st-key-chat_input_container {
        }
                

        /* -----STYLING TEIL USER MESSAGES----- */        
                                                      
        div[class*="st-key-user_message_container_"] {
            max-width: 70%;
            margin-left: auto;
            margin-bottom: 0.75rem;
        }

        div[class*="st-key-user_message_container_"] .chat-user-bubble {
            background-color: #f4f4f4;
            color: #111111;
            padding: 10px 15px;
            border-radius: 20px;
            width: fit-content;
            max-width: 100%;
            margin-left: auto;
        }

        /* Button selbst */
        div[class*="st-key-user_message_container_"] button {
            min-height: 0;
            height: 1.35rem;
            padding: 0.05rem 0.35rem;
            font-size: 0.7rem;
            border: none;
            background-color: transparent;
            color: #666666;
        }

                
        /* -----STYLING TEIL ASSISTANT MESSAGES----- */                 

        /* Chat Assistant Box Settings */
        .chat-assistant-box {
            display: flex;
            justify-content: flex-start;
            margin-bottom: 1.25rem;
        }

        /* Chat Assistant Bubble Styling */
        .chat-assistant-bubble {
            background-color: transparent;
            color: #111111;
            padding: 0;
            border-radius: 0;
            max-width: 80%;
            line-height: 1.6;
        } 

        /* Chat Chunk Box Settings als Container für Expander*/
        div[class*="st-key-chat_chunk_container_"] {
            background-color: #f7f8fa;
            border: 1px solid #e2e4e8;
            border-radius: 12px;
                
            max-width: 75%;
            margin-right: auto;
            margin-bottom: 0.5rem;
        }   

        div[class*="st-key-assistant_actions_container_"] {
            max-width: 75%;
            margin-right: auto;
            margin-bottom: 1rem;
        }

        div[class*="st-key-assistant_actions_container_"] button {
            min-height: 0;
            height: 1.35rem;
            padding: 0.05rem 0.35rem;
            font-size: 0.7rem;
            border: none;
            background-color: transparent;
            color: #666666;
        }  
                                 
        </style>
        """,
        unsafe_allow_html=True
    )


def load_sidebar_styles():

    # Mit markdown wird ein Style-Tag in die Seite eingebettet, der die Breite der Sidebar anpasst.
    # Die Sidebar selbst besteht aus mehreren "HTML-Elementen", die alle angepasst werden müssen (daher die zwei Selektoren).
    st.markdown(
        """
        <style>

        /* Setzt die Breite der Sidebar (außen) auf 260px */
        section[data-testid="stSidebar"] {
            width: 260px !important;
        }

        /* Setzt die Breite der Sidebar (innen) auf 260px */
        section[data-testid="stSidebar"] > div {
            width: 260px !important;
        }

        /* Setzt individuelle Abstände für den Divider in der Sidebar */
        section[data-testid="stSidebar"] hr {
            margin-top: 1em;
            margin-bottom: 2rem;
        }

        /* Styling der Sidebar-Buttons (gilt für alle Buttons in der Sidebar) */
        section[data-testid="stSidebar"] div[data-testid="stButton"] button {
            border: none;
            width: 100%;
            padding: 0.2rem 0.75rem;
            border-radius: 0.5rem;
            
            display: flex !important;
            justify-content: flex-start !important;
        }

        /* Styling der Sidebar-Buttons (gilt nur für primary Buttons) */
        section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="primary"] {
            background-color: #dfe3e8;
            color: #111827;
        }

        /* Styling der Sidebar-Buttons (gilt nur für secondary Buttons) */
        section[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="secondary"] {
            background-color: transparent;
            color: #1f2937;
        }

        /* Hover-Effekt für Sidebar-Buttons (gilt für alle Buttons*/
        section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {
            background-color: rgba(255, 255, 255, 0.55);
            color: #111827;
        }


        /* Richtet den Text innerhalb der Sidebar-Buttons linksbündig aus */
        section[data-testid="stSidebar"] div[data-testid="stButton"] button span {
            justify-content: flex-start !important;
            text-align: left !important;
            width: 100%;
        }

        /* Verringert den vertikalen Abstand zwischen den Sidebar-Buttons */
        section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
            gap: 0.25rem !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
