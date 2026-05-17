import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "task-cli"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CATEGORIES = {
    "Math": ["Homework", "Review", "Other"],
    "Programming": ["LeetCode", "Personal Project", "Work Project", "Other"],
    "Wasted": ["Browsing", "Video Games", "Other"],
}

POMODORO_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15
CYCLES_BEFORE_LONG = 3


def load_categories():
    if not CONFIG_FILE.exists():
        save_categories(DEFAULT_CATEGORIES)
        return DEFAULT_CATEGORIES
    data = json.loads(CONFIG_FILE.read_text())
    return data.get("categories", DEFAULT_CATEGORIES)


def save_categories(categories):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps({"categories": categories}, indent=2))
