import logging
from typing import Tuple
from app.models import call_model

logger = logging.getLogger(__name__)

# MLCommons hazard taxonomy used by Llama Guard 3
UNSAFE_CATEGORIES = """S1: Violent Crimes.
S2: Non-Violent Crimes.
S3: Sex Crimes.
S4: Child Exploitation.
S5: Defamation.
S6: Specialized Advice.
S7: Privacy.
S8: Intellectual Property.
S9: Indiscriminate Weapons.
S10: Hate.
S11: Self-Harm.
S12: Sexual Content.
S13: Elections.
S14: Code Interpreter Abuse."""

def _classify(conversation: str) -> Tuple[bool, str]:

    # Llama Guard 3 conversation-classification prompt
    prompt = (
        "Task: Check if there is unsafe content in the conversation below "
        "according our safety policy with the below categories.\n\n"
        f"<BEGIN UNSAFE CONTENT CATEGORIES>\n{UNSAFE_CATEGORIES}\n<END UNSAFE CONTENT CATEGORIES>\n\n"
        "<BEGIN CONVERSATION>\n\n"
        f"{conversation}\n"
        "<END CONVERSATION>\n\n"
        "Provide your safety assessment for ONLY THE LAST message in the above conversation:\n"
        " - First line must read 'safe' or 'unsafe'.\n"
        " - If unsafe, a second line must include a comma-separated list of violated categories."
    )

    try:
        decision = call_model(task="judge", prompt=prompt, max_tokens=20, stream=False)

        # First line: 'safe'/'unsafe', second line (if unsafe): violated categories
        lines = decision.strip().splitlines()
        first_line = lines[0].strip().lower() if lines else ""

        if first_line.startswith("safe"):
            return True, "Success"

        if first_line.startswith("unsafe"):
            categories = lines[1].strip() if len(lines) > 1 else "unspecified category"
            return False, f"Unsafe content detected ({categories})"

        return False, f"Safety validation failed (unexpected judge output: {decision!r})"

    except Exception:
        # Don't leak internal error details (e.g. Ollama URLs) to the user
        logger.exception("Judge call failed")
        return False, "Safety check unavailable"

def judge_query(user_query: str) -> Tuple[bool, str]:
    return _classify(f"User: {user_query}")

def judge_response(user_query: str, ai_response: str) -> Tuple[bool, str]:
    return _classify(f"User: {user_query}\n\nAgent: {ai_response}")
