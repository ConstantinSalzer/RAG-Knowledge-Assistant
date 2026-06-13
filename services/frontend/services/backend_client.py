import requests # Externe Bibliothek für HTTP-Anfragen
from urllib.parse import quote

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
            f"{self.base_url}/documents",
            files=files,
            timeout=60,
        )

        # Überprüft, ob die Anfrage erfolgreich war, und gibt die JSON-Antwort zurück
        response.raise_for_status()
        return response.json()
    

    def get_documents(self):

        response = requests.get(
            f"{self.base_url}/documents",
            timeout=10,
        )

        response.raise_for_status()
        return response.json()


    def get_document_url(self, file_name):

        encoded_file_name = quote(file_name, safe="")

        return f"{self.base_url}/documents/{encoded_file_name}"