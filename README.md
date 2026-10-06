# Student Information System

A cloud-ready, command-line Student Information System built in Python. It supports full CRUD, JSON persistence, validation, search, CSV export, configuration management, and logging.

## Features
- Add, view, update, and delete student records
- JSON data storage with atomic writes and automatic backup recovery
- Input validation (ID, name, age, email, year level)
- Search by ID, name, course, or email
- Export records to CSV
- External configuration (`config/config.json`) with environment variable overrides
- Rotating file logs in `logs/app.log`
- Unit tests with pytest

## Project Structure
```
student-info-system/
├── src/
│   ├── models/student.py
│   ├── services/student_service.py
│   ├── utils/ (config_loader.py, logger.py, validators.py)
│   └── main.py
├── data/students.json
├── config/config.json
├── logs/
├── tests/test_student_service.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Installation
```bash
git clone https://github.com/<your-username>/student-info-system.git
cd student-info-system
python -m venv venv
venv\Scripts\activate        # Windows  (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
```

## Usage
```bash
python -m src.main
```

## Configuration
Edit `config/config.json`, or override with environment variables:

| Variable | Purpose |
|---|---|
| `SIS_DATA_FILE` | Path to the JSON data file |
| `SIS_LOG_LEVEL` | DEBUG, INFO, WARNING, ERROR |

## Running Tests
```bash
pytest -v
```

## Architecture
- **models**: the `Student` dataclass, which validates itself
- **services**: business logic and storage (`StudentService`)
- **utils**: config, logging, and validators
- **main**: the user interface (menu)

## Git Workflow
Feature branches (`feature/*`) merged into `main` through pull requests.

## Author
Mark Dave Leaño – BSIT 3A URD
