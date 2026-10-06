"""Unit tests for StudentService. Run with: pytest"""
import pytest

from src.models.student import Student
from src.services.student_service import (
    DuplicateStudentError, StudentNotFoundError, StudentService)
from src.utils.validators import ValidationError


@pytest.fixture
def service(tmp_path):
    return StudentService(str(tmp_path / "students.json"))


def make_student(student_id="2024-001", **overrides):
    data = dict(student_id=student_id, name="Juan Dela Cruz", age=20,
                email="juan@example.com", course="BSIT", year_level=3)
    data.update(overrides)
    return Student(**data)


def test_add_and_get(service):
    service.add_student(make_student())
    assert service.get_student("2024-001").name == "Juan Dela Cruz"


def test_duplicate_id_rejected(service):
    service.add_student(make_student())
    with pytest.raises(DuplicateStudentError):
        service.add_student(make_student())


def test_update(service):
    service.add_student(make_student())
    updated = service.update_student("2024-001", name="Maria Santos", age="21")
    assert updated.name == "Maria Santos" and updated.age == 21


def test_delete(service):
    service.add_student(make_student())
    service.delete_student("2024-001")
    with pytest.raises(StudentNotFoundError):
        service.get_student("2024-001")


def test_persistence(tmp_path):
    path = str(tmp_path / "students.json")
    StudentService(path).add_student(make_student())
    assert len(StudentService(path).list_students()) == 1


def test_search(service):
    service.add_student(make_student())
    service.add_student(make_student("2024-002", name="Ana Reyes", email="ana@example.com"))
    assert len(service.search("ana")) == 1


def test_export_csv(service, tmp_path):
    service.add_student(make_student())
    path = service.export_csv(str(tmp_path / "exports"))
    assert "2024-001" in open(path, encoding="utf-8").read()


def test_invalid_email():
    with pytest.raises(ValidationError):
        make_student(email="not-an-email")


def test_invalid_age():
    with pytest.raises(ValidationError):
        make_student(age=5)


def test_corrupted_file_recovers_from_backup(tmp_path):
    path = tmp_path / "students.json"
    svc = StudentService(str(path))
    svc.add_student(make_student())
    svc.add_student(make_student("2024-002", name="Ana Reyes"))  # creates .bak
    path.write_text("{ broken json")
    assert len(StudentService(str(path)).list_students()) >= 1
