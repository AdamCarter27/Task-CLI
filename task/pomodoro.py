# task/pomodoro.py
from task import config, timew, notify, ui, spotify


def _spotify_callbacks():
    uri = config.load_settings().get("spotify_playlist", "")
    if not uri:
        return None, None
    return spotify.pause, lambda: spotify.play()


def run(category, subcategory):
    cycle = 1
    on_pause, on_resume = _spotify_callbacks()
    uri = config.load_settings().get("spotify_playlist", "")

    while True:
        print(f"\n--- Pomodoro {cycle} ---")

        timew.start(category, subcategory)
        notify.send("Pomodoro started")
        if uri:
            spotify.play(uri)

        ui.countdown(config.POMODORO_MIN, f"{category}>{subcategory}",
                     on_pause=on_pause, on_resume=on_resume)

        timew.stop()
        notify.chime()
        notify.send("Pomodoro complete!")
        if uri:
            spotify.pause()

        if cycle % config.CYCLES_BEFORE_LONG == 0:
            print("\nLong break...")
            notify.send("Long break")
            ui.countdown(config.LONG_BREAK_MIN, "Break")
        else:
            print("\nShort break...")
            notify.send("Short break")
            ui.countdown(config.SHORT_BREAK_MIN, "Break")

        notify.chime()
        notify.send("Break over")

        cont = input("\nContinue? (y/n): ").lower()
        if cont != "y":
            break

        cycle += 1


def run_timer(category, subcategory, minutes):
    on_pause, on_resume = _spotify_callbacks()
    uri = config.load_settings().get("spotify_playlist", "")

    print(f"\n--- Timer: {category}>{subcategory} ({minutes}m) ---")
    timew.start(category, subcategory)
    notify.send("Timer started")
    if uri:
        spotify.play(uri)

    ui.countdown(minutes, f"{category}>{subcategory}",
                 on_pause=on_pause, on_resume=on_resume)

    timew.stop()
    notify.chime()
    notify.send("Timer complete!")
    if uri:
        spotify.pause()


def run_open(category, subcategory):
    on_pause, on_resume = _spotify_callbacks()
    uri = config.load_settings().get("spotify_playlist", "")

    print(f"\n--- Open Timer: {category}>{subcategory} ---")
    timew.start(category, subcategory)
    notify.send("Timer started")
    if uri:
        spotify.play(uri)

    ui.elapsed_timer(f"{category}>{subcategory}",
                     on_pause=on_pause, on_resume=on_resume)

    timew.stop()
    notify.send("Timer stopped")
    if uri:
        spotify.pause()
