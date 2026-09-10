def remove_duplicate_mcqs(mcqs):

    unique_mcqs = []
    seen_questions = set()

    for mcq in mcqs:

        normalized_question = " ".join(
            mcq.question.lower().split()
        )

        if normalized_question not in seen_questions:
            seen_questions.add(normalized_question)
            unique_mcqs.append(mcq)

    return unique_mcqs