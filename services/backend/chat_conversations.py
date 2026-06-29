from shared.schemas import ChatConversation
from services.backend.db import SessionLocal
from services.backend.models import ConversationRecord


def create_chat_conversation() -> ChatConversation:
    conversation = ChatConversation.create_new()
    save_chat_conversation(conversation)
    return conversation


def save_chat_conversation(chat_conversation: ChatConversation) -> None:
    with SessionLocal() as session:
        record = session.get(ConversationRecord, chat_conversation.id)
        if record:
            # Konversation existiert bereits → nur Daten und Zeitstempel aktualisieren.
            record.data = chat_conversation.model_dump_json()
            record.updated_at = chat_conversation.updated_at
        else:
            session.add(ConversationRecord(
                id=chat_conversation.id,
                data=chat_conversation.model_dump_json(),
                updated_at=chat_conversation.updated_at,
            ))
        session.commit()


def get_chat_conversations() -> list[ChatConversation]:
    with SessionLocal() as session:
        records = (
            session.query(ConversationRecord)
            .order_by(ConversationRecord.updated_at.desc())
            .all()
        )
        return [ChatConversation.model_validate_json(r.data) for r in records]
