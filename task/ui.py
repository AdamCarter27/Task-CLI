# task/ui.py
import subprocess
import sys
import time
import select
import tty
import termios


def choose(options, prompt="Select:"):
    try:
        result = subprocess.check_output(
            ["fzf", "--prompt", prompt + " ", "--bind", "j:down,k:up"],
            input="\n".join(options),
            text=True
        ).strip()
        return result
    except subprocess.CalledProcessError:
        return None


def _render_countdown(label, remaining, total, paused):
    mins, secs = divmod(remaining, 60)
    progress = int((total - remaining) / total * 20)
    bar = "█" * progress + "-" * (20 - progress)
    status = "[PAUSED - p to resume]" if paused else "[p to pause]         "
    sys.stdout.write(f"\r{label} [{bar}] {mins:02d}:{secs:02d}  {status}")
    sys.stdout.flush()


def _render_elapsed(label, elapsed, paused):
    mins, secs = divmod(elapsed, 60)
    status = "[PAUSED - p to resume]" if paused else "[p to pause | Enter to stop]"
    sys.stdout.write(f"\r{label} [running] {mins:02d}:{secs:02d}  {status}   ")
    sys.stdout.flush()


def countdown(minutes, label=""):
    total = minutes * 60
    elapsed = 0
    paused = False

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        last_tick = time.time()

        while elapsed < total:
            _render_countdown(label, total - elapsed, total, paused)

            r, _, _ = select.select([sys.stdin], [], [], 0.1)
            if r:
                ch = sys.stdin.read(1)
                if ch == '\x03':
                    raise KeyboardInterrupt
                elif ch == 'p':
                    paused = not paused
                    last_tick = time.time()

            if not paused and time.time() - last_tick >= 1.0:
                elapsed += 1
                last_tick = time.time()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    sys.stdout.write("\n")


def elapsed_timer(label=""):
    elapsed = 0
    paused = False

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        last_tick = time.time()

        while True:
            _render_elapsed(label, elapsed, paused)

            r, _, _ = select.select([sys.stdin], [], [], 0.1)
            if r:
                ch = sys.stdin.read(1)
                if ch == '\x03':
                    raise KeyboardInterrupt
                elif ch in ('\r', '\n'):
                    break
                elif ch == 'p':
                    paused = not paused
                    last_tick = time.time()

            if not paused and time.time() - last_tick >= 1.0:
                elapsed += 1
                last_tick = time.time()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    sys.stdout.write("\n")
