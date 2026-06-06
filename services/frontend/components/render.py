import streamlit as st

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

def render_assistant_actions(message_index, message_time):
    with st.container(key=f"assistant_actions_container_{message_index}"):

        time_col, thumbs_up_col, thumbs_down_col, spacer_col = st.columns([1.2, 1, 1, 10])

        with time_col:
            st.caption(message_time)

        with thumbs_up_col:
            if st.button("👍", key=f"thumbs_up_assistant_message_{message_index}"):
                st.session_state[f"assistant_feedback_{message_index}"] = "up"

        with thumbs_down_col:
            if st.button("👎", key=f"thumbs_down_assistant_message_{message_index}"):
                st.session_state[f"assistant_feedback_{message_index}"] = "down"

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