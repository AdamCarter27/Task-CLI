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


def _active_elapsed(start, paused_total, pause_start):
    paused_now = (time.time() - pause_start) if pause_start else 0
    return time.time() - start - paused_total - paused_now


def countdown(minutes, label=""):
    total = minutes * 60
    start = time.time()
    paused_total = 0.0
    pause_start = None

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)

        while True:
            elapsed = _active_elapsed(start, paused_total, pause_start)
            if elapsed >= total:
                break
            _render_countdown(label, int(total - elapsed), total, pause_start is not None)

            r, _, _ = select.select([sys.stdin], [], [], 0.1)
            if r:
                ch = sys.stdin.read(1)
                if ch == '\x03':
                    raise KeyboardInterrupt
                elif ch == 'p':
                    if pause_start is None:
                        pause_start = time.time()
                    else:
                        paused_total += time.time() - pause_start
                        pause_start = None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    sys.stdout.write("\n")


def elapsed_timer(label=""):
    start = time.time()
    paused_total = 0.0
    pause_start = None

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)

        while True:
            elapsed = int(_active_elapsed(start, paused_total, pause_start))
            _render_elapsed(label, elapsed, pause_start is not None)

            r, _, _ = select.select([sys.stdin], [], [], 0.1)
            if r:
                ch = sys.stdin.read(1)
                if ch == '\x03':
                    raise KeyboardInterrupt
                elif ch in ('\r', '\n'):
                    break
                elif ch == 'p':
                    if pause_start is None:
                        pause_start = time.time()
                    else:
                        paused_total += time.time() - pause_start
                        pause_start = None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    sys.stdout.write("\n")
