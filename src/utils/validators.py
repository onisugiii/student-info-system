"""Input validation helpers for student data."""
import re


class ValidationError(ValueError):
    """Raised when user-supplied data is invalid."""


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ID_PATTERN = re.compile(r"^[A-Za-z0-9-]{3,20}$")


def validate_student_id(student_id: str) -> str:
    student_id = str(student_id).strip()
    if not ID_PATTERN.match(student_id):
        raise ValidationError("Student ID must be 3-20 characters (letters, numbers, hyphens).")
    return student_id


def validate_name(name: str) -> str:
    name = str(name).strip()
    if len(name) < 2:
        raise ValidationError("Name must be at least 2 characters.")
    return name


def validate_age(age) -> int:
    try:
        age = int(age)
    except (TypeError, ValueError):
        raise ValidationError("Age must be a whole number.")
    if not 15 <= age <= 100:
        raise ValidationError("Age must be between 15 and 100.")
    return age


def validate_email(email: str) -> str:
    email = str(email).strip()
    if not EMAIL_PATTERN.match(email):
        raise ValidationError("Invalid email format.")
    return email


def validate_course(course: str) -> str:
    course = str(course).strip()
    if not course:
        raise ValidationError("Course cannot be empty.")
    return course


def validate_year_level(year_level) -> int:
    try:
        year_level = int(year_level)
    except (TypeError, ValueError):
        raise ValidationError("Year level must be a whole number.")
    if not 1 <= year_level <= 6:
        raise ValidationError("Year level must be between 1 and 6.")
    return year_level
