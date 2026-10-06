"""Business logic and JSON persistence for students."""
import csv
import json
import logging
import os
import shutil
from pathlib import Path
from typing import List

from src.models.student import Student

logger = logging.getLogger(__name__)

UPDATABLE_FIELDS = {"name", "age", "email", "course", "year_level"}


class StudentNotFoundError(Exception):
    """Raised when a student ID does not exist."""


class DuplicateStudentError(Exception):
    """Raised when adding a student whose ID already exists."""


class StorageError(Exception):
    """Raised when the data file cannot be read or written."""


class StudentService:
    def __init__(self, data_file: str):
        self.data_file = Path(data_file)
        self.backup_file = Path(str(data_file) + ".bak")
        self._students = {}
        self._load()

    # ---------- persistence ----------
    def _read_file(self, path: Path) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return {d["student_id"]: Student.from_dict(d) for d in json.load(f)}

    def _load(self) -> None:
        """Load students; recover from the backup if the main file is corrupted."""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_file.exists():
            self._students = {}
            self._save()
            logger.info("Created new data file: %s", self.data_file)
            return
        try:
            self._students = self._read_file(self.data_file)
            logger.info("Loaded %d students", len(self._students))
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            logger.error("Data file corrupted (%s). Trying backup.", exc)
            if self.backup_file.exists():
                try:
                    self._students = self._read_file(self.backup_file)
                    self._save()
                    logger.warning("Recovered %d students from backup", len(self._students))
                    return
                except Exception as exc2:
                    logger.error("Backup also unreadable: %s", exc2)
            raise StorageError("Data file is corrupted and could not be recovered.") from exc
        except OSError as exc:
            raise StorageError(f"Cannot read data file: {exc}") from exc

    def _save(self) -> None:
        """Write atomically (temp file + replace) and keep a backup copy."""
        tmp = Path(str(self.data_file) + ".tmp")
        try:
            if self.data_file.exists():
                shutil.copy2(self.data_file, self.backup_file)
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump([s.to_dict() for s in self._students.values()], f, indent=2)
            os.replace(tmp, self.data_file)
        except OSError as exc:
            logger.error("Failed to save data: %s", exc)
            raise StorageError(f"Cannot save data: {exc}") from exc

    # ---------- CRUD ----------
    def add_student(self, student: Student) -> Student:
        if student.student_id in self._students:
            raise DuplicateStudentError(f"Student ID {student.student_id} already exists.")
        self._students[student.student_id] = student
        self._save()
        logger.info("Added student %s", student.student_id)
        return student

    def get_student(self, student_id: str) -> Student:
        try:
            return self._students[student_id.strip()]
        except KeyError:
            raise StudentNotFoundError(f"No student with ID {student_id}.") from None

    def list_students(self) -> List[Student]:
        return sorted(self._students.values(), key=lambda s: s.student_id)

    def update_student(self, student_id: str, **fields) -> Student:
        current = self.get_student(student_id)
        invalid = set(fields) - UPDATABLE_FIELDS
        if invalid:
            raise ValueError(f"Cannot update fields: {', '.join(sorted(invalid))}")
        data = current.to_dict()
        data.update({k: val for k, val in fields.items() if val not in (None, "")})
        updated = Student.from_dict(data)  # re-validates
        self._students[current.student_id] = updated
        self._save()
        logger.info("Updated student %s", student_id)
        return updated

    def delete_student(self, student_id: str) -> None:
        student = self.get_student(student_id)
        del self._students[student.student_id]
        self._save()
        logger.info("Deleted student %s", student_id)

    # ---------- bonus ----------
    def search(self, keyword: str) -> List[Student]:
        kw = keyword.strip().lower()
        return [s for s in self.list_students()
                if kw in s.student_id.lower() or kw in s.name.lower()
                or kw in s.course.lower() or kw in s.email.lower()]

    def export_csv(self, export_dir: str) -> str:
        Path(export_dir).mkdir(parents=True, exist_ok=True)
        path = Path(export_dir) / "students_export.csv"
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f, fieldnames=["student_id", "name", "age", "email", "course", "year_level"])
                writer.writeheader()
                writer.writerows(s.to_dict() for s in self.list_students())
        except OSError as exc:
            raise StorageError(f"Cannot export: {exc}") from exc
        logger.info("Exported %d students to %s", len(self._students), path)
        return str(path)
