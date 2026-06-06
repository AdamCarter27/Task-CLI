# task-cli

A productivity CLI for tracking time across tasks using [Timewarrior](https://timewarrior.net/), with a built-in Pomodoro timer for focused study sessions.

![demo](demo.gif)

## Requirements

- [Timewarrior](https://timewarrior.net/) (`timew`)
- [fzf](https://github.com/junegunn/fzf)
- Python 3.8+

Install on macOS:
```
brew install timewarrior fzf
```

Install on Linux:
```
sudo apt install timewarrior fzf
```

## Installation

```
git clone https://github.com/AdamCarter27/task-cli
cd task-cli
pip install -e .
```

## Commands

| Command          | Description                              |
|------------------|------------------------------------------|
| `task start`     | Start a new session                      |
| `task stop`      | Stop any running session                 |
| `task stats`     | Show time totals for today and this week |
| `task config`    | Add or remove categories and toggle settings |
| `task edit`      | Fix or delete a recent session           |
| `task shortcuts` | Show all commands and key bindings       |

## Timer modes

When starting a session you'll be prompted to pick a mode:

- **Open Timer** — tracks time with no countdown; press Enter when you're done
- **Timer** — single countdown with a custom duration you set at start
- **Pomodoro** — repeating 25-minute work cycles with short and long breaks

## Controls

### Selection menus
| Key       | Action            |
|-----------|-------------------|
| `j` / `k` | Move down / up (similar to vim motions)  |
| Enter     | Confirm selection |
| Ctrl-C    | Cancel            |

### During a timer
| Key    | Action                        |
|--------|-------------------------------|
| `p`    | Pause / resume                |
| Enter  | Stop (Open Timer only)        |
| Ctrl-C | Quit                          |

## Configuration

All config is stored in `~/.config/task-cli/config.json` and created with defaults on first run. Use `task config` to manage everything interactively, or edit the file directly:

```json
{
  "categories": {
    "Programming": ["LeetCode", "Personal Project", "Work Project", "Other"],
    "Math": ["Homework", "Review", "Other"]
  },
  "settings": {
    "chime": true,
    "spotify_playlist": ""
  }
}
```

### Settings

| Setting            | Default | Description |
|--------------------|---------|-------------|
| `chime`            | `true`  | Play a sound when a countdown or Pomodoro timer ends |
| `spotify_playlist` | `""`    | Spotify playlist URI to play during sessions — pauses when you pause, stops when the timer ends |

To set your Spotify playlist, right-click a playlist in Spotify → Share → Copy Spotify URI, then run `task config` → "Set Spotify playlist". The URI is stored only in your local config file and never committed to the repo.
