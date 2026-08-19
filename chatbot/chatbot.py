import re

from chatbot.ai_service import generate_ai_response
from chatbot.intents import INTENTS


def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def calculate_pattern_score(message, pattern):
    message_words = set(message.split())
    pattern_words = pattern.split()

    if all(word in message_words for word in pattern_words):
        return len(pattern_words)

    return 0


def find_best_intent(user_message):
    cleaned_message = normalize_text(user_message)

    best_intent = None
    highest_score = 0
    highest_priority = 0

    for intent_name, intent_data in INTENTS.items():
        intent_priority = intent_data.get("priority", 1)

        for pattern in intent_data["patterns"]:
            cleaned_pattern = normalize_text(pattern)

            score = calculate_pattern_score(
                cleaned_message,
                cleaned_pattern
            )

            if (
                score > highest_score
                or (
                    score == highest_score
                    and score > 0
                    and intent_priority > highest_priority
                )
            ):
                highest_score = score
                highest_priority = intent_priority
                best_intent = intent_name

    return best_intent


def get_response(user_message):
    best_intent = find_best_intent(user_message)

    if best_intent:
        return INTENTS[best_intent]["response"]

    return generate_ai_response(user_message)