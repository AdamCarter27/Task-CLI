# task/ui.py
import subprocess
import sys
import time
import threading

def choose(options, prompt="Select:"):
    try:
        result = subprocess.check_output(
            ["fzf", "--prompt", prompt + " "],
            input="\n".join(options),
            text=True
        ).strip()
        return result
    except subprocess.CalledProcessError:
        return None

def countdown(minutes, label=""):
    total = minutes * 60

    for remaining in range(total, 0, -1):
        mins, secs = divmod(remaining, 60)

        progress = int((total - remaining) / total * 20)
        bar = "█" * progress + "-" * (20 - progress)

        sys.stdout.write(f"\r{label} [{bar}] {mins:02d}:{secs:02d}")
        sys.stdout.flush()
        time.sleep(1)

    sys.stdout.write("\n")

def elapsed_timer(label=""):
    stop_event = threading.Event()

    def display():
        start = time.time()
        while not stop_event.is_set():
            elapsed = int(time.time() - start)
            mins, secs = divmod(elapsed, 60)
            sys.stdout.write(f"\r{label} [running] {mins:02d}:{secs:02d}  (press Enter to stop)")
            sys.stdout.flush()
            time.sleep(1)

    thread = threading.Thread(target=display, daemon=True)
    thread.start()
    input()
    stop_event.set()
    sys.stdout.write("\n")