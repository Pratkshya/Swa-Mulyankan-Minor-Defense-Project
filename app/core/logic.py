def calculate_mastery(answers, questions):
    total_weight = 0
    score = 0

    for q in questions:
        wi = q['weight']
        si = 1 if answers.get(str(q['id'])) == q['correct_answer'] else 0

        score += si * wi
        total_weight += wi

    return score / total_weight if total_weight else 0


def calculate_gap(answers, questions):
    level_weight = {"K":1, "U":2, "A":3, "HA":4}
    gap = 0

    for q in questions:
        if answers.get(str(q['id'])) != q['correct_answer']:
            gap += level_weight.get(q['level'], 1)

    return gap


def classify(m):
    if m >= 0.75:
        return "Mastered"
    elif m >= 0.4:
        return "Review Required"
    return "Critical Gap"