from mailroom import count_emails, count_group, read_leads

# ---------- tests ----------

leads: str = read_leads("data/leads.csv")

# Behavior 1: when the file is read, its output type is string
assert type(leads) is str, "reading the file should give back text (str)"

# Behavior 2: total number of emails is 24
assert count_emails(leads) == 24, "there should be 24 emails"

# Behavior 3: the it-compliance group has 8 rows
assert count_group(leads, "it-compliance") == 8, "it-compliance should have 8 rows"

print("All checks passed!")
