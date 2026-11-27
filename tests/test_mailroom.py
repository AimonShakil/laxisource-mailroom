from datetime import date

from mailroom import (
    check_subject,
    count_emails,
    count_group,
    count_joined_since,
    get_option,
    list_subscribers,
    next_send,
    pick_run_date,
    read_leads,
    subscriber_summary,
)

LEADS_PATH = "data/subscribers.csv"
RUN_ARGS = ["mailroom.py", "next-send", "--run-date", "2026-11-20"]


def test_reading_the_file_gives_text() -> None:
    leads = read_leads(LEADS_PATH)
    assert type(leads) is str


def test_there_are_24_emails() -> None:
    leads = read_leads(LEADS_PATH)
    assert count_emails(leads) == 24


def test_it_compliance_group_has_8_rows() -> None:
    leads = read_leads(LEADS_PATH)
    assert count_group(leads, "it-compliance") == 8


def test_list_subscribers_gives_one_line_per_lead() -> None:
    leads = read_leads(LEADS_PATH)
    assert len(list_subscribers(leads)) == 24


def test_list_subscribers_skips_the_header() -> None:
    leads = read_leads(LEADS_PATH)
    assert list_subscribers(leads)[0] == "Ayesha Khan <ayesha.khan@example.com>"


def test_summary_shows_total_then_count_per_group() -> None:
    leads = read_leads(LEADS_PATH)
    assert subscriber_summary(leads) == [
        "Total subscribers: 24",
        "enterprise-chro: 8",
        "it-compliance: 8",
        "mid-market-hr: 8",
    ]


def test_7_joined_in_the_30_days_up_to_2026_11_20() -> None:
    leads = read_leads(LEADS_PATH)
    run_date = date.fromisoformat("2026-11-20")
    assert count_joined_since(leads, run_date, 30) == 7


def test_joining_exactly_30_days_before_run_date_counts() -> None:
    text = "first_name,last_name,email,group,joined_on,consent\nA,B,a@example.com,x,2026-10-21,form"
    run_date = date.fromisoformat("2026-11-20")
    assert count_joined_since(text, run_date, 30) == 1


def test_next_send_is_first_monday_of_next_month() -> None:
    assert next_send(date.fromisoformat("2026-11-20")) == date.fromisoformat("2026-12-07")


def test_next_send_from_december_rolls_into_next_year() -> None:
    assert next_send(date.fromisoformat("2026-12-07")) == date.fromisoformat("2027-01-04")


def test_get_option_gives_the_word_after_the_option() -> None:
    assert get_option(RUN_ARGS, "--run-date") == "2026-11-20"


def test_get_option_gives_empty_text_when_option_missing() -> None:
    assert get_option(RUN_ARGS, "--since-days") == ""


def test_pick_run_date_uses_run_date_when_given() -> None:
    assert pick_run_date(RUN_ARGS) == date.fromisoformat("2026-11-20")


# check_subject: a list of problems with the Subject line, empty when it is fine.
# Aimon's cases.


def test_empty_subject_is_one_problem_empty() -> None:
    assert check_subject("Subject:\nPreview: Hi") == ["empty"]


def test_subject_of_only_spaces_is_one_problem_empty() -> None:
    assert check_subject("Subject:     \nPreview: Hi") == ["empty"]


def test_no_subject_line_is_one_problem_missing() -> None:
    assert check_subject("Preview: Hi\n\nHi {{first_name}},") == ["missing"]


# Claude's cases (Aimon to confirm the answers).


def test_normal_subject_has_no_problems() -> None:
    assert check_subject("Subject: Studio opens Monday\nPreview: Hi") == []


def test_issue_01_subject_has_no_problems() -> None:
    issue = read_leads("docs/issue-01.md")
    assert check_subject(issue) == []


def test_subject_of_exactly_50_characters_is_fine() -> None:
    assert check_subject("Subject: " + "a" * 50 + "\nPreview: Hi") == []


def test_subject_of_51_characters_is_one_problem_too_long() -> None:
    assert check_subject("Subject: " + "a" * 51 + "\nPreview: Hi") == ["too long"]


def test_subject_not_on_the_first_line_is_missing() -> None:
    assert check_subject("Preview: Hi\nSubject: Studio opens Monday") == ["missing"]


def test_empty_file_is_one_problem_missing() -> None:
    assert check_subject("") == ["missing"]


def test_windows_line_ending_does_not_count_toward_length() -> None:
    assert check_subject("Subject: " + "a" * 50 + "\r\nPreview: Hi") == []
