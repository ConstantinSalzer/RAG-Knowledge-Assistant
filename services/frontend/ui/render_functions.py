import streamlit as st

# RENDER-FUNKTIONEN FÜR DIE VIEW "AKTUELLER CHAT"

def render_user_message(message_content, message_index, message_time):
    with st.container(key=f"user_message_container_{message_index}"):

        st.markdown(
            f"""
            <div class='chat-user-bubble'>
                {message_content}
            </div>
            """,
            unsafe_allow_html=True
        )

        spacer_col, time_col, button_col = st.columns([7, 1, 1])

        with time_col:
            st.caption(message_time)

        with button_col:
            if st.button("⧉", key=f"copy_user_message_{message_index}"):
                st.session_state.copied_user_message = message_content
                st.toast("Nachricht kopiert")

def render_assistant_message(message_content):

    st.markdown(
        f"""
        <div class='chat-assistant-box'>
            <div class='chat-assistant-bubble'>
                {message_content}
            </div>
        </div>""",
        unsafe_allow_html=True
    )

def render_chunk_message(chunk, message_index, chunk_index):
    file_name = chunk.file_name
    author = chunk.author
    confidence_score = chunk.confidence_score
    content = chunk.content

    title = f"{file_name} | {author} | Score: {confidence_score}"

    with st.container(key=f"chat_chunk_container_{message_index}_{chunk_index}"):
        with st.expander(title, expanded=False):
            st.write(content)

def render_assistant_actions(message_index, message_time, message_content, has_chunks=False):
    sources_key = f"show_sources_assistant_message_{message_index}"

    if sources_key not in st.session_state:
        st.session_state[sources_key] = False

    with st.container(key=f"assistant_actions_container_{message_index}"):

        time_col, copy_col, thumbs_up_col, thumbs_down_col, sources_col, spacer_col = st.columns([1.3, 1, 1, 1, 2.4, 6.6])

        with time_col:
            st.caption(message_time)
        
        with copy_col:
            if st.button("⧉", key=f"copy_assistant_message_{message_index}"):
                st.session_state.copied_assistant_message = message_content
                st.toast("Nachricht kopiert")

        with thumbs_up_col:
            if st.button("👍", key=f"thumbs_up_assistant_message_{message_index}"):
                st.session_state[f"assistant_feedback_{message_index}"] = "up"

        with thumbs_down_col:
            if st.button("👎", key=f"thumbs_down_assistant_message_{message_index}"):
                st.session_state[f"assistant_feedback_{message_index}"] = "down"

        with sources_col:
            if has_chunks:
                button_label = "Quellen" if st.session_state[sources_key] else "Quellen"

                if st.button(button_label, key=f"toggle_sources_assistant_message_{message_index}"):
                    st.session_state[sources_key] = not st.session_state[sources_key]
                    st.rerun()

    return st.session_state[sources_key]

def render_chat_settings_panel():

    st.subheader("Chat Settings")

    chat_settings = st.session_state.chat_settings

    top_k = st.slider(
        "Top-K Chunks",
        chat_settings.MIN_TOP_K,
        chat_settings.MAX_TOP_K,
        value=chat_settings.top_k,
        key="chat_settings_top_k"
    )

    selected_llm = st.selectbox(
        "LLM",
        chat_settings.LLM_OPTIONS,
        index=chat_settings.LLM_OPTIONS.index(chat_settings.llm),
        key="chat_settings_llm"
    )

    prompting_strategy = st.selectbox(
        "Prompting Strategy",
        chat_settings.PROMPT_STRATEGIES,
        index=chat_settings.PROMPT_STRATEGIES.index(chat_settings.prompting_strategy),
        key="chat_settings_prompting_strategy"
    )

    if st.button(
        "Apply Settings",
        use_container_width=True,
        type="primary"
    ):

        chat_settings.top_k = top_k
        chat_settings.llm = selected_llm
        chat_settings.prompting_strategy = prompting_strategy

        st.success("Settings applied!")
    

# RENDER-FUNKTIONEN FÜR DIE VIEW "CHAT HISTORY"

# Rendert die Vorschau einer Konversation. Orientiert sich dabei am Schema aus "aktueller Chat"
def render_chat_history_preview(conversation):
    messages = conversation.get("messages", [])
    conversation_id = conversation["id"]

    if not messages:
        st.caption("Keine Nachrichten vorhanden.")
        return

    with st.container(key=f"history_preview_container_{conversation_id}"):
        for message_index, message in enumerate(messages):
            role = message.get("role", "")
            content = message.get("content", "")

            if role == "user":
                with st.container(key=f"history_user_message_container_{conversation_id}_{message_index}"):
                    st.markdown(
                        f"""
                        <div class='chat-user-bubble'>
                            {content}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            elif role == "assistant":
                st.markdown(
                    f"""
                    <div class='chat-assistant-box'>
                        <div class='chat-assistant-bubble'>
                            {content}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )