from app.schemas.mcq import MCQResponse


VALID_ANSWERS = {
    "A",
    "B",
    "C",
    "D"
}

VALID_DIFFICULTIES = {
    "easy",
    "medium",
    "hard"
}


def validate_mcqs(mcq_response: MCQResponse):
    if not mcq_response.questions:
        raise ValueError("No MCQs were generated")

    for mcq in mcq_response.questions:

        # Check correct answer
        if mcq.correct_answer not in VALID_ANSWERS:
            raise ValueError(
                f"Invalid correct answer: {mcq.correct_answer}"
            )

        # Check difficulty
        if mcq.difficulty not in VALID_DIFFICULTIES:
            raise ValueError(
                f"Invalid difficulty: {mcq.difficulty}"
            )

        # Check that all fields contain something
        options = [
            mcq.option_a,
            mcq.option_b,
            mcq.option_c,
            mcq.option_d
        ]

        if not all(options):
            raise ValueError("One or more options are empty")

        if not mcq.question.strip():
            raise ValueError("Question cannot be empty")

    return True