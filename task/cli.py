import argparse
from task import config, ui, pomodoro


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


def config_cmd():
    categories = config.load_categories()

    action = ui.choose(
        ["Add category", "Remove category", "Add subcategory", "Remove subcategory"],
        "Action:",
    )
    if not action:
        return

    if action == "Add category":
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


def main():
    parser = argparse.ArgumentParser(prog="task")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("start")
    subparsers.add_parser("config")

    args = parser.parse_args()

    if args.command == "start":
        start()
    elif args.command == "config":
        config_cmd()
    else:
        parser.print_help()
