# Standard Imports
import os
import json
import requests
from typing import List

# Local workspace imports
from schemas import Chunk

# system prompt temmplates

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

# example chunks

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

# helper local llm

def _prepare_local_request(query: str, context: str, system_prompt: str):
    
    # local ollama
    base_url = os.getenv("OLLAMA_BASE_URL", "http://rag_ollama:11434")
    url = f"{base_url.rstrip('/')}/api/generate"
    
    # prepare payload
    full_prompt = f"System: {system_prompt}\n\nKontext:\n{context}\nNutzer Frage: {query}\nAntwort:"
    payload = {
        "model": os.getenv("GENERATION_MODEL", "qwen2.5:1.5b"),
        "prompt": full_prompt,
        "stream": True 
    }

    # return url, payload, headers
    return url, payload, {"Content-Type": "application/json"}

# helper api llm

def _prepare_api_request(query: str, context: str, system_prompt: str):
    
    # gemini cloud api    
    api_key = os.getenv("GEMINI_API_KEY")

    # error handling for missing API key
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set!")

    # prepare request details    
    url = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gemini-2.5-flash",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Kontext:\n{context}\nNutzer Frage: {query}"}
        ],
        "stream": True
    }

    # return results for API request
    return url, payload, headers

# parsing helper for streaming responses

def _parse_stream_line(line_text: str, mode: str) -> str:

    # api mode
    if mode == "api":

        if line_text.startswith("data: "):
            line_text = line_text[6:]
        if line_text == "[DONE]" or not line_text:
            return ""
            
        chunk_json = json.loads(line_text)
        choices = chunk_json.get("choices", [])
        if choices:
            return choices[0].get("delta", {}).get("content", "")
    
    # local mode
    else:
        chunk_json = json.loads(line_text)
        return chunk_json.get("response", "")
    return ""

# main orchestrator function
def generate_rag_response(query: str, chunks: List[Chunk], style: str = "technical", mode: str = "local") -> str:

    # prepare inputs 
    system_prompt = system_prompts.get(style, system_prompts["technical"])
    context = "".join([f"Document: {c.file_name} (Author: {c.author})\nContent: {c.content}\n\n" for c in chunks])

    try:
        # Step 1: delegate to api or local
        if mode.lower() == "api":
            print("Routing request to Google Gemini API (gemini-2.5-flash)...")
            url, payload, headers = _prepare_api_request(query, context, system_prompt)
        else:
            print("Routing request to local Ollama container...")
            url, payload, headers = _prepare_local_request(query, context, system_prompt)
            
        # Step 2: execute request
        response = requests.post(url, json=payload, headers=headers, timeout=30, stream=True)
        response.raise_for_status()
        
        print(f"--- Response ({mode.upper()} - {style.upper()} Mode) ---")
        
        # Step 3: Stream and parse on the fly
        for line in response.iter_lines():
            if line:
                text_piece = _parse_stream_line(line.decode('utf-8').strip(), mode.lower())
                if text_piece:
                    print(text_piece, end="", flush=True)
        
        print("\n")
        return "Streaming complete."
        
    except Exception as e:
        return f"Error contacting {mode.upper()} LLM: {e}"


if __name__ == "__main__":
    
    # testing configuration variables
    test_query = "Erkläre den Begriff RAG?"
    test_style = "defensive"                            # defensive, technical, creative
    test_mode = "local"                                 # api, local

    print(f"Asking LLM ({test_style.upper()} Mode) via {test_mode.upper()} engine: {test_query}\n")
    
    # Run the slim orchestrator
    generate_rag_response(
        query=test_query, 
        chunks=example_chunks, 
        style=test_style,
        mode=test_mode
    )