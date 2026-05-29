from fastapi import FastAPI
from typing import List
from services.backend.chat_models import ChatRequest, ChatResponse
from services.backend.chunks import example_chunks, Chunk

app = FastAPI()


@app.post("/chat", response_model=ChatResponse)
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