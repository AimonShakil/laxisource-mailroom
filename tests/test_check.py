from check import get_emails, read_text, rows_in_group

LEADS_PATH = "data/leads.csv"


def test_read_text_returns_a_string() -> None:
    text = read_text(LEADS_PATH)
    assert type(text) is str


def test_there_are_24_emails() -> None:
    text = read_text(LEADS_PATH)
    emails = get_emails(text)
    assert len(emails) == 24


def test_it_compliance_group_has_8_rows() -> None:
    text = read_text(LEADS_PATH)
    rows = rows_in_group(text, "it-compliance")
    assert len(rows) == 8


def test_every_it_compliance_row_is_in_that_group() -> None:
    text = read_text(LEADS_PATH)
    rows = rows_in_group(text, "it-compliance")
    for row in rows:
        assert row[3] == "it-compliance"
