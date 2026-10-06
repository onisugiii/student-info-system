"""Student data model."""
from dataclasses import dataclass, asdict

from src.utils import validators as v


@dataclass
class Student:
    student_id: str
    name: str
    age: int
    email: str
    course: str
    year_level: int

    def __post_init__(self):
        """Validate and normalize every field on creation."""
        self.student_id = v.validate_student_id(self.student_id)
        self.name = v.validate_name(self.name)
        self.age = v.validate_age(self.age)
        self.email = v.validate_email(self.email)
        self.course = v.validate_course(self.course)
        self.year_level = v.validate_year_level(self.year_level)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Student":
        return cls(**data)

    def __str__(self) -> str:
        return (f"{self.student_id:<12} {self.name:<25} {self.age:<4} "
                f"{self.course:<10} Y{self.year_level}  {self.email}")
