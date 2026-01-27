from __future__ import annotations

from typing import Iterable, List, Sequence


def _get_value(item, key: str):
    if isinstance(item, dict):
        return item.get(key)
    return getattr(item, key, None)


def _extract_scores(grades: Iterable) -> List[float]:
    scores: List[float] = []
    for grade in grades:
        score = _get_value(grade, "score")
        if score is not None:
            scores.append(float(score))
    return scores


def _safe_average(values: Sequence[float]) -> float:
    if not values:
        raise ZeroDivisionError("Cannot calculate average from empty values.")
    return sum(values) / len(values)


def calculate_student_average(grades: Iterable) -> float:
    """Calculate a student's average score from grade list."""
    scores = _extract_scores(grades)
    return _safe_average(scores)


def calculate_pass_rate(grades: Iterable, threshold: float = 60) -> float:
    """Calculate pass rate percentage for grades using a threshold."""
    scores = _extract_scores(grades)
    if not scores:
        raise ZeroDivisionError("Cannot calculate pass rate from empty grades.")
    passed = sum(1 for score in scores if score >= threshold)
    return (passed / len(scores)) * 100


def calculate_group_statistics(students: Iterable, group: str) -> dict:
    """Calculate statistics for a specific group."""
    group_students = [
        student for student in students if _get_value(student, "group") == group
    ]
    if not group_students:
        raise ZeroDivisionError("No students found for the specified group.")

    all_grades = []
    student_averages = []
    for student in group_students:
        grades = _get_value(student, "grades") or []
        all_grades.extend(grades)
        student_averages.append(calculate_student_average(grades))

    all_scores = _extract_scores(all_grades)
    return {
        "group": group,
        "student_count": len(group_students),
        "average_score": _safe_average(all_scores),
        "min_score": min(all_scores),
        "max_score": max(all_scores),
        "pass_rate": calculate_pass_rate(all_grades),
        "average_student_score": _safe_average(student_averages),
    }


def calculate_subject_statistics(students: Iterable, subject: str) -> dict:
    """Calculate statistics for a specific subject."""
    subject_grades = []
    for student in students:
        grades = _get_value(student, "grades") or []
        subject_grades.extend(
            [grade for grade in grades if _get_value(grade, "subject") == subject]
        )

    scores = _extract_scores(subject_grades)
    if not scores:
        raise ZeroDivisionError("No grades found for the specified subject.")

    return {
        "subject": subject,
        "grade_count": len(scores),
        "average_score": _safe_average(scores),
        "min_score": min(scores),
        "max_score": max(scores),
        "pass_rate": calculate_pass_rate(subject_grades),
    }


def calculate_rating(students: Iterable) -> List[dict]:
    """Build a rating list of students sorted by average score."""
    rating = []
    for student in students:
        grades = _get_value(student, "grades") or []
        average = calculate_student_average(grades)
        rating.append(
            {
                "id": _get_value(student, "id"),
                "name": _get_value(student, "name"),
                "group": _get_value(student, "group"),
                "average_score": average,
            }
        )

    rating.sort(key=lambda item: (-item["average_score"], item["name"]))
    return rating
