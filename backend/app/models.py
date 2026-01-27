from __future__ import annotations

from datetime import date
from typing import List

from pydantic import BaseModel, Field, conint, constr


class Grade(BaseModel):
    subject: constr(strip_whitespace=True, min_length=1)
    score: conint(ge=0, le=100)
    date: date


class Student(BaseModel):
    id: conint(ge=1)
    name: constr(strip_whitespace=True, min_length=1)
    group: constr(strip_whitespace=True, min_length=1)
    grades: List[Grade] = Field(default_factory=list)


class StudentsPayload(BaseModel):
    students: List[Student] = Field(default_factory=list)
