# Datenbankverbindung für den Backend-Service.
# Spiegelt den Aufbau des Retrieval-Service (services/retrieval/app/db.py),
# arbeitet aber auf derselben PostgreSQL-Instanz mit eigener Tabelle (conversations).
import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Im Docker-Netzwerk wird DATABASE_URL per docker-compose gesetzt.
# Der Fallback gilt für lokale Entwicklung ohne Docker.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:password123@localhost:5432/rag_db",
)


class Base(DeclarativeBase):
    pass


# pool_pre_ping prüft die Verbindung vor jeder Nutzung – verhindert Fehler nach längerer Inaktivität.
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    # Import hier, damit Base das Modell kennt bevor create_all aufgerufen wird.
    from services.backend.models import ConversationRecord  # noqa: F401

    Base.metadata.create_all(bind=engine)


def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
