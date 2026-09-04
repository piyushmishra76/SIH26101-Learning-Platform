def calculate_recommendation_score(
    gap: int,
    current_level: int,
    target_level: int
) -> float:

    # Bigger competency gap = higher priority
    gap_score = min(gap / 4, 1)

    # How much of the target competency the course can address
    if target_level > current_level:
        level_fit = min(
            (target_level - current_level) / 4,
            1
        )
    else:
        level_fit = 0

    score = (
        0.7 * gap_score +
        0.3 * level_fit
    )

    return round(score * 100, 2)