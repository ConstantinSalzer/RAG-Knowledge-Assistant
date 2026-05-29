# Standard Imports
import os
import json
import requests
from typing import List

# Local workspace imports
from schemas import Chunk

# 1. Different Prompts

system_prompts = {
    "technical": (
        """Du bist ein präziser, technischer Experte. Beantworte die Frage des Nutzers
        ausschließlich basierend auf dem bereitgestellten Kontext. Nutze Fachbegriffe,
        bleibe absolut sachlich und strukturiere die Antwort klar."""
    ),
    "creative": (
        """Du bist ein kreativer Assistent. Beantworte die Frage des Nutzers basierend
        auf dem Kontext, aber nutze Analogien, anschauliche Metaphern und einen 
        begeisternden, lockeren Tonfall."""
    ),
    "defensive": (
        """Du bist ein extrem vorsichtiger IT-Sicherheitsanalyst. Beantworte die Frage 
        streng nach dem Kontext. Wenn eine Information nicht zu 100% im Kontext steht, 
        sage explizit 'Das kann ich anhand der Dokumente nicht beantworten'. Vermeide jede Spekulation."""
    )
}

# 2. Example Chunks

example_chunks: List[Chunk] = [
    Chunk(
        file_name="machine_learning_basics.pdf",
        author="Max Mustermann",
        confidence_score=4.8,
        content="""Machine Learning bezeichnet Verfahren, bei denen Computer aus Daten lernen, 
        ohne explizit programmiert zu werden. Typische Anwendungsbereiche sind
        Bildverarbeitung, Sprachverarbeitung und Empfehlungssysteme."""
    ),

    Chunk(
        file_name="rag_architecture_notes.docx",
        author="Laura Schmidt",
        confidence_score=4.3,
        content="""Retrieval-Augmented Generation kombiniert klassische Informationssuche
        mit Large Language Models. Relevante Dokumente werden zunächst gesucht
        und anschließend als Kontext an das Sprachmodell übergeben."""
    ),

    Chunk(
        file_name="database_systems_summary.txt",
        author="Jonas Weber",
        confidence_score=3.9,
        content="""Relationale Datenbanken speichern Daten tabellarisch und verwenden SQL
        für Abfragen. NoSQL-Datenbanken bieten dagegen flexible Datenstrukturen
        und eignen sich besonders für große, verteilte Systeme."""
    ),

    Chunk(
        file_name="network_security_script.pdf",
        author="Anna Keller",
        confidence_score=4.6,
        content="""Firewalls überwachen den Netzwerkverkehr und blockieren unerlaubte Zugriffe.
        Zusätzlich werden Verschlüsselungsverfahren eingesetzt, um Daten vor
        Manipulation und unbefugtem Zugriff zu schützen."""
    ),

    Chunk(
        file_name="software_engineering_notes.md",
        author="David Fischer",
        confidence_score=2.7,
        content="""Agile Softwareentwicklung basiert auf iterativen Entwicklungszyklen,
        regelmäßigem Feedback und enger Zusammenarbeit im Team.
        Scrum und Kanban gehören zu den bekanntesten agilen Methoden."""
    )
]

# 3. function rag response with dynamic system prompt injection
def generate_rag_response(query: str, chunks: List[Chunk], style: str = "technical") -> str:

    # Fallback to technical if an invalid style is passed
    system_prompt = system_prompts.get(style, system_prompts["technical"])

    base_url = os.getenv("OLLAMA_BASE_URL", "http://rag_ollama:11434")
    OLLAMA_URL = f"{base_url.rstrip('/')}/api/generate"
    MODEL_NAME = os.getenv("GENERATION_MODEL", "qwen2.5:1.5b")
    
    # Build context
    context = ""
    for chunk in chunks:
        context += f"Document: {chunk.file_name} (Author: {chunk.author})\n"
        context += f"Content: {chunk.content}\n\n"

    # Injected the dynamic system prompt here
    full_prompt = f"System: {system_prompt}\n\nKontext:\n{context}\nNutzer Frage: {query}\nAntwort:"

    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": True 
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30, stream=True)
        response.raise_for_status()
        
        print(f"--- Response ({style.upper()} Mode) ---")
        
        # streaming loop
        for line in response.iter_lines():
            if line:
                chunk_json = json.loads(line.decode('utf-8'))
                text_piece = chunk_json.get("response", "")
                print(text_piece, end="", flush=True)
        
        print("\n")
        return "Streaming complete."
        
    except requests.exceptions.RequestException as e:
        return f"Error contacting local LLM: {e}"


if __name__ == "__main__":
    
    # testing temp vars
    test_query = "Was ist Retrieval-Augmented Generation?"
    test_style = "technical"  

    print(f"Asking LLM ({test_style.upper()} Mode): {test_query}\n")
    
    # Run the generator using your temporary variables
    generate_rag_response(
        query=test_query, 
        chunks=example_chunks, 
        style=test_style
    )