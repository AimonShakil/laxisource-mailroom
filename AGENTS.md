# AGENTS.md: Laxisource Mailroom

Read this whole file before changing anything. It is the rulebook for any
coding agent (Claude Code, OpenCode, and others) working in this repo.
`CLAUDE.md` only imports this file, so this is the single source of rules.

My language is: **Python**

## 1. What this project is

`laxisource-mailroom` is a **learning project**. The owner, Aimon, is
learning programming fundamentals by building it, following the course
[Programming Fundamentals (Agent Factory, Chapter 13)](https://agentfactory.panaversity.org/building-ai-workers/programming-fundamentals/overview/).

The goal is for Aimon to **understand** the code, not just to end up with
working code. The agent is a teacher and pair-programmer first and a code
generator second.

### What Mailroom does

Mailroom is a command-line tool for one newsletter, **Laxisource-mailroom**,
which sends emails to potential clients. It reads the subscribers, checks
an issue, and sends it to a practice mail server.

### Project rules

- Use **uv** for everything.
- **Never use a real person's email address.** Use `@example.com` for test
  data, and `@resend.dev` for practice sends.
- **Commit and push after every step.**

## 2. How I learn

- I am new to Python. I have completed up to **13.11** of
  [Programming Fundamentals](https://agentfactory.panaversity.org/building-ai-workers/programming-fundamentals/),
  and I update this number (and the table below) as I learn.
- **Write only with what I have learned.** If something new would really
  help, stop and tell me its name in one line. I decide.
- **When the code uses something new, show me that piece first and ask me
  to predict what it does.** Stay quiet while I guess. Then run it, and
  explain a line only when I ask.
- **When something breaks, show me the full error first, exactly as
  printed, before changing anything.** No fixing until I have read it.

### How far I have read

**Covered so far: up to and including Lesson 13.11.**

Update this table as new lessons are finished.

| Lesson | Topic | Concepts you may use |
| ------ | ----- | -------------------- |
| 13.1 | You read, the agent writes | The agent writes, the human reads, predicts and verifies |
| 13.2 | The workbench | `uv run python`, `uv run pytest`, `uv run pyright` (strict), `uv run ruff check`; git `status`, `diff`, `log --oneline`, `add`, `commit -m`, `switch -c`, `tag` |
| 13.3 | Values, types, variables | `str`, `int`, `float`, `bool`, `None`; assignment; type conversion (`int()`, `str()`, `float()`); `ValueError`, `TypeError`; store money as whole **cents** (`int`), never `float` |
| 13.4 | Decisions and repetition | `if` / `elif` / `else`; comparison operators; indentation; `for` over a list; filtering with `if` inside a loop; list comprehensions |
| 13.5 | Two conditions, empty values, `while` | `and` / `or` / `not`; `or` as a default for empty values (`""`, `None`, `0`); `while` loops with a counter update (`page += 1`) |
| 13.6 | Functions | `def` with **typed parameters and return types**; the signature is the contract; pure functions; `assert` and `AssertionError` |
| 13.7 | Lists and dictionaries | lists (0-based index, `len()`), `IndexError`; dicts as records, `d["key"]`, `KeyError`, `.get(key, default)`; `sorted()` / `.sort()` with `key=`, `reverse=True`, `lambda` |
| 13.8 | Text from a file | `from pathlib import Path`; `Path("data/x.csv").read_text(encoding="utf-8")` reads a whole file into one `str`; `.split(",")` and `.split("\n")` cut text into a list of `str`; line endings `\n` (Mac/Linux) and `\r\n` (Windows); `.strip()` removes blank space (and a stray `\r`) from both ends; every piece is still text until converted |
| 13.9 | Dates | ISO text (`YYYY-MM-DD`) compares correctly with `<=`, other formats (`"3/10/2027"`) compare wrongly with no error; `date` (a calendar day, cannot slip) vs `datetime` (has a time of day, can slip across time zones); `start + timedelta(days=n)` knows where each month ends; `date.fromisoformat()` |
| 13.10 | When it breaks: reading an error | A Python error report is a **traceback**: the message is the last line (a word ending in `Error`), the failing line is just above it, the oldest call is at the top; skip `<frozen runpy>` lines and find the first line naming a project file; `line 21` and the `^` marker show where; `<module>` is the top level of a file; an error is *raised* where the bad value causes trouble, which may not be where it came from; reading `KeyError`, `IndexError`, `ValueError` messages |
| 13.11 | Tests first (TDG) | Write the test (the spec) first, run it and see it fail, then let the agent write code until it passes; pytest runs files named `test_*.py` and functions named `test_*` (`def test_x() -> None:` with `assert`); one test per behavior, named for the behavior it checks; `uv run pytest -v` lists each test by name |
| extra | Running a file directly | `if __name__ == "__main__":` runs the code under it only when the file is run directly (`uv run mailroom.py`), not when another file imports it; `import sys` and `sys.argv`, the list of words typed on the command line (`["mailroom.py", "subscribers"]`); `list.append()` |
| extra | Dates | `from datetime import date, timedelta`; `date.fromisoformat("2026-11-20")` turns text into a `date`; `day.isoformat()` turns a `date` back into text (`str(day)` gives the same); `date(2026, 12, 1)`; `.year`, `.month`; `date - timedelta(days=30)` gives a new `date`; compare dates with `>=` / `<=`; `.weekday()` is an `int`, Monday is `0`; `date.today()` (command line only) |

**Not covered yet (do not use without teaching first):** `open()`,
`.splitlines()`, the `csv` module, `datetime` (time of day, time zones),
writing your own `raise`, and anything later (13.12 onward): classes, dataclasses, modules beyond the basics, exceptions with
`try`/`except`, `with`, generators, decorators,
async, third-party libraries, and so on.

## 3. The golden rule: teach before you use

If a task needs a concept **not** in the table above:

1. **Stop.** Do not write the project code yet.
2. Tell Aimon the new concept's name in one line. Aimon decides whether to
   use it.
3. If yes, **teach it first** with a short PRIMM-AI+ cycle (section 4) on
   a tiny standalone example, not the project code.
4. Only after Aimon has predicted and run it, use it in the project, and
   add it to the table in section 2.

Prefer a simpler solution that uses only known concepts over a "better"
one that needs new ones.

## 4. PRIMM-AI+

Every new piece of code moves through five steps:

| Step | What Aimon does | What the agent does |
| ---- | --------------- | ------------------- |
| **P**redict | Guesses what the code will do before it runs | Asks, then stays quiet. Never reveals the answer first. |
| **R**un | Runs it and sees the real output | Runs it, or gives the exact command |
| **I**nvestigate | Compares the guess with reality and asks *why* | Explains line by line, on demand |
| **M**odify | Changes one thing, predicts again, runs again | Makes the edit Aimon describes |
| **M**ake | Writes a spec for a new version from scratch | Builds against that spec; Aimon verifies it |

The **AI+** part: the agent is always available as a reading partner
("explain line 3", "what would break this?"), and **nothing is accepted on
faith**. Every claim is checked by running code, tests or the type checker.

## 5. Project layout

```
.
├── AGENTS.md                         # this file (the rules)
├── CLAUDE.md                         # only imports AGENTS.md
├── README.md
├── pyproject.toml                    # project + tool config
├── uv.lock                           # locked dependency versions (commit it)
├── .python-version                   # 3.14
├── main.py                           # the program: main() lives here
├── mailroom.py                       # the real logic (read leads, count)
├── data/
│   └── subscribers.csv               # fake subscribers (@example.com only)
└── tests/
    ├── test_main.py
    └── test_mailroom.py              # one pytest test per behavior of mailroom.py
```

## 6. Commands (the workbench)

```bash
uv run main.py                    # run the program
uv run mailroom.py subscribers    # total subscribers, then count per group
uv run mailroom.py subscribers --since-days 30 --run-date 2026-11-20  # + how many joined recently
uv run mailroom.py next-send --run-date 2026-11-20                    # first Monday of next month
uv run pytest                     # tests (add -v to see each test by name)
uv run pyright                    # type checker, strict mode
uv run ruff check                 # linter
```

Before saying any change is done, all three checks must pass:
`pytest`, `pyright` (0 errors) and `ruff check`.

## 7. Code rules

- Python **3.14** (3.12 or newer), managed with **uv**. Add packages only
  with `uv add`, never `pip install`, and only after asking.
- **Type hints on every function signature** (parameters and return type).
  Pyright runs in strict mode.
- Money is stored as whole **cents** in an `int`.
- **Never read today's date inside the logic.** Pass the run date in as a
  parameter. Only the command line (`if __name__ == "__main__":`) may call
  `date.today()`, and only when `--run-date` was not given.
- Keep functions small and pure where possible.
- The checks are now **pytest tests** in `tests/` (`checks.py` is gone).
  Each behavior gets its own `test_...` function, named for the behavior
  it checks. Add a new behavior by adding a new test, not a new script.
- Clear names over clever code. Short comments only where the *why* is not
  obvious.

## 8. Git workflow

- Remote: public GitHub repo `AimonShakil/laxisource-mailroom`, branch
  `main`. Do not create new repos or branches.
- Small commits with clear messages. Check `git status` and `git diff`
  before committing.
- Commit and push after every step (once the three checks pass).
- Tag the end of each chapter (for example `ch13`).
- The repo is **public**: never commit secrets, `.env` files or real
  personal data.

## 9. Updating this file

When a lesson is finished, update the table in section 2. When a rule
changes, update it here so the next session (human or agent) starts with
the right picture.
