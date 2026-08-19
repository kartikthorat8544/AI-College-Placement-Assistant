import pytest

from rag.document_processor import create_text_chunks
from rag.retriever import retrieve_relevant_chunks


def test_short_text_creates_one_chunk():
    text = "Python is a popular programming language."

    chunks = create_text_chunks(
        text,
        chunk_size=20,
        overlap=5
    )

    assert len(chunks) == 1
    assert chunks[0] == text


def test_long_text_creates_multiple_chunks():
    text = " ".join(
        f"word{number}"
        for number in range(250)
    )

    chunks = create_text_chunks(
        text,
        chunk_size=100,
        overlap=20
    )

    assert len(chunks) == 3


def test_chunks_have_correct_overlap():
    text = " ".join(
        f"word{number}"
        for number in range(150)
    )

    chunks = create_text_chunks(
        text,
        chunk_size=100,
        overlap=20
    )

    first_chunk_words = chunks[0].split()
    second_chunk_words = chunks[1].split()

    assert first_chunk_words[-20:] == second_chunk_words[:20]


def test_invalid_chunk_size():
    with pytest.raises(ValueError):
        create_text_chunks(
            "Some example text",
            chunk_size=0,
            overlap=0
        )


def test_overlap_cannot_equal_chunk_size():
    with pytest.raises(ValueError):
        create_text_chunks(
            "Some example text",
            chunk_size=10,
            overlap=10
        )


def test_retriever_finds_relevant_chunk():
    chunks = [
        "Python lists are mutable collections.",
        "SQL is used to query relational databases.",
        "A resume should include projects and skills."
    ]

    results = retrieve_relevant_chunks(
        "How are SQL databases queried?",
        chunks,
        top_k=2
    )

    assert len(results) >= 1
    assert results[0]["chunk_index"] == 1
    assert results[0]["score"] > 0


def test_retriever_rejects_empty_question():
    chunks = [
        "Python is a programming language."
    ]

    with pytest.raises(ValueError):
        retrieve_relevant_chunks("", chunks)


def test_retriever_rejects_empty_chunks():
    with pytest.raises(ValueError):
        retrieve_relevant_chunks(
            "What is Python?",
            []
        )