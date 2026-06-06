from fastapi import APIRouter

from schemas import ChatConversation
from services.backend.chat_models import ChatRequest, ChatResponse
from services.backend.testdummys import example_chunks
from services.backend.chat_conversations import (
    create_chat_conversation,
    get_chat_conversations,
    save_chat_conversation,
)

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    user_message = request.message
    settings = request.chat_settings

    ai_response = (
        f"Backend received: {user_message}<br><br>"
        f"Current Chat Settings:<br>"
        f"top_k = {settings.top_k}<br>"
        f"llm = {settings.llm}<br>"
        f"prompting_strategy = {settings.prompting_strategy}<br>"
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