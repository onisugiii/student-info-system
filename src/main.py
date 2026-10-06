"""Student Information System - command-line interface.

Run from the project root:  python -m src.main
"""
import logging

from src.models.student import Student
from src.services.student_service import (
    DuplicateStudentError, StorageError, StudentNotFoundError, StudentService)
from src.utils.config_loader import load_config
from src.utils.logger import setup_logging
from src.utils.validators import ValidationError

logger = logging.getLogger(__name__)

MENU = """
========== STUDENT INFORMATION SYSTEM ==========
1. Add student
2. View all students
3. View one student
4. Update student
5. Delete student
6. Search students
7. Export to CSV
0. Exit
================================================"""


def print_students(students) -> None:
    if not students:
        print("No records found.")
        return
    print(f"{'ID':<12} {'Name':<25} {'Age':<4} {'Course':<10} Year  Email")
    print("-" * 80)
    for s in students:
        print(s)


def add_student(service: StudentService) -> None:
    student = Student(
        student_id=input("Student ID: "),
        name=input("Name: "),
        age=input("Age: "),
        email=input("Email: "),
        course=input("Course: "),
        year_level=input("Year level (1-6): "),
    )
    service.add_student(student)
    print("Student added.")


def update_student(service: StudentService) -> None:
    student_id = input("Student ID to update: ")
    current = service.get_student(student_id)
    print(f"Current: {current}\n(Press Enter to keep a value)")
    updated = service.update_student(
        student_id,
        name=input("New name: "),
        age=input("New age: "),
        email=input("New email: "),
        course=input("New course: "),
        year_level=input("New year level: "),
    )
    print(f"Updated: {updated}")


def delete_student(service: StudentService) -> None:
    student_id = input("Student ID to delete: ")
    student = service.get_student(student_id)
    if input(f"Delete {student.name}? (y/n): ").strip().lower() == "y":
        service.delete_student(student_id)
        print("Student deleted.")
    else:
        print("Cancelled.")


def main() -> None:
    config = load_config()
    setup_logging(config["log_file"], config["log_level"])
    logger.info("Starting %s v%s", config["app_name"], config["version"])

    try:
        service = StudentService(config["data_file"])
    except StorageError as exc:
        print(f"Fatal storage error: {exc}")
        logger.critical("Startup failed: %s", exc)
        return

    actions = {
        "1": lambda: add_student(service),
        "2": lambda: print_students(service.list_students()),
        "3": lambda: print(service.get_student(input("Student ID: "))),
        "4": lambda: update_student(service),
        "5": lambda: delete_student(service),
        "6": lambda: print_students(service.search(input("Search keyword: "))),
        "7": lambda: print(f"Exported to {service.export_csv(config['export_dir'])}"),
    }

    while True:
        print(MENU)
        try:
            choice = input("Choose an option: ").strip()
            if choice == "0":
                logger.info("Application exited by user")
                print("Goodbye!")
                break
            action = actions.get(choice)
            if action is None:
                print("Invalid option. Try again.")
                continue
            action()
        except (ValidationError, DuplicateStudentError, StudentNotFoundError, ValueError) as exc:
            print(f"Error: {exc}")
            logger.warning("User error: %s", exc)
        except StorageError as exc:
            print(f"Storage error: {exc}")
            logger.error("Storage error: %s", exc)
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
        except Exception:
            logger.exception("Unexpected error")
            print("An unexpected error occurred. See logs/app.log for details.")


if __name__ == "__main__":
    main()
