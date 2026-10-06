"""Configuration management: loads config.json with defaults and env overrides."""
import json
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT_DIR / "config" / "config.json"

DEFAULTS = {
    "app_name": "Student Information System",
    "version": "1.0.0",
    "data_file": "data/students.json",
    "log_file": "logs/app.log",
    "log_level": "INFO",
    "export_dir": "data/exports",
}


def load_config(path: Path = CONFIG_PATH) -> dict:
    """Load configuration, falling back to defaults if the file is missing/invalid.

    Environment variables SIS_DATA_FILE and SIS_LOG_LEVEL override the file,
    which makes the app easy to configure in cloud/container deployments.
    """
    config = dict(DEFAULTS)
    try:
        with open(path, "r", encoding="utf-8") as f:
            config.update(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"[WARN] Could not read config ({exc}). Using defaults.")

    config["data_file"] = os.getenv("SIS_DATA_FILE", config["data_file"])
    config["log_level"] = os.getenv("SIS_LOG_LEVEL", config["log_level"])

    # Resolve relative paths against the project root
    for key in ("data_file", "log_file", "export_dir"):
        p = Path(config[key])
        config[key] = str(p if p.is_absolute() else ROOT_DIR / p)
    return config
