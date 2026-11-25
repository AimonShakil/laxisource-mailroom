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


# ---------- tests ----------

leads: str = read_leads("data/leads.csv")

# Behavior 1: when the file is read, its output type is string
assert type(leads) is str, "reading the file should give back text (str)"

# Behavior 2: total number of emails is 24
assert count_emails(leads) == 24, "there should be 24 emails"

# Behavior 3: the it-compliance group has 8 rows
assert count_group(leads, "it-compliance") == 8, "it-compliance should have 8 rows"

print("All checks passed!")
