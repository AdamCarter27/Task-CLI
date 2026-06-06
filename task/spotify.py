import subprocess
import re
import time


def _to_uri(url_or_uri):
    if url_or_uri.startswith("spotify:"):
        return url_or_uri
    match = re.search(r'open\.spotify\.com/([^/?]+)/([^/?]+)', url_or_uri)
    if match:
        return f"spotify:{match.group(1)}:{match.group(2)}"
    return url_or_uri


def _tell(cmd):
    subprocess.run(
        ["osascript", "-e", f'tell application "Spotify" to {cmd}'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )


def play(uri=None):
    if uri:
        spotify_uri = _to_uri(uri)
        # open acts like a deep link click — navigates and starts playback
        subprocess.Popen(
            ["open", spotify_uri],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        time.sleep(3)
        _tell("play")  # backup in case open navigated but didn't autoplay
    else:
        _tell("play")


def pause():
    _tell("pause")
