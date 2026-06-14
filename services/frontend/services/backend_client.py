import os
from typing import List

import requests

from shared.schemas import ChatMessage, ChatRequest, ChatResponse, Settings


# Zuständige Klasse für die Kommunikation mit Pipeline- und Backend-Service (sauberes Kapseln)
class BackendClient:

    # Konstruktor, der die Basis-URLs der Services festlegt (per ENV überschreibbar fürs Docker-Netzwerk)
    def __init__(self):

        self.pipeline_url = os.environ.get("PIPELINE_URL", "http://127.0.0.1:8000")
        self.backend_url = os.environ.get("BACKEND_URL", "http://127.0.0.1:8001")

    # Sendet eine Chat-Nachricht des Benutzers (= query) an den Pipeline-Service und liefert die ChatResponse
    def send_chat_message(self, query: str, settings: Settings, history: List[ChatMessage] = None, confirm_web_search: bool = False) -> ChatResponse:

        request = ChatRequest(query=query, settings=settings, history=history or [], confirm_web_search=confirm_web_search)

        response = requests.post(
            f"{self.pipeline_url}/augment",
            json=request.model_dump()
        )

        response.raise_for_status()
        return ChatResponse.model_validate(response.json())

    # Erhält gespeicherte Chat-Konversationen aus dem Backend
    def get_chat_conversations(self):

        response = requests.get(
            f"{self.backend_url}/chat-conversations"
        )

        response.raise_for_status()
        return response.json()

    # Speichert eine Konversation und gibt diese ans Backend weiter
    def save_chat_conversation(self, chat_conversation):

        response = requests.put(
            f"{self.backend_url}/chat-conversations/{chat_conversation.id}",
            json=chat_conversation.model_dump()
        )

        response.raise_for_status()
