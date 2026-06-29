# Datenbankmodell für gespeicherte Chat-Konversationen.
# Die gesamte Konversation (inkl. aller Nachrichten) wird als JSON-String in `data` abgelegt,
# anstatt Nachrichten in eigene Tabellen aufzuteilen – das hält das Schema einfach und
# passt gut zu den Pydantic-Modellen in shared/schemas.py (einfaches serialize/deserialize).
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from services.backend.db import Base


class ConversationRecord(Base):
    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    data: Mapped[str] = mapped_column(Text, nullable=False)
    # updated_at wird separat gespeichert, damit die DB-Abfrage nach Datum sortieren kann,
    # ohne das JSON parsen zu müssen.
    updated_at: Mapped[str] = mapped_column(String(64), nullable=False)
