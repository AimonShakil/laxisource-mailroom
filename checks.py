from datetime import date

from mailroom import (
    count_emails,
    count_group,
    count_joined_since,
    get_option,
    list_subscribers,
    next_send,
    read_leads,
    subscriber_summary,
)

# ---------- tests ----------

leads: str = read_leads("data/subscribers.csv")

# Behavior 1: when the file is read, its output type is string
assert type(leads) is str, "reading the file should give back text (str)"

# Behavior 2: total number of emails is 24
assert count_emails(leads) == 24, "there should be 24 emails"

# Behavior 3: the it-compliance group has 8 rows
assert count_group(leads, "it-compliance") == 8, "it-compliance should have 8 rows"

# Behavior 4: listing subscribers gives one line per lead, header skipped
subscribers = list_subscribers(leads)
assert len(subscribers) == 24, "there should be 24 subscribers"
assert subscribers[0] == "Ayesha Khan <ayesha.khan@example.com>", "first should be Ayesha"

# Behavior 5: the summary shows the total first, then one count per group
summary = subscriber_summary(leads)
assert summary == [
    "Total subscribers: 24",
    "enterprise-chro: 8",
    "it-compliance: 8",
    "mid-market-hr: 8",
], "summary should be the total, then 8 in each of the 3 groups"

# Behavior 6: with run date 2026-11-20, 7 subscribers joined in the last 30 days
run_date = date.fromisoformat("2026-11-20")
assert count_joined_since(leads, run_date, 30) == 7, "7 should have joined in 30 days"

# Behavior 7: joining exactly 30 days before the run date (2026-10-21) counts
boundary = "first_name,last_name,email,group,joined_on,consent\nA,B,a@example.com,x,2026-10-21,form"
assert count_joined_since(boundary, run_date, 30) == 1, "2026-10-21 should count"

# Behavior 8: next send is the first Monday of the next month
assert next_send(date.fromisoformat("2026-11-20")) == date.fromisoformat("2026-12-07")
assert next_send(date.fromisoformat("2026-12-07")) == date.fromisoformat("2027-01-04")

# Behavior 9: get_option gives the word after the option name, or "" if missing
args = ["mailroom.py", "next-send", "--run-date", "2026-11-20"]
assert get_option(args, "--run-date") == "2026-11-20", "should find the run date"
assert get_option(args, "--since-days") == "", "missing option should give empty text"

print("All checks passed!")
