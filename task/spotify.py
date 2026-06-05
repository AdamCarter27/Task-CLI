import subprocess


def _tell(cmd):
    subprocess.run(
        ["osascript", "-e", f'tell application "Spotify" to {cmd}'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )


def play(uri=None):
    if uri:
        _tell(f'play track "{uri}"')
    else:
        _tell("play")


def pause():
    _tell("pause")
