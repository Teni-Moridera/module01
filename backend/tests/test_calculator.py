from app.calculator import (
    calculate_group_statistics,
    calculate_pass_rate,
    calculate_rating,
    calculate_student_average,
    calculate_subject_statistics,
)


def sample_students():
    return [
        {
            "id": 1,
            "name": "Ivanov",
            "group": "PR-21",
            "grades": [
                {"subject": "Math", "score": 80},
                {"subject": "CS", "score": 90},
            ],
        },
        {
            "id": 2,
            "name": "Petrov",
            "group": "PR-21",
            "grades": [
                {"subject": "Math", "score": 70},
                {"subject": "CS", "score": 60},
            ],
        },
    ]


def test_calculate_student_average():
    grades = [{"score": 80}, {"score": 90}]
    assert calculate_student_average(grades) == 85


def test_calculate_pass_rate():
    grades = [{"score": 80}, {"score": 40}, {"score": 60}]
    assert calculate_pass_rate(grades) == (2 / 3) * 100


def test_group_statistics():
    stats = calculate_group_statistics(sample_students(), "PR-21")
    assert stats["student_count"] == 2
    assert stats["min_score"] == 60
    assert stats["max_score"] == 90


def test_subject_statistics():
    stats = calculate_subject_statistics(sample_students(), "Math")
    assert stats["average_score"] == 75


def test_rating_order():
    rating = calculate_rating(sample_students())
    assert rating[0]["name"] == "Ivanov"
