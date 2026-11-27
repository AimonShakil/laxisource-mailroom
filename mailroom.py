import sys
from datetime import date, timedelta
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


# The groups we send to. Add a name here if a new group appears in the CSV.
GROUPS: list[str] = ["enterprise-chro", "it-compliance", "mid-market-hr"]


def subscriber_summary(text: str) -> list[str]:
    """Promise: the total line first, then one "group: count" line per group."""
    summary: list[str] = ["Total subscribers: " + str(count_emails(text))]
    for group in GROUPS:
        summary.append(group + ": " + str(count_group(text, group)))
    return summary


def count_joined_since(text: str, run_date: date, days: int) -> int:
    """Promise: count rows whose joined_on is in the `days` days up to run_date."""
    cutoff = run_date - timedelta(days=days)
    lines = text.strip().split("\n")
    count = 0
    for line in lines[1:]:  # skip the header line
        parts = line.strip().split(",")
        joined_on = date.fromisoformat(parts[4])
        if joined_on >= cutoff and joined_on <= run_date:
            count += 1
    return count


def next_send(run_date: date) -> date:
    """Promise: the first Monday of the month after run_date."""
    if run_date.month == 12:
        day = date(run_date.year + 1, 1, 1)
    else:
        day = date(run_date.year, run_date.month + 1, 1)
    while day.weekday() != 0:  # 0 is Monday
        day = day + timedelta(days=1)
    return day


def get_option(args: list[str], name: str) -> str:
    """Promise: the word after `name` in args, or "" if `name` is not there."""
    i = 0
    while i < len(args) - 1:
        if args[i] == name:
            return args[i + 1]
        i += 1
    return ""


def pick_run_date(args: list[str]) -> date:
    """Promise: the --run-date from args, or today if none was given."""
    text = get_option(args, "--run-date")
    if text:
        return date.fromisoformat(text)
    # The only place that reads today's date: the logic always gets it passed in.
    return date.today()


# Runs only for `uv run mailroom.py ...`, not when the tests import this file.
if __name__ == "__main__":
    # sys.argv is the list of words typed after `uv run`: ["mailroom.py", "subscribers"]
    command = ""
    if len(sys.argv) > 1:
        command = sys.argv[1]
    if command == "subscribers":
        leads = read_leads("data/subscribers.csv")
        for line in subscriber_summary(leads):
            print(line)
        since_days = get_option(sys.argv, "--since-days")
        if since_days:
            run_date = pick_run_date(sys.argv)
            count = count_joined_since(leads, run_date, int(since_days))
            print("Joined in the last " + since_days + " days: " + str(count))
    elif command == "next-send":
        run_date = pick_run_date(sys.argv)
        print("Next send: " + str(next_send(run_date)))
    else:
        print("Usage: uv run mailroom.py subscribers [--since-days N] [--run-date YYYY-MM-DD]")
        print("       uv run mailroom.py next-send [--run-date YYYY-MM-DD]")
