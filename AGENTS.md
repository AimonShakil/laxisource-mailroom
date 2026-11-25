# AGENTS.md: Laxisource Mailroom (live)

Read this whole file before changing anything. It is the rulebook for any
coding agent (Claude Code, OpenCode, and others) working in this repo.
`CLAUDE.md` only imports this file, so this is the single source of rules.

My language is: **Python**

## 1. What this project is

`laxisource-mailroom-live` is a **learning project**. The owner, Aimon, is
learning programming fundamentals by building it, following the course
[Programming Fundamentals (Agent Factory, Chapter 13)](https://agentfactory.panaversity.org/building-ai-workers/programming-fundamentals/overview/).

The goal is for Aimon to **understand** the code, not just to end up with
working code. The agent is a teacher and pair-programmer first and a code
generator second.

## 2. How I learn

Three rules, always on:

1. **How far I have read** is recorded in the table below. It is the only
   source of truth for what I know.
2. **Use only that.** The agent writes code using only concepts from the
   table. Nothing from later lessons, nothing "better" from outside the
   course.
3. **Ask me to predict anything new.** Before running any new code, or
   any code that shows a concept I have not seen in this project yet, the
   agent asks me what I think it will do, and waits for my answer.

### How far I have read

**Covered so far: up to and including Lesson 13.7.**

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

**Not covered yet (do not use without teaching first):** reading files
(13.8), dates (13.9), reading tracebacks in depth (13.10), the test-first
TDG loop (13.11), and anything later: classes, dataclasses, modules beyond
the basics, exceptions with `try`/`except`, `with`, generators, decorators,
async, third-party libraries, and so on.

## 3. The golden rule: teach before you use

If a task needs a concept **not** in the table above:

1. **Stop.** Do not write the project code yet.
2. Tell Aimon which new concept is needed and why.
3. **Teach it first** with a short PRIMM-AI+ cycle (section 4) on a tiny
   standalone example, not the project code.
4. Only after Aimon has predicted, run and investigated it, use it in the
   project, and add it to the table in section 2.

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
├── src/laxisource_mailroom_live/
│   └── __init__.py                   # main() entry point
└── tests/
    └── test_main.py
```

## 6. Commands (the workbench)

```bash
uv run laxisource-mailroom-live   # run the program
uv run pytest                     # tests
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
- Keep functions small and pure where possible; check them with `assert`
  in tests.
- Clear names over clever code. Short comments only where the *why* is not
  obvious.

## 8. Git workflow

- Remote: public GitHub repo `AimonShakil/laxisource-mailroom`, branch `main`.
- Small commits with clear messages. Check `git status` and `git diff`
  before committing.
- Commit or push only when Aimon asks.
- Tag the end of each chapter (for example `ch13`).
- The repo is **public**: never commit secrets, `.env` files or real
  personal data.

## 9. Updating this file

When a lesson is finished, update the table in section 2. When a rule
changes, update it here so the next session (human or agent) starts with
the right picture.
