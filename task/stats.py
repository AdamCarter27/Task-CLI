import subprocess
import json
from datetime import datetime, timezone
from collections import defaultdict


def _get_entries(period):
    result = subprocess.run(
        ["timew", "export", period],
        capture_output=True, text=True
    )
    if not result.stdout.strip():
        return []
    return json.loads(result.stdout)


def _duration_seconds(entry):
    fmt = "%Y%m%dT%H%M%SZ"
    start = datetime.strptime(entry["start"], fmt).replace(tzinfo=timezone.utc)
    end = (
        datetime.strptime(entry["end"], fmt).replace(tzinfo=timezone.utc)
        if "end" in entry
        else datetime.now(timezone.utc)
    )
    return (end - start).total_seconds()


def _summarize(entries):
    totals = defaultdict(float)
    for entry in entries:
        tags = entry.get("tags", [])
        if not tags:
            continue
        category = tags[0].split("+")[0].capitalize()
        totals[category] += _duration_seconds(entry)
    return totals


def _fmt(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    return f"{h}h {m:02d}m" if h else f"{m}m"


def _print_block(label, totals):
    print(f"\n{label}")
    print("─" * 35)
    if not totals:
        print("  No data.")
        print()
        return

    total_secs = sum(totals.values())
    for cat, secs in sorted(totals.items(), key=lambda x: -x[1]):
        bar = "█" * int(secs / total_secs * 20)
        print(f"  {cat:<14} {_fmt(secs):>7}  {bar}")
    print("─" * 35)
    print(f"  {'Total':<14} {_fmt(total_secs):>7}")
    print()


def show():
    _print_block("Today", _summarize(_get_entries(":day")))
    _print_block("This Week", _summarize(_get_entries(":week")))


def recent_entries(n=10):
    result = subprocess.run(
        ["timew", "export", ":all"],
        capture_output=True, text=True
    )
    if not result.stdout.strip():
        return []
    entries = json.loads(result.stdout)
    return entries[-n:]


def fmt_entry(entry):
    fmt = "%Y%m%dT%H%M%SZ"
    start = datetime.strptime(entry["start"], fmt).replace(tzinfo=timezone.utc)
    start_local = start.astimezone().strftime("%Y-%m-%d %H:%M")

    if "end" in entry:
        end = datetime.strptime(entry["end"], fmt).replace(tzinfo=timezone.utc)
        end_str = end.astimezone().strftime("%H:%M")
        duration = _fmt((end - start).total_seconds())
    else:
        end_str = "now"
        duration = _fmt((datetime.now(timezone.utc) - start).total_seconds())

    tag = entry.get("tags", ["?"])[0]
    return f"@{entry['id']}  {tag:<25} {start_local} → {end_str}  ({duration})"
