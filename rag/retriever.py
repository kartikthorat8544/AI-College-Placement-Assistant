from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def retrieve_relevant_chunks(question, chunks, top_k=3):
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    if not chunks:
        raise ValueError("No document chunks are available.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    documents = chunks + [question]

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english"
    )

    document_vectors = vectorizer.fit_transform(documents)

    chunk_vectors = document_vectors[:-1]
    question_vector = document_vectors[-1]

    similarity_scores = cosine_similarity(
        question_vector,
        chunk_vectors
    ).flatten()

    ranked_indices = similarity_scores.argsort()[::-1]
    selected_indices = ranked_indices[:min(top_k, len(chunks))]

    results = []

    for index in selected_indices:
        score = float(similarity_scores[index])

        if score > 0:
            results.append(
                {
                    "chunk_index": int(index),
                    "score": score,
                    "text": chunks[index]
                }
            )

    return results