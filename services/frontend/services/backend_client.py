import requests # Externe Bibliothek für HTTP-Anfragen

# Zuständige Klasse für die Kommunikation mit dem Backend (sauberes Kapseln)
class BackendClient:

    # Konstruktor, der die Basis-URL des Backends festlegt (hier lokal auf Port 8000)
    def __init__(self):

        self.base_url = "http://127.0.0.1:8000"

    # Funktion, die eine Chat-Nachricht des Benutzers (= message) an das Backend sendet 
    def send_chat_message(self, message):

        # POST-Anfrage an den /chat-Endpunkt des Backends mit JSON-Daten
        response = requests.post(
            f"{self.base_url}/chat",
            json={
                "message": message
            }
        )

        return response.json()