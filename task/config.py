import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "task-cli"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CATEGORIES = {
    "Math": ["Homework", "Review", "Other"],
    "Programming": ["LeetCode", "Personal Project", "Work Project", "Other"],
    "Wasted": ["Browsing", "Video Games", "Other"],
}

DEFAULT_SETTINGS = {
    "chime": True,
}

POMODORO_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15
CYCLES_BEFORE_LONG = 3


def _load_data():
    if not CONFIG_FILE.exists():
        data = {"categories": DEFAULT_CATEGORIES, "settings": DEFAULT_SETTINGS}
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text(json.dumps(data, indent=2))
        return data
    return json.loads(CONFIG_FILE.read_text())


def _save_data(data):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(data, indent=2))


def load_categories():
    return _load_data().get("categories", DEFAULT_CATEGORIES)


def save_categories(categories):
    data = _load_data()
    data["categories"] = categories
    _save_data(data)


def load_settings():
    return {**DEFAULT_SETTINGS, **_load_data().get("settings", {})}


def save_settings(settings):
    data = _load_data()
    data["settings"] = settings
    _save_data(data)
