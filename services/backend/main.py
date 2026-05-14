from fastapi import FastAPI
from models.chat_models import ChatRequest, ChatResponse

app = FastAPI()


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    user_message = request.message

    ai_response = f"Backend received: {user_message}"

    print(user_message)

    return ChatResponse(
        response=ai_response
    )