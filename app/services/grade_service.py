def calculate_grade(mark_value: float, maximum_marks: float = 100.0) -> tuple[str, float]:
    if maximum_marks <= 0:
        maximum_marks = 100.0
    percent = (float(mark_value) / float(maximum_marks)) * 100
    if percent >= 90:
        return "A+", 4.0
    if percent >= 80:
        return "A", 3.7
    if percent >= 70:
        return "B+", 3.3
    if percent >= 60:
        return "B", 3.0
    if percent >= 50:
        return "C", 2.0
    if percent >= 40:
        return "D", 1.0
    return "F", 0.0


def calculate_sgpa(grade_points_by_subject: dict) -> float:
    total_credits = 0.0
    weighted_total = 0.0
    for subject, item in grade_points_by_subject.items():
        credits = float(item.get("credits", 0))
        grade_point = float(item.get("grade_point", 0))
        total_credits += credits
        weighted_total += credits * grade_point
    if total_credits == 0:
        return 0.0
    return round(weighted_total / total_credits, 2)
