import sys
from pathlib import Path


def read_leads(path: str) -> str:
    """Promise: give back the whole file as one piece of text."""
    return Path(path).read_text(encoding="utf-8")


def count_emails(text: str) -> int:
    """Promise: count the lead rows (one email per row, header not counted)."""
    lines = text.strip().split("\n")
    return len(lines) - 1  # minus 1 for the header line


def count_group(text: str, group: str) -> int:
    """Promise: count the rows whose group column equals `group`."""
    lines = text.strip().split("\n")
    count = 0
    for line in lines[1:]:  # skip the header line
        parts = line.strip().split(",")
        if parts[3] == group:
            count += 1
    return count


def list_subscribers(text: str) -> list[str]:
    """Promise: one line per lead, as "First Last <email>" (header skipped)."""
    lines = text.strip().split("\n")
    subscribers: list[str] = []
    for line in lines[1:]:  # skip the header line
        parts = line.strip().split(",")
        subscribers.append(parts[0] + " " + parts[1] + " <" + parts[2] + ">")
    return subscribers


# Runs only for `uv run mailroom.py ...`, not when check.py imports this file.
if __name__ == "__main__":
    # sys.argv is the list of words typed after `uv run`: ["mailroom.py", "subscribers"]
    if len(sys.argv) > 1 and sys.argv[1] == "subscribers":
        leads = read_leads("data/leads.csv")
        for subscriber in list_subscribers(leads):
            print(subscriber)
    else:
        print("Usage: uv run mailroom.py subscribers")
