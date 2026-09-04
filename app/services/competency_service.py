def score_to_level(score: int) -> int:
    if score < 40:
        return 1

    if score < 60:
        return 2

    if score < 75:
        return 3

    if score < 90:
        return 4

    return 5