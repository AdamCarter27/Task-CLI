# task-cli

A productivity CLI for tracking time across tasks using [Timewarrior](https://timewarrior.net/), with a built-in Pomodoro timer for focused study sessions.

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
| `task stats`     | Show time totals for today and this week |
| `task config`    | Add or remove categories/subcategories   |
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

Categories are stored in `~/.config/task-cli/config.json` and created with defaults on first run. Use `task config` to add or remove categories and subcategories interactively, or edit the file directly:

```json
{
  "categories": {
    "Programming": ["LeetCode", "Personal Project", "Work Project", "Other"],
    "Math": ["Homework", "Review", "Other"]
  }
}
```
