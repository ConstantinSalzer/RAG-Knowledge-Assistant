import math
from typing import List, NamedTuple, Optional

from shared.schemas import Chunk, ChatMessage, SourceReference

from app.search import fetch_webcrawler_results
from app.models import get_embedding

# Reference sentences describing the corpus' topic domains (see get_mock_chunks in main.py).
DOMAIN_TOPICS = [
    "Machine Learning und künstliche Intelligenz: Verfahren, bei denen Computer aus Daten lernen, ohne explizit programmiert zu werden.",
    "Retrieval-Augmented Generation (RAG): Kombination von Informationssuche und Large Language Models.",
    "Datenbanken: relationale und NoSQL-Datenbanksysteme, SQL-Abfragen, Datenspeicherung.",
    "Netzwerksicherheit: Firewalls, Verschlüsselung, Schutz vor unbefugtem Netzwerkzugriff.",
    "Softwareentwicklung: agile Methoden, iterative Entwicklungszyklen, Teamarbeit im Projekt.",
]

# Calibrated empirically: in-domain ~0.61-0.82, off-topic (recipes, geography, small talk) ~0.55-0.63.
DOMAIN_RELEVANCE_THRESHOLD = 0.60

_domain_embeddings_cache: Optional[List[List[float]]] = None

def _cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

def _get_domain_embeddings() -> List[List[float]]:
    global _domain_embeddings_cache
    if _domain_embeddings_cache is None:
        _domain_embeddings_cache = [get_embedding(topic) for topic in DOMAIN_TOPICS]
    return _domain_embeddings_cache

def is_in_domain(query: str) -> bool:
    query_embedding = get_embedding(query)
    domain_embeddings = _get_domain_embeddings()
    max_similarity = max(_cosine_similarity(query_embedding, topic_embedding) for topic_embedding in domain_embeddings)
    return max_similarity >= DOMAIN_RELEVANCE_THRESHOLD

def _calculate_weighted_confidence(chunks: List[Chunk]) -> float:

    if not chunks:
        return 0.0
    # Weight: top chunk gets 1.0, second 0.5, etc.
    weights = [1 / (i + 1) for i in range(len(chunks))]
    weighted_scores = [c.confidence_score * w for c, w in zip(chunks, weights)]
    return sum(weighted_scores) / sum(weights)

WEB_SEARCH_REFERENCES = [
    SourceReference(file_name="Tavily Web Search", author="AI Crawler", confidence_score=0.0)
]

class EvaluationResult(NamedTuple):
    context: str
    references: List[SourceReference]
    confidence: float
    used_web_search: bool
    needs_confirmation: bool   # True: nothing in the knowledge base; ask the user before searching the web

def run_evaluation_pipeline(query: str, chunks: List[Chunk], threshold: float = 4.0, history: Optional[List[ChatMessage]] = None, confirm_web_search: bool = False) -> EvaluationResult:

    # 0. Out-of-domain pre-check, combined with the last user turn so follow-ups inherit the topic (a switch can slip through but still gets a judge-checked answer)
    domain_check_text = query
    if history:
        previous_user_messages = [m.content for m in history if m.role == "user"]
        if previous_user_messages:
            domain_check_text = f"{previous_user_messages[-1]} {query}"

    if not is_in_domain(domain_check_text):
        if not confirm_web_search:
            print("[CURATOR] Query is out of domain. Asking user to confirm a web search.")
            return EvaluationResult("", [], 0.0, False, True)

        print("[CURATOR] Query is out of domain, but user confirmed web search.")
        context = fetch_webcrawler_results(query)
        return EvaluationResult(context, WEB_SEARCH_REFERENCES, 0.0, True, False)

    # 1. Filter & Sort
    confident_chunks = [c for c in chunks if c.confidence_score >= threshold]
    confident_chunks.sort(key=lambda x: x.confidence_score, reverse=True)

    # 2. Build Context
    context = "\n".join([c.content for c in confident_chunks])

    # 3. Handle References and Confidence
    if confident_chunks:
        references = [
            SourceReference(
                file_name=c.file_name,
                author=c.author,
                confidence_score=c.confidence_score
            )
            for c in confident_chunks
        ]
        agg_conf = _calculate_weighted_confidence(confident_chunks)
        return EvaluationResult(context, references, agg_conf, False, False)

    # 4. No confident chunks: don't hallucinate or silently fall back to Tavily — ask the user first.
    if not confirm_web_search:
        print("[CURATOR] Internal confidence low. Asking user to confirm a web search.")
        return EvaluationResult("", [], 0.0, False, True)

    print("[CURATOR] Internal confidence low, user confirmed web search. Querying Tavily...")
    context = fetch_webcrawler_results(query)
    return EvaluationResult(context, WEB_SEARCH_REFERENCES, 0.0, True, False)