from mailroom import count_emails, count_group, list_subscribers, read_leads

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

print("All checks passed!")
