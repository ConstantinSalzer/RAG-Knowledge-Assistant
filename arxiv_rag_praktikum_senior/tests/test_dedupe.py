from app.dedupe import normalize_text, paper_fingerprint


def test_normalize_text_removes_punctuation_and_extra_spaces():
    assert normalize_text("A  Test-Paper!") == "a test paper"


def test_fingerprint_is_stable_for_small_formatting_changes():
    first = paper_fingerprint("A Test Paper", "This is an abstract.")
    second = paper_fingerprint("A test paper!", "This is an abstract.")

    assert first == second
