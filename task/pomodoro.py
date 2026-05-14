# task/pomodoro.py
from task import config, timew, notify, ui

def run(category, subcategory):
    cycle = 1

    while True:
        print(f"\n--- Pomodoro {cycle} ---")

        timew.start(category, subcategory)
        notify.send("Pomodoro started")

        ui.countdown(config.POMODORO_MIN, f"{category}>{subcategory}")

        timew.stop()
        notify.send("Pomodoro complete!")

        # Break logic
        if cycle % config.CYCLES_BEFORE_LONG == 0:
            print("\nLong break...")
            notify.send("Long break")
            ui.countdown(config.LONG_BREAK_MIN, "Break")
        else:
            print("\nShort break...")
            notify.send("Short break")
            ui.countdown(config.SHORT_BREAK_MIN, "Break")

        notify.send("Break over")

        cont = input("\nContinue? (y/n): ").lower()
        if cont != "y":
            break

        cycle += 1

def run_open(category, subcategory):
    print(f"\n--- Open Timer: {category}>{subcategory} ---")
    timew.start(category, subcategory)
    notify.send("Timer started")

    ui.elapsed_timer(f"{category}>{subcategory}")

    timew.stop()
    notify.send("Timer stopped")