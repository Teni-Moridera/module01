from __future__ import annotations

from datetime import date
import csv
import io
from typing import Dict, List

from fastapi import FastAPI, File, HTTPException, UploadFile

from .calculator import (
    calculate_group_statistics,
    calculate_pass_rate,
    calculate_rating,
    calculate_student_average,
    calculate_subject_statistics,
)
from .exporters import export_report
from .models import Grade, Student, StudentsPayload
from .validators import (
    DivisionByZeroError,
    MissingDataError,
    ValidationError,
    ensure_grades_present,
    ensure_group_exists,
    ensure_students_present,
    ensure_subject_exists,
)

app = FastAPI(title="Student Performance Metrics", version="1.0.0")

# In-memory storage for the latest dataset.
DATA_STORE: StudentsPayload | None = None


@app.get("/")
def health_check() -> dict:
    return {"status": "ok"}


def _ensure_data_loaded() -> StudentsPayload:
    if DATA_STORE is None:
        raise HTTPException(status_code=400, detail="No data loaded.")
    return DATA_STORE


def _parse_csv(content: str) -> StudentsPayload:
    reader = csv.DictReader(io.StringIO(content))
    required_fields = {"id", "name", "group", "subject", "score", "date"}
    if not required_fields.issubset(reader.fieldnames or []):
        raise ValidationError("CSV is missing required columns.")

    students: Dict[int, Student] = {}
    for row in reader:
        try:
            student_id = int(row["id"])
            score = float(row["score"])
            grade_date = date.fromisoformat(row["date"])
        except (ValueError, TypeError) as exc:
            raise ValidationError("CSV contains invalid values.") from exc

        if student_id not in students:
            students[student_id] = Student(
                id=student_id,
                name=row["name"].strip(),
                group=row["group"].strip(),
                grades=[],
            )

        students[student_id].grades.append(
            Grade(subject=row["subject"].strip(), score=score, date=grade_date)
        )

    return StudentsPayload(students=list(students.values()))


@app.post("/api/upload")
async def upload_data(file: UploadFile = File(...)) -> dict:
    try:
        content = (await file.read()).decode("utf-8")
        if file.filename and file.filename.lower().endswith(".csv"):
            payload = _parse_csv(content)
        else:
            payload = StudentsPayload.model_validate_json(content)

        ensure_students_present(payload.students)
    except (ValidationError, MissingDataError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    global DATA_STORE
    DATA_STORE = payload
    return {"status": "loaded", "students": len(payload.students)}


@app.post("/api/upload/json")
def upload_data_json(payload: StudentsPayload) -> dict:
    try:
        ensure_students_present(payload.students)
    except MissingDataError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    global DATA_STORE
    DATA_STORE = payload
    return {"status": "loaded", "students": len(payload.students)}


@app.get("/api/students")
def get_students() -> List[Student]:
    payload = _ensure_data_loaded()
    return payload.students


@app.get("/api/statistics")
def get_statistics() -> dict:
    payload = _ensure_data_loaded()
    students = payload.students
    try:
        ensure_students_present(students)
        all_grades = [grade for student in students for grade in student.grades]
        ensure_grades_present(all_grades)
    except (MissingDataError, DivisionByZeroError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    scores = [grade.score for grade in all_grades]
    return {
        "student_count": len(students),
        "grade_count": len(all_grades),
        "average_score": sum(scores) / len(scores),
        "min_score": min(scores),
        "max_score": max(scores),
        "pass_rate": calculate_pass_rate(all_grades),
        "rating": calculate_rating(students),
    }


@app.get("/api/statistics/student/{student_id}")
def get_student_statistics(student_id: int) -> dict:
    payload = _ensure_data_loaded()
    student = next((s for s in payload.students if s.id == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    try:
        ensure_grades_present(student.grades)
    except DivisionByZeroError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "student_id": student.id,
        "name": student.name,
        "group": student.group,
        "average_score": calculate_student_average(student.grades),
        "pass_rate": calculate_pass_rate(student.grades),
        "grade_count": len(student.grades),
    }


@app.get("/api/statistics/group/{group}")
def get_group_statistics(group: str) -> dict:
    payload = _ensure_data_loaded()
    try:
        ensure_group_exists(payload.students, group)
        return calculate_group_statistics(payload.students, group)
    except (MissingDataError, DivisionByZeroError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/statistics/subject/{subject}")
def get_subject_statistics(subject: str) -> dict:
    payload = _ensure_data_loaded()
    try:
        ensure_subject_exists(payload.students, subject)
        return calculate_subject_statistics(payload.students, subject)
    except (MissingDataError, DivisionByZeroError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/export/{format}")
def export_statistics(format: str) -> dict:
    payload = _ensure_data_loaded()
    try:
        report = get_statistics()
        content, media_type = export_report(report, format=format)
        return {"format": format, "media_type": media_type, "content": content}
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
