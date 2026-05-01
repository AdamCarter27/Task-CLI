# task/notify.py
import subprocess
import platform

def send(msg):
    system = platform.system()

    if system == "Darwin":  # macOS
        subprocess.run(["osascript", "-e", f'display notification "{msg}"'])
    elif system == "Linux":
        subprocess.run(["notify-send", msg])
    else:
        print(f"[NOTIFY] {msg}")