from pathlib import Path
from shutil import copyfileobj

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from schemas import ChatConversation
from services.backend.chat_models import ChatRequest, ChatResponse
from services.backend.testdummys import example_chunks
from services.backend.chat_conversations import (
    create_chat_conversation,
    get_chat_conversations,
    save_chat_conversation,
)

router = APIRouter()

DOCUMENTS_DIRECTORY = Path(__file__).parent / "documents"
DOCUMENTS_DIRECTORY.mkdir(exist_ok=True)


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    user_message = request.message
    settings = request.chat_settings

    ai_response = (
        f"Backend received: {user_message}\n\n"
        f"Current Chat Settings:\n"
        f"top_k = {settings.top_k}\n"
        f"llm = {settings.llm}\n"
        f"prompting_strategy = {settings.prompting_strategy}\n"
    )
    
    sorted_chunks = sorted(example_chunks, key=lambda c: c.confidence_score, reverse=True)
    top_k_chunks = sorted_chunks[:request.chat_settings.top_k]

    print(user_message)

    return ChatResponse(
        response=ai_response,
        chunks=top_k_chunks
    )


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

        with file_path.open("wb") as target_file:
            copyfileobj(uploaded_file.file, target_file)

        saved_files.append(file_name)

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