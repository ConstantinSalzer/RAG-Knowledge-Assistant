from pydantic import BaseModel
from typing import List


class Chunk(BaseModel):
    file_name: str
    author: str
    confidence_score: float
    content: str


example_chunks: List[Chunk] = [
    Chunk(
        file_name="machine_learning_basics.pdf",
        author="Max Mustermann",
        confidence_score=4.8,
        content="""
Machine Learning bezeichnet Verfahren, bei denen Computer aus Daten lernen,
ohne explizit programmiert zu werden. Typische Anwendungsbereiche sind
Bildverarbeitung, Sprachverarbeitung und Empfehlungssysteme.
"""
    ),

    Chunk(
        file_name="rag_architecture_notes.docx",
        author="Laura Schmidt",
        confidence_score=4.3,
        content="""
Retrieval-Augmented Generation kombiniert klassische Informationssuche
mit Large Language Models. Relevante Dokumente werden zunächst gesucht
und anschließend als Kontext an das Sprachmodell übergeben.
"""
    ),

    Chunk(
        file_name="database_systems_summary.txt",
        author="Jonas Weber",
        confidence_score=3.9,
        content="""
Relationale Datenbanken speichern Daten tabellarisch und verwenden SQL
für Abfragen. NoSQL-Datenbanken bieten dagegen flexible Datenstrukturen
und eignen sich besonders für große, verteilte Systeme.
"""
    ),

    Chunk(
        file_name="network_security_script.pdf",
        author="Anna Keller",
        confidence_score=4.6,
        content="""
Firewalls überwachen den Netzwerkverkehr und blockieren unerlaubte Zugriffe.
Zusätzlich werden Verschlüsselungsverfahren eingesetzt, um Daten vor
Manipulation und unbefugtem Zugriff zu schützen.
"""
    ),

    Chunk(
        file_name="software_engineering_notes.md",
        author="David Fischer",
        confidence_score=2.7,
        content="""
Agile Softwareentwicklung basiert auf iterativen Entwicklungszyklen,
regelmäßigem Feedback und enger Zusammenarbeit im Team.
Scrum und Kanban gehören zu den bekanntesten agilen Methoden.
"""
    )
]