from dataclasses import dataclass


@dataclass(frozen=True)
class ScoreConfig:
    good_terms: tuple[str, ...] = (
        "retrieval augmented generation",
        "rag",
        "hybrid retrieval",
        "vector database",
        "knowledge graph",
        "graph retrieval",
        "embedding",
        "transformer",
        "semantic search",
        "information retrieval",
    )
    bad_terms: tuple[str, ...] = (
        "editorial",
        "opinion",
        "non technical",
    )


DEFAULT_SCORE_CONFIG = ScoreConfig()


def score_paper(
    title: str,
    abstract: str,
    config: ScoreConfig = DEFAULT_SCORE_CONFIG,
) -> float:
    text = f"{title}\n{abstract}".lower()
    score = sum(1.0 for term in config.good_terms if term in text)
    score -= sum(1.0 for term in config.bad_terms if term in text)

    if "rag" in text and "retrieval" in text:
        score += 1.0

    return score
