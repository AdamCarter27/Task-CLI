import argparse
from task import config, ui, pomodoro

def start():
    category = ui.choose(list(config.CATEGORIES.keys()), "Category:")
    if not category:
        return

    subcats = config.CATEGORIES.get(category, [])
    subcategory = None

    if subcats:
        subcategory = ui.choose(subcats, "Subcategory:")

    pomodoro.run(category, subcategory)


def main():
    parser = argparse.ArgumentParser(prog="task")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("start")

    args = parser.parse_args()

    if args.command == "start":
        start()
    else:
        parser.print_help()