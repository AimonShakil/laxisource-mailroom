from pathlib import Path


def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def lead_lines(text: str) -> list[str]:
    # Skip line 0: it is the header with the column names, not a lead.
    lines = text.strip().split("\n")
    return [line.strip() for line in lines[1:]]


def get_emails(text: str) -> list[str]:
    return [line.split(",")[2] for line in lead_lines(text)]


def rows_in_group(text: str, group: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in lead_lines(text):
        row = line.split(",")
        if row[3] == group:
            rows.append(row)
    return rows


text = read_text("data/leads.csv")
print("Type:", type(text))
print("Emails:", len(get_emails(text)))
for row in rows_in_group(text, "it-compliance"):
    print(row)
