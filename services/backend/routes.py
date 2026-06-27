import logging
import os
from pathlib import Path

import requests
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from shared.schemas import ChatConversation
from services.backend.chat_conversations import (
    create_chat_conversation,
    get_chat_conversations,
    save_chat_conversation,
)

logger = logging.getLogger(__name__)

router = APIRouter()

DOCUMENTS_DIRECTORY = Path(__file__).parent / "documents"
DOCUMENTS_DIRECTORY.mkdir(exist_ok=True)

RETRIEVAL_URL = os.getenv("RETRIEVAL_URL", "http://retrieval:8001")


@router.post("/chat-conversations", response_model=ChatConversation)
def post_chat_conversation():
    return create_chat_conversation()


@router.get("/chat-conversations", response_model=list[ChatConversation])
def get_all_chat_conversations():
    return get_chat_conversations()


@router.put("/chat-conversations/{conversation_id}")
def put_chat_conversation(
    conversation_id: str,
    chat_conversation: ChatConversation
):
    save_chat_conversation(chat_conversation)


@router.post("/documents")
def upload_documents(
    files: list[UploadFile] = File(...)
):
    saved_files = []

    for uploaded_file in files:
        file_name = Path(uploaded_file.filename).name
        file_path = DOCUMENTS_DIRECTORY / file_name
        file_bytes = uploaded_file.file.read()

        with file_path.open("wb") as target_file:
            target_file.write(file_bytes)

        chunks_stored = 0
        try:
            resp = requests.post(
                f"{RETRIEVAL_URL}/ingest",
                files={"file": (file_name, file_bytes, uploaded_file.content_type or "application/pdf")},
                data={"title": Path(file_name).stem, "author": "Unknown"},
                timeout=120,
            )
            if resp.ok:
                chunks_stored = resp.json().get("chunks_stored", 0)
        except Exception as exc:
            logger.warning(f"Ingestion failed for {file_name}: {exc}")

        saved_files.append({"name": file_name, "chunks_stored": chunks_stored})

    return {
        "count": len(saved_files),
        "files": saved_files,
    }


@router.get("/documents")
def get_documents():

    documents = []

    for file_path in DOCUMENTS_DIRECTORY.iterdir():
        if file_path.is_file():
            documents.append({
                "name": file_path.name,
                "size": file_path.stat().st_size,
                "modified_at": file_path.stat().st_mtime,
            })

    return documents


@router.get("/documents/{file_name}")
def open_document(file_name: str):

    safe_file_name = Path(file_name).name
    file_path = DOCUMENTS_DIRECTORY / safe_file_name

    if not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Dokument wurde nicht gefunden."
        )

    if file_path.suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Nur PDF-Dateien können geöffnet werden."
        )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=safe_file_name,
        content_disposition_type="inline"
    )