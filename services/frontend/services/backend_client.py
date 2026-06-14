import os
from typing import List
from urllib.parse import quote

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

    # Übergibt die im Fontend hochgeladenen Dokumente ans Backend
    def upload_documents(self, uploaded_files):

        # Erstellt eine Liste von Dateien, die für den Multipart-Upload kompatibel sind (Name, Inhalt, Typ)
        files = []

        for uploaded_file in uploaded_files:
            file = (
                "files",
                (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            )

            files.append(file)

        # Sendet einen POST-Request an den /documents-Endpunkt des Backends mit den Dateien als Multipart-Formulardaten
        response = requests.post(
            f"{self.backend_url}/documents",
            files=files,
            timeout=60,
        )

        # Überprüft, ob die Anfrage erfolgreich war, und gibt die JSON-Antwort zurück
        response.raise_for_status()
        return response.json()

    def get_documents(self):

        response = requests.get(
            f"{self.backend_url}/documents",
            timeout=10,
        )

        response.raise_for_status()
        return response.json()

    def get_document_url(self, file_name):

        encoded_file_name = quote(file_name, safe="")

        return f"{self.backend_url}/documents/{encoded_file_name}"
