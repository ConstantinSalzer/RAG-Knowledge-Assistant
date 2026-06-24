from app.scoring import score_paper


def test_score_positive_for_relevant_rag_paper():
    score = score_paper(
        "Hybrid RAG for Scientific Retrieval",
        "This paper combines retrieval augmented generation and embeddings.",
    )

    assert score >= 3.0


def test_score_penalizes_irrelevant_paper():
    score = score_paper(
        "An Editorial Opinion",
        "This is a non technical editorial text.",
    )

    assert score < 0
