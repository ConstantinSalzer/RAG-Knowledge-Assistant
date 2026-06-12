from schemas import ChatConversation
from services.backend.testdummys import example_chat_conversations


chat_conversations: dict[str, ChatConversation] = {
    conversation.id: conversation for conversation in example_chat_conversations
}


def create_chat_conversation() -> ChatConversation:
    conversation = ChatConversation.create_new()
    chat_conversations[conversation.id] = conversation
    return conversation


def save_chat_conversation(chat_conversation: ChatConversation) -> None:
    chat_conversations[chat_conversation.id] = chat_conversation


def get_chat_conversations() -> list[ChatConversation]:
    return sorted(
        chat_conversations.values(),
        key=lambda conversation: conversation.updated_at,
        reverse=True
    )