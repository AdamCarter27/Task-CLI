# task/ui.py
import subprocess
import sys
import time

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

        sys.stdout.write
        (
            f"\r{label} [{bar}] {mins:02d}:{secs:02d}"
        )
        sys.stdout.flush()
        time.sleep(1)

    sys.stdout.write("\n")