from typing import List

from shared.schemas import ChatConversation, ChatMessage, SourceReference

def create_conversation_title_from_message(message: str, max_length: int = 50) -> str:
    clean_message = message.strip()

    if len(clean_message) <= max_length:
        return clean_message

    return clean_message[:max_length] + "..."

# Beispiel Source-Referenzen zum Testen der Chat-Funktionalität
example_sources: List[SourceReference] = [
    SourceReference(
        file_name="machine_learning_basics.pdf",
        author="Max Mustermann",
        confidence_score=4.8,
    ),

    SourceReference(
        file_name="rag_architecture_notes.docx",
        author="Laura Schmidt",
        confidence_score=4.3,
    ),

    SourceReference(
        file_name="database_systems_summary.txt",
        author="Jonas Weber",
        confidence_score=3.9,
    ),

    SourceReference(
        file_name="network_security_script.pdf",
        author="Anna Keller",
        confidence_score=4.6,
    ),

    SourceReference(
        file_name="software_engineering_notes.md",
        author="David Fischer",
        confidence_score=2.7,
    ),
]

# Beispiel Konversationen zum Testen der Chat-Konversations-Funktionalität
example_chat_conversations: list[ChatConversation] = [
    ChatConversation(
        id="7f7d8f91-6d2e-44f1-8df2-34e62dc2c3b7",
        title=create_conversation_title_from_message("Was ist der Unterschied zwischen SQL und NoSQL?"),
        created_at="2026-05-12T10:15:00",
        updated_at="2026-05-12T10:22:00",
        messages=[
            ChatMessage(role="user", content="Was ist der Unterschied zwischen SQL und NoSQL?", created_at="2026-05-12T10:15:00"),
            ChatMessage(role="assistant", content="SQL-Datenbanken arbeiten meist tabellarisch, NoSQL-Datenbanken erlauben flexiblere Datenstrukturen.", created_at="2026-05-12T10:15:20", chunks=[example_sources[2]]),
        ],
    ),
    ChatConversation(
        id="cc0a8b82-4f61-4d0e-99be-b0e1c9f00fa4",
        title=create_conversation_title_from_message("Kannst du mir Retrieval-Augmented Generation einfach erklären?"),
        created_at="2026-06-06T09:30:00",
        updated_at="2026-06-06T09:38:00",
        messages=[
            ChatMessage(role="user", content="Kannst du mir Retrieval-Augmented Generation einfach erklären?", created_at="2026-06-06T09:30:00"),
            ChatMessage(role="assistant", content="RAG kombiniert eine Suche nach relevanten Dokumentstellen mit der Antwortgenerierung durch ein Sprachmodell.", created_at="2026-06-06T09:30:25", chunks=[example_sources[1]]),
            ChatMessage(role="user", content="Warum ist das nützlich?", created_at="2026-06-06T09:34:00"),
            ChatMessage(role="assistant", content="Dadurch kann das Modell Antworten stärker auf vorhandene Dokumente stützen.", created_at="2026-06-06T09:34:20", chunks=[example_sources[1]]),
        ],
    ),
    ChatConversation(
        id="2a50be6c-0d1f-4b46-89f5-f8f2c3a859ea",
        title=create_conversation_title_from_message("Welche Rolle spielen Firewalls in der Netzwerksicherheit?"),
        created_at="2025-08-14T14:40:00",
        updated_at="2025-08-14T14:47:00",
        messages=[
            ChatMessage(role="user", content="Welche Rolle spielen Firewalls in der Netzwerksicherheit?", created_at="2025-08-14T14:40:00"),
            ChatMessage(role="assistant", content="Firewalls überwachen Netzwerkverkehr und können unerlaubte Zugriffe blockieren.", created_at="2025-08-14T14:40:22", chunks=[example_sources[3]]),
        ],
    ),
    ChatConversation(
        id="b3fd6d42-928e-4bdf-bda1-fdfdf66101b8",
        title=create_conversation_title_from_message("Was bedeutet agile Softwareentwicklung im Projektalltag?"),
        created_at="2024-11-20T16:05:00",
        updated_at="2024-11-20T16:13:00",
        messages=[
            ChatMessage(role="user", content="Was bedeutet agile Softwareentwicklung im Projektalltag?", created_at="2024-11-20T16:05:00"),
            ChatMessage(role="assistant", content="Agile Entwicklung arbeitet iterativ, mit regelmäßigem Feedback und enger Zusammenarbeit.", created_at="2024-11-20T16:05:30", chunks=[example_sources[4]]),
            ChatMessage(role="user", content="Gehört Scrum auch dazu?", created_at="2024-11-20T16:09:00"),
            ChatMessage(role="assistant", content="Ja, Scrum gehört zu den bekannten agilen Methoden.", created_at="2024-11-20T16:09:15", chunks=[example_sources[4]]),
        ],
    ),
    ChatConversation(
        id="3d7f239f-c89a-40d2-aae1-53721834c9df",
        title=create_conversation_title_from_message("Was ist Machine Learning in einfachen Worten?"),
        created_at="2026-05-28T11:00:00",
        updated_at="2026-05-28T11:04:00",
        messages=[
            ChatMessage(role="user", content="Was ist Machine Learning in einfachen Worten?", created_at="2026-05-28T11:00:00"),
            ChatMessage(role="assistant", content="Machine Learning bedeutet, dass Computer aus Daten Muster erkennen und daraus lernen.", created_at="2026-05-28T11:00:18", chunks=[example_sources[0]]),
        ],
    ),
    ChatConversation(
        id="de06cf44-47c6-42d6-a9a0-75fc143e8a11",
        title=create_conversation_title_from_message("Kann eine Firewall Phishing-Angriffe vollständig verhindern?"),
        created_at="2026-04-03T09:20:00",
        updated_at="2026-04-03T09:25:00",
        messages=[
            ChatMessage(role="user", content="Kann eine Firewall Phishing-Angriffe vollständig verhindern?", created_at="2026-04-03T09:20:00"),
            ChatMessage(role="assistant", content="Dazu finde ich in den bereitgestellten Dokumenten keine vollständige Antwort.", created_at="2026-04-03T09:20:22", chunks=[]),
        ],
    ),
    ChatConversation(
        id="6f41ab71-b48d-4491-a0b3-d913b7aef70b",
        title=create_conversation_title_from_message("Wie unterscheiden sich relationale Datenbanken von flexiblen Datenmodellen?"),
        created_at="2023-10-02T13:15:00",
        updated_at="2023-10-02T13:23:00",
        messages=[
            ChatMessage(role="user", content="Wie unterscheiden sich relationale Datenbanken von flexiblen Datenmodellen?", created_at="2023-10-02T13:15:00"),
            ChatMessage(role="assistant", content="Relationale Datenbanken verwenden Tabellen, während flexible Modelle weniger starre Strukturen nutzen.", created_at="2023-10-02T13:15:28", chunks=[example_sources[2]]),
        ],
    ),
    ChatConversation(
        id="24e4a6e0-0d2a-4529-a2c0-7e06e2f6203f",
        title=create_conversation_title_from_message("Welche Dokumentstellen nutzt ein RAG-System für seine Antwort?"),
        created_at="2026-05-19T15:45:00",
        updated_at="2026-05-19T15:54:00",
        messages=[
            ChatMessage(role="user", content="Welche Dokumentstellen nutzt ein RAG-System für seine Antwort?", created_at="2026-05-19T15:45:00"),
            ChatMessage(role="assistant", content="Es nutzt relevante Chunks aus Dokumenten als Kontext für das Sprachmodell.", created_at="2026-05-19T15:45:24", chunks=[example_sources[1]]),
            ChatMessage(role="user", content="Werden alle Dokumente komplett an das Modell gegeben?", created_at="2026-05-19T15:50:00"),
            ChatMessage(role="assistant", content="Nein, typischerweise werden nur relevante Ausschnitte übergeben.", created_at="2026-05-19T15:50:18", chunks=[example_sources[1]]),
        ],
    ),
    ChatConversation(
        id="99c6ac79-b643-46c2-8b87-4bcfc94f4931",
        title=create_conversation_title_from_message("Was ist ein Embedding-Modell und wie funktioniert es?"),
        created_at="2026-03-18T08:30:00",
        updated_at="2026-03-18T08:34:00",
        messages=[
            ChatMessage(role="user", content="Was ist ein Embedding-Modell und wie funktioniert es?", created_at="2026-03-18T08:30:00"),
            ChatMessage(role="assistant", content="Dazu finde ich in den bereitgestellten Chunks keine passende Antwort.", created_at="2026-03-18T08:30:18", chunks=[]),
        ],
    ),
    ChatConversation(
        id="0ff63e87-68db-474e-826d-8e34238f1f01",
        title=create_conversation_title_from_message("Warum ist regelmäßiges Feedback bei agiler Entwicklung wichtig?"),
        created_at="2026-05-30T17:05:00",
        updated_at="2026-05-30T17:12:00",
        messages=[
            ChatMessage(role="user", content="Warum ist regelmäßiges Feedback bei agiler Entwicklung wichtig?", created_at="2026-05-30T17:05:00"),
            ChatMessage(role="assistant", content="Feedback hilft dabei, Anforderungen und Umsetzung schrittweise anzupassen.", created_at="2026-05-30T17:05:21", chunks=[example_sources[4]]),
        ],
    ),
    ChatConversation(
        id="e18fd613-5c42-42f3-9696-5ce6ea5d4cb6",
        title=create_conversation_title_from_message("Was passiert bei einem unerlaubten Zugriff im Netzwerk?"),
        created_at="2024-04-12T12:10:00",
        updated_at="2024-04-12T12:16:00",
        messages=[
            ChatMessage(role="user", content="Was passiert bei einem unerlaubten Zugriff im Netzwerk?", created_at="2024-04-12T12:10:00"),
            ChatMessage(role="assistant", content="Firewalls können solche Zugriffe erkennen und blockieren.", created_at="2024-04-12T12:10:25", chunks=[example_sources[3]]),
            ChatMessage(role="user", content="Kann man damit auch Daten verschlüsseln?", created_at="2024-04-12T12:14:00"),
            ChatMessage(role="assistant", content="Dazu finde ich keine eindeutige Antwort in den bereitgestellten Dokumenten.", created_at="2024-04-12T12:14:20", chunks=[]),
        ],
    ),
    ChatConversation(
        id="f09546ce-5fb4-4725-b2fa-d77d43e9f984",
        title=create_conversation_title_from_message("Wie lernt ein Computer aus Daten ohne explizite Programmierung?"),
        created_at="2026-06-06T18:20:00",
        updated_at="2026-06-06T18:27:00",
        messages=[
            ChatMessage(role="user", content="Wie lernt ein Computer aus Daten ohne explizite Programmierung?", created_at="2026-06-06T18:20:00"),
            ChatMessage(role="assistant", content="Beim Machine Learning werden Muster in Daten erkannt und für neue Fälle genutzt.", created_at="2026-06-06T18:20:30", chunks=[example_sources[0]]),
        ],
    ),
    ChatConversation(
        id="ab7c4d08-e625-4fbc-a919-f56b45bfad4a",
        title=create_conversation_title_from_message("Welche Vorteile haben NoSQL-Datenbanken bei großen verteilten Systemen?"),
        created_at="2025-11-03T10:35:00",
        updated_at="2025-11-03T10:43:00",
        messages=[
            ChatMessage(role="user", content="Welche Vorteile haben NoSQL-Datenbanken bei großen verteilten Systemen?", created_at="2025-11-03T10:35:00"),
            ChatMessage(role="assistant", content="NoSQL-Datenbanken eignen sich besonders für große, verteilte Systeme und flexible Datenstrukturen.", created_at="2025-11-03T10:35:26", chunks=[example_sources[2]]),
        ],
    ),
    ChatConversation(
        id="92c1cbd8-0ad5-4b5c-a2d0-08656e37d0d3",
        title=create_conversation_title_from_message("Kannst du mir erklären, ob Kanban und Scrum dasselbe sind?"),
        created_at="2026-05-06T09:55:00",
        updated_at="2026-05-06T10:02:00",
        messages=[
            ChatMessage(role="user", content="Kannst du mir erklären, ob Kanban und Scrum dasselbe sind?", created_at="2026-05-06T09:55:00"),
            ChatMessage(role="assistant", content="Beide gehören zu agilen Methoden, sind aber unterschiedliche Vorgehensweisen.", created_at="2026-05-06T09:55:20", chunks=[example_sources[4]]),
            ChatMessage(role="user", content="Welche ist besser?", created_at="2026-05-06T09:59:00"),
            ChatMessage(role="assistant", content="Dazu finde ich in den bereitgestellten Dokumenten keine Bewertung.", created_at="2026-05-06T09:59:18", chunks=[]),
        ],
    ),
    ChatConversation(
        id="0db889ea-3215-44d1-9f6a-c6747d6ff5a7",
        title=create_conversation_title_from_message("Was bedeutet Kontext bei Retrieval-Augmented Generation?"),
        created_at="2026-02-07T14:05:00",
        updated_at="2026-02-07T14:11:00",
        messages=[
            ChatMessage(role="user", content="Was bedeutet Kontext bei Retrieval-Augmented Generation?", created_at="2026-02-07T14:05:00"),
            ChatMessage(role="assistant", content="Kontext sind relevante Dokumentstellen, die dem Sprachmodell für die Antwort mitgegeben werden.", created_at="2026-02-07T14:05:22", chunks=[example_sources[1]]),
        ],
    ),
    ChatConversation(
        id="d36003a9-8068-4476-b179-9f2da1f6481e",
        title=create_conversation_title_from_message("Welche typischen Anwendungsbereiche hat Machine Learning?"),
        created_at="2024-08-22T11:45:00",
        updated_at="2024-08-22T11:52:00",
        messages=[
            ChatMessage(role="user", content="Welche typischen Anwendungsbereiche hat Machine Learning?", created_at="2024-08-22T11:45:00"),
            ChatMessage(role="assistant", content="Typische Bereiche sind Bildverarbeitung, Sprachverarbeitung und Empfehlungssysteme.", created_at="2024-08-22T11:45:24", chunks=[example_sources[0]]),
        ],
    ),
    ChatConversation(
        id="6a60914d-7ff8-420d-9852-873871849eca",
        title=create_conversation_title_from_message("Was ist der Unterschied zwischen Daten verschlüsseln und Daten speichern?"),
        created_at="2025-03-16T15:20:00",
        updated_at="2025-03-16T15:29:00",
        messages=[
            ChatMessage(role="user", content="Was ist der Unterschied zwischen Daten verschlüsseln und Daten speichern?", created_at="2025-03-16T15:20:00"),
            ChatMessage(role="assistant", content="Speichern legt Daten ab, Verschlüsselung schützt sie vor unbefugtem Zugriff.", created_at="2025-03-16T15:20:28", chunks=[example_sources[3]]),
        ],
    ),
    ChatConversation(
        id="62f27d5e-e0f4-4a59-b33a-cd2bc4a2dfad",
        title=create_conversation_title_from_message("Kann ein RAG-System automatisch perfekte Antworten geben?"),
        created_at="2026-05-24T13:10:00",
        updated_at="2026-05-24T13:18:00",
        messages=[
            ChatMessage(role="user", content="Kann ein RAG-System automatisch perfekte Antworten geben?", created_at="2026-05-24T13:10:00"),
            ChatMessage(role="assistant", content="Nein, RAG verbessert die Kontextnutzung, garantiert aber keine perfekten Antworten.", created_at="2026-05-24T13:10:24", chunks=[example_sources[1]]),
            ChatMessage(role="user", content="Was passiert, wenn kein passender Chunk gefunden wird?", created_at="2026-05-24T13:15:00"),
            ChatMessage(role="assistant", content="Dann sollte das System sagen, dass keine passende Antwort gefunden wurde.", created_at="2026-05-24T13:15:20", chunks=[]),
        ],
    ),
    ChatConversation(
        id="a9b08f98-cc15-422d-a661-7a57c5ed9323",
        title=create_conversation_title_from_message("Warum sind iterative Entwicklungszyklen in agilen Projekten nützlich?"),
        created_at="2024-01-29T09:00:00",
        updated_at="2024-01-29T09:07:00",
        messages=[
            ChatMessage(role="user", content="Warum sind iterative Entwicklungszyklen in agilen Projekten nützlich?", created_at="2024-01-29T09:00:00"),
            ChatMessage(role="assistant", content="Sie ermöglichen schrittweise Entwicklung, regelmäßige Prüfung und Anpassung.", created_at="2024-01-29T09:00:25", chunks=[example_sources[4]]),
        ],
    ),
    ChatConversation(
        id="5b96ea9b-53b5-4660-a895-5469c2e0f796",
        title=create_conversation_title_from_message("Welche Datenstruktur nutzen relationale Datenbanken normalerweise?"),
        created_at="2026-05-02T08:40:00",
        updated_at="2026-05-02T08:47:00",
        messages=[
            ChatMessage(role="user", content="Welche Datenstruktur nutzen relationale Datenbanken normalerweise?", created_at="2026-05-02T08:40:00"),
            ChatMessage(role="assistant", content="Relationale Datenbanken speichern Daten normalerweise tabellarisch.", created_at="2026-05-02T08:40:20", chunks=[example_sources[2]]),
        ],
    ),
]