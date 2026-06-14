import os
import json
import requests
import time
from typing import List

from shared.schemas import Chunk


# 1. System Prompt Templates

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

# 3. Helper: Tavily Search Crawler

def _fetch_tavily_fallback_context(query: str) -> str:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        print("[TAVILY] Warning: TAVILY_API_KEY not set. Skipping live web crawl.\n")
        return ""

    print(f"[TAVILY] Crawling live web via Tavily for: '{query}'...\n")
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",            
        "include_answer": False             
    }

    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        web_context = ""
        results = data.get("results", [])
        for i, res in enumerate(results[:3]): 
            web_context += f"Web Source {i+1}: {res.get('title')}\nURL: {res.get('url')}\nContent: {res.get('content')}\n\n"
            
        return web_context
    except Exception as e:
        print(f"[TAVILY] Tavily crawl failed: {e}\n")
        return ""

# 4. Helper: Request Builders

def _prepare_local_request(query: str, context: str, system_prompt: str):
    base_url = os.getenv("OLLAMA_BASE_URL", "http://rag_ollama:11434")
    url = f"{base_url.rstrip('/')}/api/generate"
    
    full_prompt = f"System: {system_prompt}\n\nKontext:\n{context}\nNutzer Frage: {query}\nAntwort:"
    payload = {
        "model": os.getenv("GENERATION_MODEL", "qwen2.5:1.5b"),
        "prompt": full_prompt,
        "stream": True,
        "keep_alive": "10m"         # keeps model in memory for 10min, better speed
    }
    return url, payload, {"Content-Type": "application/json"}

def _prepare_api_request(query: str, context: str, system_prompt: str):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set!")
        
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
    return url, payload, headers

# 5. LLM Sufficiency Evaluator
def _is_context_sufficient(query: str, context: str, mode: str) -> bool:
    eval_prompt = (
        "Analysiere, ob der bereitgestellte Kontext ausreicht, um die Frage des Nutzers wahrheitsgemäß zu beantworten.\n"
        "Antworte AUSSCHLIESSLICH mit dem Wort 'JA' oder 'NEIN'. Keine Begründung!\n\n"
        f"Kontext:\n{context}\n\n"
        f"Nutzer Frage: {query}\n"
        "Ausreichend?"
    )
    
    try:
        if mode.lower() == "api":
            url, payload, headers = _prepare_api_request(query="", context="", system_prompt="")
            payload["messages"] = [{"role": "user", "content": eval_prompt}]
            payload["stream"] = False
        else:
            url, payload, headers = _prepare_local_request(query="", context="", system_prompt="")
            payload["prompt"] = eval_prompt
            payload["stream"] = False

        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        if mode.lower() == "api":
            result = response.json()["choices"][0]["message"]["content"].strip().upper()
        else:
            result = response.json().get("response", "").strip().upper()

        print(f"[EVALUATOR] Context sufficient according to LLM? {result}\n")
        return "JA" in result
        
    except Exception as e:
        print(f"[EVALUATOR] Sufficiency evaluation failed: {e}. Defaulting to True.\n")
        return True

# 6. Parsing Helper for Streaming Responses

def _parse_stream_line(line_text: str, mode: str) -> str:
    if mode == "api":
        if line_text.startswith("data: "):
            line_text = line_text[6:]
        if line_text == "[DONE]" or not line_text:
            return ""
            
        chunk_json = json.loads(line_text)
        choices = chunk_json.get("choices", [])
        if choices:
            return choices[0].get("delta", {}).get("content", "")
    else:
        chunk_json = json.loads(line_text)
        return chunk_json.get("response", "")
    return ""

# 7. Main Orchestrator Function

def generate_rag_response(query: str, chunks: List[Chunk], style: str = "technical", mode: str = "local") -> str:

    total_start = time.time()

    system_prompt = system_prompts.get(style, system_prompts["technical"])
    context = "".join([f"Document: {c.file_name} (Author: {c.author})\nContent: {c.content}\n\n" for c in chunks])

    eval_start = time.time()
    needs_tavily = not _is_context_sufficient(query, context, mode)
    eval_time = time.time() - eval_start

    fetch_time = 0

    if needs_tavily:
        fetch_start = time.time()
        print("[TAVILY] Local context insufficient! Activating live internet crawling...\n")
        web_context = _fetch_tavily_fallback_context(query)
        fetch_time = time.time() - fetch_start
        
        if web_context:
            print("[TAVILY] Web metadata injected into generation pipeline.\n")
            context = web_context
        else:
            print("[TAVILY] Web crawl found nothing.\n")
            context = "Keine Dokumente oder Web-Daten vorhanden."

    try:
        if mode.lower() == "api":
            print("[API] Routing request to Cloud API...\n")
            url, payload, headers = _prepare_api_request(query, context, system_prompt)
        else:
            print("[LOCAL] Routing request to local Ollama container...\n")
            url, payload, headers = _prepare_local_request(query, context, system_prompt)
            
        gen_start = time.time()
        response = requests.post(url, json=payload, headers=headers, timeout=60, stream=True)
        response.raise_for_status()
        
        print(f"--- RESPONSE ({mode.upper()} - {style.upper()} MODE) ---\n")
        
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8', errors='replace').strip()
                text_piece = _parse_stream_line(decoded_line, mode.lower())
                if text_piece:
                    print(text_piece, end="", flush=True)
        
        gen_time = time.time() - gen_start

        total_duration = time.time() - total_start
        print("\n\n")
        print(f"[PERFORMANCE] Eval: {eval_time:.2f}s | Fetch: {fetch_time:.2f}s | Gen: {gen_time:.2f}s")
        print(f"[PERFORMANCE] Total Execution Time: {total_duration:.2f}s")
        print("\n")
        
        return "Streaming complete."
        
    except Exception as e:
        return f"Error contacting {mode.upper()} LLM: {e}"


if __name__ == "__main__":
    test_query = "Erkläre den Begriff RAG?"                     # choose any question, current chunks are regarding RAG
    test_style = "defensive"                                    # defensive, technical, creative        
    test_mode = "local"                                         # local, api
    # test_model_size = "small"                                 # small, medium, (large not supported in local mode right now)
    # test_resp_len = "small"                                   # small, medium, large (150, 500, 1000 Token)


    print(f"[INPUT] Asking LLM ({test_style.upper()} Mode) via {test_mode.upper()} engine: {test_query}\n")
    
    generate_rag_response(
        query=test_query, 
        chunks=example_chunks, 
        style=test_style,
        mode=test_mode
    )