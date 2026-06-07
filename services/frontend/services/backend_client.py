import requests # Externe Bibliothek für HTTP-Anfragen

# Zuständige Klasse für die Kommunikation mit dem Backend (sauberes Kapseln)
class BackendClient:

    # Konstruktor, der die Basis-URL des Backends festlegt (hier lokal auf Port 8000)
    def __init__(self):

        self.base_url = "http://127.0.0.1:8000"

    # Funktion, die eine Chat-Nachricht des Benutzers (= message) an das Backend sendet 
    def send_chat_message(self, message, chat_settings):

        # POST-Anfrage an den /chat-Endpunkt des Backends mit JSON-Daten
        response = requests.post(
            f"{self.base_url}/chat",
            json={
                "message": message,
                "chat_settings": {
                    "top_k": chat_settings.top_k,
                    "llm": chat_settings.llm,
                    "prompting_strategy": chat_settings.prompting_strategy
                }
            }
        )

        response.raise_for_status()
        return response.json()
    
    # Erhält gespeicherte Chat-Konversationen aus dem Backend
    def get_chat_conversations(self):

        response = requests.get(
            f"{self.base_url}/chat-conversations"
        )

        response.raise_for_status()
        return response.json()
    
    # Speichert eine Konversation und gibt diese ans Backend weiter
    def save_chat_conversation(self, chat_conversation):

        response = requests.put(
            f"{self.base_url}/chat-conversations/{chat_conversation.id}",
            json=chat_conversation.model_dump()
        )

        response.raise_for_status()