from __future__ import annotations


class ValidationError(Exception):
    """Raised when input data has invalid format or values."""


class MissingDataError(Exception):
    """Raised when required data is missing."""


class DivisionByZeroError(Exception):
    """Raised when a calculation would divide by zero."""


def ensure_students_present(students) -> None:
    if not students:
        raise MissingDataError("Students list is empty.")


def ensure_grades_present(grades) -> None:
    if not grades:
        raise DivisionByZeroError("Grades list is empty.")


def ensure_group_exists(students, group: str) -> None:
    if not any(getattr(student, "group", None) == group for student in students):
        raise MissingDataError(f"Group '{group}' not found.")


def ensure_subject_exists(students, subject: str) -> None:
    for student in students:
        grades = getattr(student, "grades", None) or []
        if any(getattr(grade, "subject", None) == subject for grade in grades):
            return
    raise MissingDataError(f"Subject '{subject}' not found.")
