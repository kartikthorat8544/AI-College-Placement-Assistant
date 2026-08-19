from chatbot.chatbot import (
    calculate_pattern_score,
    find_best_intent,
    get_response,
    normalize_text
)


def test_normalize_text():
    result = normalize_text("  Hello!!! How ARE you?  ")

    assert result == "hello how are you"


def test_pattern_score_for_matching_words():
    message = "prepare for python interview"
    pattern = "python interview"

    score = calculate_pattern_score(message, pattern)

    assert score == 2


def test_pattern_score_for_non_matching_words():
    message = "help me prepare my resume"
    pattern = "python interview"

    score = calculate_pattern_score(message, pattern)

    assert score == 0


def test_greeting_intent():
    result = find_best_intent("Hello!")

    assert result == "greeting"


def test_resume_intent():
    result = find_best_intent("Please help me improve my CV")

    assert result == "resume"


def test_python_interview_priority():
    result = find_best_intent(
        "How should I prepare for a Python interview?"
    )

    assert result == "python_interview"


def test_aptitude_intent():
    result = find_best_intent(
        "I want logical reasoning preparation"
    )

    assert result == "aptitude"


def test_known_response_without_ai_request():
    response = get_response("Help me improve my resume")

    assert "skills" in response.lower()
    assert "education" in response.lower()