import streamlit as st

from services.frontend_actions import copy_to_clipboard_button


# ALLGEMEINE RENDER-FUNKTIONEN

def render_section_header(title):

    st.markdown(
        f"""
        <div class="section-header">
            <div class="section-title">{title}</div>
            <div class="section-line"></div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_list_item(
    item_label,
    item_key,
    action_label,
    action_disabled=False,
    action_url=None
):

    with st.container(key=f"list_item_container_{item_key}"):

        item_col, action_col = st.columns([10, 1.6])

        with item_col:
            with st.container(key=f"list_item_toggle_container_{item_key}"):
                toggle_clicked = st.button(
                    item_label,
                    key=f"toggle_list_item_{item_key}",
                    use_container_width=True
                )

        with action_col:
            with st.container(key=f"list_item_action_container_{item_key}"):

                if action_url:
                    st.link_button(
                        action_label,
                        action_url,
                        use_container_width=True
                    )
                    action_clicked = False

                else:
                    action_clicked = st.button(
                        action_label,
                        key=f"action_list_item_{item_key}",
                        use_container_width=True,
                        disabled=action_disabled
                    )

    return toggle_clicked, action_clicked


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

        spacer_col, time_col, copy_col, rerun_col = st.columns([6, 1, 1, 1])

        with time_col:
            st.caption(message_time)

        with copy_col:
            copy_to_clipboard_button(
                message_content,
                f"copy_user_message_{message_index}"
            )

        with rerun_col:
            if st.button("↻", key=f"rerun_user_message_{message_index}"):
                st.session_state.rerun_query = message_content
                st.rerun()

def render_assistant_message(message_content, message_index, used_web_search=False):

    with st.container(key=f"chat_assistant_box_{message_index}"):
        st.markdown(message_content)

        if used_web_search:
            st.caption("🌐 Diese Antwort basiert auf einer Websuche und nicht auf der Wissensbasis.")

def render_web_search_confirmation(message_index):

    with st.container(key=f"web_search_confirmation_container_{message_index}"):
        return st.button("🌐 Im Web suchen", key=f"confirm_web_search_{message_index}")

def render_chunk_message(chunk, message_index, chunk_index):
    file_name = chunk.file_name
    author = chunk.author
    confidence_score = chunk.confidence_score

    with st.container(key=f"chat_chunk_container_{message_index}_{chunk_index}"):
        st.caption(f"{file_name} | {author} | Score: {confidence_score}")

def render_assistant_actions(message_index, message_time, message_content, has_chunks=False, tokens_used=0):
    sources_key = f"show_sources_assistant_message_{message_index}"

    if sources_key not in st.session_state:
        st.session_state[sources_key] = False

    with st.container(key=f"assistant_actions_container_{message_index}"):

        time_col, copy_col, thumbs_up_col, thumbs_down_col, sources_col, spacer_col = st.columns([1.3, 1, 1, 1, 2.4, 6.6])

        with time_col:
            st.caption(f"{message_time} · {tokens_used} Tokens" if tokens_used else message_time)

        with copy_col:
            copy_to_clipboard_button(
                message_content,
                f"copy_assistant_message_{message_index}"
            )

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

    st.subheader("Chat Einstellungen")

    chat_settings = st.session_state.chat_settings

    role_options = ["technical", "creative", "defensive", "concise", "detailed"]
    provider_options = ["local", "api"]
    mode_options = ["fast", "complex"]

    role = st.selectbox(
        "Rolle",
        role_options,
        index=role_options.index(chat_settings.role),
        key="chat_settings_role"
    )

    provider = st.selectbox(
        "Provider",
        provider_options,
        index=provider_options.index(chat_settings.provider),
        key="chat_settings_provider"
    )

    mode = st.selectbox(
        "Modus",
        mode_options,
        index=mode_options.index(chat_settings.mode),
        key="chat_settings_mode"
    )

    threshold = st.slider(
        "Confidence Threshold",
        min_value=0.0,
        max_value=5.0,
        value=chat_settings.threshold,
        step=0.1,
        key="chat_settings_threshold"
    )

    max_tokens = st.slider(
        "Max Tokens",
        min_value=100,
        max_value=2000,
        value=chat_settings.max_tokens,
        step=50,
        key="chat_settings_max_tokens"
    )

    if st.button(
        "Einstellungen anwenden",
        use_container_width=True,
        type="primary"
    ):

        chat_settings.role = role
        chat_settings.provider = provider
        chat_settings.mode = mode
        chat_settings.threshold = threshold
        chat_settings.max_tokens = max_tokens

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
                with st.container(key=f"history_assistant_box_{conversation_id}_{message_index}"):
                    st.markdown(content)
