import logging
import json
import time
from fastapi import FastAPI
from typing import List, Optional
from pydantic import TypeAdapter

from shared.schemas import ChatRequest, ChatResponse, ChatMessage, Settings, Chunk

from app.evaluator import run_evaluation_pipeline
from app.compressor import compress_context
from app.prompt_builder import build_prompt
from app.generator import get_llm_response
from app.judge import judge_query, judge_response

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# Mocked retrieval results; real retrieval is not yet wired in
def get_mock_chunks() -> List[Chunk]:

    return [
        Chunk(
            file_name="machine_learning_basics.pdf",
            author="Max Mustermann",
            confidence_score=4.8,
            content="Machine Learning bezeichnet Verfahren, bei denen Computer aus Daten lernen, ohne explizit programmiert zu werden."
        ),
        Chunk(
            file_name="rag_architecture_notes.docx",
            author="Laura Schmidt",
            confidence_score=4.3,
            content="Retrieval-Augmented Generation kombiniert klassische Informationssuche mit Large Language Models."
        ),
        Chunk(
            file_name="database_systems_summary.txt",
            author="Jonas Weber",
            confidence_score=3.9,
            content="Relationale Datenbanken speichern Daten tabellarisch und verwenden SQL für Abfragen. NoSQL-Datenbanken bieten dagegen flexible Datenstrukturen."
        ),
        Chunk(
            file_name="network_security_script.pdf",
            author="Anna Keller",
            confidence_score=4.6,
            content="Firewalls überwachen den Netzwerkverkehr und blockieren unerlaubte Zugriffe. Verschlüsselungsverfahren schützen Daten vor Manipulation und unbefugtem Zugriff."
        ),
        Chunk(
            file_name="software_engineering_notes.md",
            author="David Fischer",
            confidence_score=2.7,
            content="Agile Softwareentwicklung basiert auf iterativen Entwicklungszyklen, regelmäßigem Feedback und enger Zusammenarbeit im Team."
        )
    ]

@app.post("/augment", response_model=ChatResponse)
async def augment(request: ChatRequest):
    return run_pipeline(request.query, request.settings, request.history, request.confirm_web_search)

def run_pipeline(query, settings: Settings, history: Optional[List[ChatMessage]] = None, confirm_web_search: bool = False) -> ChatResponse:

    pipeline_start = time.time()

    # 0. Pre-generation safety check: block illegal/jailbreak prompts before retrieval/generation
    step_start = time.time()
    is_safe_query, _ = judge_query(query)
    logger.info(f"[TIMER] judge_query (judge.py): {time.time() - step_start:.3f}s")

    if not is_safe_query:
        logger.info(f"[TIMER] TOTAL pipeline (main.py): {time.time() - pipeline_start:.3f}s (unsafe query)")
        return ChatResponse(
            answer="Diese Anfrage kann ich nicht bearbeiten.",
            tokens_used=0,
            source_documents=[],
            aggregated_confidence=0.0
        )

    try:
        # 1. Retrieve the mock data
        step_start = time.time()
        all_chunks = get_mock_chunks()
        logger.info(f"[TIMER] get_mock_chunks (main.py): {time.time() - step_start:.3f}s")

        # 2. Evaluator
        step_start = time.time()
        evaluation = run_evaluation_pipeline(query, chunks=all_chunks, threshold=settings.threshold, history=history, confirm_web_search=confirm_web_search)
        logger.info(f"[TIMER] run_evaluation_pipeline (evaluator.py): {time.time() - step_start:.3f}s")

        # Nothing in the knowledge base: don't hallucinate, ask the user whether to search the web
        if evaluation.needs_confirmation:
            logger.info(f"[TIMER] TOTAL pipeline (main.py): {time.time() - pipeline_start:.3f}s (needs confirmation)")
            return ChatResponse(
                answer="Dazu finde ich nichts in meiner Wissensbasis. Soll ich im Web danach suchen?",
                tokens_used=0,
                source_documents=[],
                aggregated_confidence=0.0,
                needs_confirmation=True
            )

        # 3. Compressor
        step_start = time.time()
        compressed_context = compress_context(evaluation.context, mode=settings.mode)
        logger.info(f"[TIMER] compress_context (compressor.py): {time.time() - step_start:.3f}s")

        # 4. Prompt Builder: COT or Fast
        step_start = time.time()
        final_prompt = build_prompt(query, compressed_context, settings.role, mode=settings.mode, grounded=evaluation.used_web_search, history=history)
        logger.info(f"[TIMER] build_prompt (prompt_builder.py): {time.time() - step_start:.3f}s")

        # 5. Generation
        step_start = time.time()
        answer_text = get_llm_response(prompt=final_prompt, provider=settings.provider, max_tokens=settings.max_tokens, mode=settings.mode, stream=False)
        logger.info(f"[TIMER] get_llm_response (generator.py): {time.time() - step_start:.3f}s")

        # 6. Judge and Return
        step_start = time.time()
        is_safe, feedback = judge_response(query, answer_text)
        logger.info(f"[TIMER] judge_response (judge.py): {time.time() - step_start:.3f}s")

        final_answer = answer_text if is_safe else f"Diese Antwort wurde zurückgehalten: {feedback}"
        final_tokens = len(answer_text.split()) if is_safe else 0
        final_refs = evaluation.references if is_safe else []
        final_conf = evaluation.confidence if is_safe else 0.0

        logger.info(f"[TIMER] TOTAL pipeline (main.py): {time.time() - pipeline_start:.3f}s")

        return ChatResponse(
            answer=final_answer,
            tokens_used=final_tokens,
            source_documents=final_refs,
            aggregated_confidence=final_conf,
            used_web_search=evaluation.used_web_search if is_safe else False
        )

    except Exception:
        # Don't leak internal error details (e.g. Ollama/API URLs) to the user
        logger.exception("Pipeline failed")
        return ChatResponse(
            answer="Bei der Verarbeitung deiner Anfrage ist ein Fehler aufgetreten. Bitte versuche es erneut.",
            tokens_used=0,
            source_documents=[],
            aggregated_confidence=0.0
        )

if __name__ == "__main__":

    test_query = "Was ist RAG?"
    test_settings = Settings(max_tokens=300, role="technical", provider="api", mode="complex")

    logger.info(f"[INPUT] query={test_query!r} settings={test_settings!r}")

    result = run_pipeline(test_query, test_settings)

    adapter = TypeAdapter(ChatResponse)
    result_dict = adapter.dump_python(result, mode='json')

    logger.info("Pipeline Execution Successful:")
    print(json.dumps(result_dict, indent=4, ensure_ascii=False))
