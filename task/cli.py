import argparse
import subprocess
from task import config, ui, pomodoro, stats, timew


def start():
    categories = config.load_categories()

    category = ui.choose(list(categories.keys()), "Category:")
    if not category:
        return

    subcats = categories.get(category, [])
    subcategory = None

    if subcats:
        subcategory = ui.choose(subcats, "Subcategory:")

    mode = ui.choose(["Open Timer", "Timer", "Pomodoro"], "Mode:")
    if not mode:
        return

    if mode == "Open Timer":
        pomodoro.run_open(category, subcategory)
    elif mode == "Timer":
        raw = input("Duration (minutes) [25]: ").strip()
        minutes = int(raw) if raw.isdigit() else 25
        pomodoro.run_timer(category, subcategory, minutes)
    else:
        pomodoro.run(category, subcategory)


def _print_category_tree(categories):
    items = list(categories.items())
    for i, (cat, subs) in enumerate(items):
        print(cat)
        for j, sub in enumerate(subs):
            prefix = "└──" if j == len(subs) - 1 else "├──"
            print(f"  {prefix} {sub}")
        if i < len(items) - 1:
            print()


def config_cmd():
    categories = config.load_categories()

    action = ui.choose(
        ["View categories", "Add category", "Remove category", "Add subcategory", "Remove subcategory"],
        "Action:",
    )
    if not action:
        return

    if action == "View categories":
        print()
        _print_category_tree(categories)

    elif action == "Add category":
        name = input("Category name: ").strip()
        if not name:
            return
        if name in categories:
            print(f"Category '{name}' already exists.")
            return
        categories[name] = []
        config.save_categories(categories)
        print(f"Added category '{name}'.")

    elif action == "Remove category":
        cat = ui.choose(list(categories.keys()), "Remove:")
        if not cat:
            return
        del categories[cat]
        config.save_categories(categories)
        print(f"Removed category '{cat}'.")

    elif action == "Add subcategory":
        cat = ui.choose(list(categories.keys()), "Category:")
        if not cat:
            return
        name = input("Subcategory name: ").strip()
        if not name:
            return
        if name in categories[cat]:
            print(f"Subcategory '{name}' already exists in '{cat}'.")
            return
        categories[cat].append(name)
        config.save_categories(categories)
        print(f"Added '{name}' to '{cat}'.")

    elif action == "Remove subcategory":
        cat = ui.choose(list(categories.keys()), "Category:")
        if not cat or not categories[cat]:
            return
        sub = ui.choose(categories[cat], "Remove:")
        if not sub:
            return
        categories[cat].remove(sub)
        config.save_categories(categories)
        print(f"Removed '{sub}' from '{cat}'.")


def stop():
    result = subprocess.run(
        ["timew", "export", "@1"],
        capture_output=True, text=True
    )
    if result.stdout.strip():
        import json
        entries = json.loads(result.stdout)
        if entries and "end" not in entries[-1]:
            print(stats.fmt_entry(entries[-1]))
    timew.stop()


def edit_cmd():
    entries = stats.recent_entries()
    if not entries:
        print("No sessions found.")
        return

    labels = [stats.fmt_entry(e) for e in entries]
    choice = ui.choose(labels, "Session:")
    if not choice:
        return

    entry = entries[labels.index(choice)]
    interval_id = f"@{entry['id']}"

    action = ui.choose(["Fix end time", "Fix start time", "Delete"], "Action:")
    if not action:
        return

    if action == "Delete":
        confirm = input(f"Delete {interval_id}? (y/n): ").strip().lower()
        if confirm == "y":
            subprocess.run(["timew", "delete", interval_id])

    elif action == "Fix end time":
        new_time = input("New end time (e.g. 16:57 or 2026-05-17T16:57): ").strip()
        if new_time:
            subprocess.run(["timew", "modify", "end", interval_id, new_time])

    elif action == "Fix start time":
        new_time = input("New start time (e.g. 09:00 or 2026-05-17T09:00): ").strip()
        if new_time:
            subprocess.run(["timew", "modify", "start", interval_id, new_time])


def shortcuts_cmd():
    print("""
Commands
────────────────────────────────
  task start       Start a new session
  task stop        Stop any running session
  task stats       Show today and weekly totals
  task config      Add or remove categories
  task edit        Fix or delete a recent session
  task shortcuts   Show this help

Selection menus (fzf)
────────────────────────────────
  j / k            Move down / up
  Enter            Confirm selection
  Ctrl-C           Cancel

During a timer
────────────────────────────────
  p                Pause / resume
  Enter            Stop (open timer only)
  Ctrl-C           Quit
""")


def main():
    parser = argparse.ArgumentParser(prog="task")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("start")
    subparsers.add_parser("stop")
    subparsers.add_parser("config")
    subparsers.add_parser("stats")
    subparsers.add_parser("edit")
    subparsers.add_parser("shortcuts")

    args = parser.parse_args()

    if args.command == "start":
        start()
    elif args.command == "stop":
        stop()
    elif args.command == "config":
        config_cmd()
    elif args.command == "stats":
        stats.show()
    elif args.command == "edit":
        edit_cmd()
    elif args.command == "shortcuts":
        shortcuts_cmd()
    else:
        parser.print_help()
