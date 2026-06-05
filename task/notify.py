# task/notify.py
import subprocess
import platform
from task import config

def send(msg):
    system = platform.system()

    if system == "Darwin":  # macOS
        subprocess.run(["osascript", "-e", f'display notification "{msg}"'])
    elif system == "Linux":
        subprocess.run(["notify-send", msg])
    else:
        print(f"[NOTIFY] {msg}")


def chime():
    if not config.load_settings().get("chime", True):
        return

    system = platform.system()

    if system == "Darwin":
        subprocess.Popen(
            ["afplay", "/System/Library/Sounds/Glass.aiff"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    elif system == "Linux":
        subprocess.Popen(
            ["paplay", "/usr/share/sounds/freedesktop/stereo/complete.oga"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    else:
        print("\a", end="", flush=True)