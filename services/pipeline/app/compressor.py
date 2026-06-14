from app.models import call_model

# Only compress genuinely large contexts; typical KB chunks (~700 chars) and Tavily
# fallback content (~1.5-2k chars for 3 sources) fit the generator's context window as-is.
COMPRESSION_THRESHOLD = 3000  # chars

def compress_context(context: str, mode: str) -> str:

    if len(context) <= COMPRESSION_THRESHOLD:
        return context

    return _summarize(context, mode)

def _summarize(context: str, mode: str) -> str:

    prompt = (
        "Extract only the key data, facts, and step-by-step instructions from the following "
        "text, using only information explicitly stated in it. Discard filler text, "
        "advertisements, links, and unrelated commentary. Do not add any facts, examples, or "
        f"details that are not present in the text.\nContext: {context}"
    )

    return call_model(
        task="summarizer",
        prompt=prompt,
        max_tokens=300,
        stream=False,
        mode=mode
    )
