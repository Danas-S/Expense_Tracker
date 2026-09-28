# Final root Expense Tracker: lab checklist and validation

The authoritative implementation is root `expenses.py`. The original Week 5
work and the corrected Week 9 improvements have been compared and consolidated
into it, including every current custom test. The supplied lab screenshots were
reviewed before removal; this checklist retains their relevant requirements.
[The file inventory](before/reference_inventory.md) records all source files,
their hashes and what was retained or superseded.

The original lab asked for `week5/` and `week9/` submission folders. The user's
final cleanup request explicitly replaces that layout with one root project.
This is an intentional layout change, not a claim that the old folder requirement
was met by the new layout. Prior versions remain in Git history at `e90b855`.

## Requirements extracted from the lab instructions

Status meanings: **Pass** is implemented and checked; **Retained** is preserved
coursework content; **Manual/history** cannot be established by a code repair.
Source names refer to the supplied screenshots before their removal.

| Requirement | Source | Final evidence / status |
| --- | --- | --- |
| Store expenses in `expenses.csv`; create it if missing | Week 5 (2)-(3) | Pass: loader and real-file tests |
| Require `id,date,description,amount,category`; ask before replacing an invalid header | Week 5 (3) | Pass: header validation and yes/no tests; refusal returns `None` to `main` |
| Write the header on creation/overwrite; otherwise load existing rows | Week 5 (3) | Pass: creation, overwrite and load/save round-trip tests |
| Keep changes in memory until Save | Week 5 (3) | Pass: add leaves the existing file unchanged until save |
| Loop over a numbered menu for display, group, add, save and exit | Week 5 (3), given test | Pass: exactly five options, dispatch and integration tests |
| Show date, description, amount and category in a table | Week 5 (3) | Pass: content, formatting and dynamic-width tests |
| Group by date or category and display sums | Week 5 (3) | Pass: submenu, grouping and sums tests |
| Enter one expense line in the lecturer's format; `<` cancels | Week 5 (3), given test | Pass: complete record, cancellation and unchanged lecturer integration |
| Save the current list including newly added items | Week 5 (3) | Pass: exact persisted rows and amount text, including CSV quoting |
| Re-request invalid input or accept the cancellation value | Week 5 (3) | Pass: invalid menu, grouping, yes/no and expense-entry tests |
| One production file named `expenses.py`, entry point named `main` | Week 5 (3)-(4) | Pass: root implementation, only standard-library imports |
| Functions about 20 code lines or less | Week 5 (3) | Pass: maximum 17 including `def`, excluding docstrings/comments/blanks |
| Avoid repeated code and unused artefacts | Week 5 (3)-(4) | Pass: shared CSV fields, menu configuration and pause; obsolete helpers/import removed |
| Keep all textual prompts and messages in a dictionary | Week 5 (4) | Pass: `PROMPTS` includes menu labels, headings and status/error messages |
| Every function has a description, parameters, returns and natural-language Tests section | Week 5 (4) | Pass: all 19 production functions checked |
| Generate tests from function docstring specifications in `test_expenses.py` | Week 5 (5) | Pass for current coverage: mapping below; original Copilot provenance retained, later repairs attributed to Codex |
| Run custom tests, manual tests and the unmodified lecturer test | Week 5 (5) | Pass: commands and results below; lecturer bytes unchanged |
| Explain Python-specific constructs with `# PYTHON:` comments, once per construct | Week 5 (5) | Pass: generators, comprehensions, context managers, f-strings, dictionaries, unpacking, CSV helpers, `defaultdict`, enumeration and entry guard |
| Draw an original decomposition on paper before development, photograph and commit it before code | Week 5 (4) | Retained: original photo `expensediagram.jpg`; historical sequence cannot be recreated |
| Develop/test one function at a time and make separate commits describing progress and learning | Week 5 (4)-(5) | Manual/history: existing history preserved; actual repair and consolidation stages committed separately |
| Final diagram stays similar, uses matching component numbers and ends each description with its function name in brackets | Week 5 (6) | Manual: JPG retained; exact required corrections in `diagram_review.md`; no image edit claimed |
| Explain the decomposition and demonstrate the first function and its tests | Week 5 (2) | Manual demo preparation |
| Start in the lab; consult the lecturer/TA as customer when clarification is needed; prerequisites are prior labs | Week 5 (1)-(4) | Manual/history; no consultation or past attendance is fabricated |
| Commit/push to the module repository; original snapshot deadline 8 March 2026, 23:59, with no Brightspace submission | Week 5 (2) | Historical submission instruction retained; current commits do not establish an earlier submission |
| Research percentage energy-use variation caused by prompting styles | Week 9 (9) | Retained: first answer in `research.md`; no new research claimed |
| Explain at least three energy-efficient prompt characteristics | Week 9 (9) | Retained: three explanations in `research.md` |
| Explain whether energy-optimal prompting varies across genAI products | Week 9 (9) | Retained: corresponding answer in `research.md` |
| Name three kinds of information to exclude from prompts for privacy | Week 9 (9) | Retained: personal, financial and health examples in `research.md` |
| Root README contains one or two sentences acknowledging GitHub Copilot assistance | Week 9 (10) | Pass: provenance retained, with later Codex repair accurately distinguished |
| Copy the original implementation as the starting point for improvements | Week 9 (10) | Historical development versions retained in Git; final consolidation intentionally removes duplicate implementations |
| Choose three improvements, describe affected people, record prompts and briefly describe solutions | Week 9 (10) | Retained and implemented: invalid-header refusal, dynamic table widths, shared menu configuration |
| Show an improvement for users and one for developers; discuss Copilot usage experiment and conclusions | Week 9 (9) | Manual demo: file safety/table readability for users, shared configuration for developers; no experiment fabricated |
| Week 9 prerequisite is Lab 8; commit/push progress with learning comments | Week 9 (9) | Prerequisite is historical; current changes use real commits without rewriting history |

Week 9 (1)-(8) provide background on utilitarianism, deontology, virtue ethics,
fairness, transparency, accountability, privacy, safety, human oversight,
sustainability, ownership and academic integrity, and common genAI mistakes.
They add no separate code deliverable. Their practical requirements are captured
by the research, provenance, testing and improvement rows above. Week 5 (1)
introduces functional decomposition and bottom-up implementation.

## Final behaviour and coursework evidence

Both `DD/MM/YY` and `YYYY-MM-DD` are accepted. Entered amount text such as
`50.00` or `5` is retained when saving; displayed amounts use two decimal places.
The application uses one-line entry and `<` cancellation throughout.

Expense-entry EOF returns `False`; pause EOF returns normally. Grouping and
overwrite-confirmation EOF propagate to `main`, which returns cleanly. EOF
never grants overwrite permission. Invalid-header refusal returns `None` from
the helper through the loader, and `main` stops before displaying its menu.
Helpers never terminate the process; save catches file I/O errors specifically.

All 67 meaningful tests from the repaired Week 5 suite are retained, adapted
where the final interface contract changed, alongside the 11 improvement tests.
Input mocks are finite or explicitly raise `EOFError`. The original stale suite
remains byte-for-byte in `before/test_expenses_original.py.txt`, outside discovery.
The lecturer file, original CSV and both diagrams remain unchanged at the root.
The research file was copied byte-for-byte to `research.md`; the original prompt
quotations and sustainability/privacy answers were not altered or re-researched.

## Docstring test coverage map

The named test classes are in root `test_expenses.py`, except the immutable
lecturer `TestExpensesMain` in root `test_expenses_given.py`.

| Production function | Automated tests covering the stated contract |
| --- | --- |
| `load_or_create_expenses` | `TestLoadOrCreateExpenses`, `TestFileRoundTrip`, `TestEndOfInput`; `TestFileValidation` |
| `_create_csv_file` | `TestCreateCSVFile`, overwrite/empty-file cases in `TestFileRoundTrip` |
| `_load_or_validate_file` | `TestLoadOrCreateExpenses`, `TestFileRoundTrip`; `TestFileValidation` |
| `display_expenses` | `TestDisplayExpenses`; `TestDynamicTable` |
| `_print_expense_table` | `TestDynamicTable`: long text, wide amounts, borders, heading minimums, right alignment |
| `group_expenses` | `TestGroupExpenses`: date/category sums, table output and empty list |
| `add_expense` | `TestAddExpense`, `TestFileRoundTrip`: complete record, `<`, retries, IDs, EOF, save after add |
| `_parse_expense_line` | `TestParsing`: both date formats, amount text, whitespace, field counts, invalid date/amount |
| `_is_valid_date_text` | `TestParsing`: supported formats, real dates and leap years |
| `_create_expense_dict` | `TestCreateExpenseDict`, `TestParsing`: fields, IDs, numeric/string amounts |
| `save_expenses` | `TestSaveExpenses`, `TestFileRoundTrip`: exact rows, headers, quoting, I/O failure and unexpected errors |
| `get_valid_yes_no` | `TestGetValidYesNo`, `TestEndOfInput`: yes/no, aliases, case, retry, EOF |
| `get_next_id` | `TestGetNextId`, `TestParsing`: empty list, sequential IDs, unsorted IDs with gaps |
| `_build_menu_options_text` | `TestMenuConfiguration`: exact interface, changed dictionary labels, configured order/numbers |
| `_build_menu_choice_prompt` | `TestMenuConfiguration`: default and changed valid-choice lists |
| `main` | `TestMainMenu`, `TestEndOfInput`, lecturer `TestExpensesMain`; `TestFileValidation` |
| `_handle_menu_choice` | `TestHandleMenuChoice`: all five routes, exact arguments, pauses, no unrelated calls |
| `_handle_group_choice` | `TestGroupChoice`, `TestEndOfInput`: date/category, retry and EOF |
| `_wait_for_enter` | `TestEndOfInput`: Enter and EOF each consume one input call |

## Validation commands and results

Run from the repository root:

```text
python -m unittest test_expenses
python -m unittest test_expenses_given
python -m unittest discover -v
python expenses.py
```

| Root suite | Tests | Failures | Errors |
| --- | ---: | ---: | ---: |
| Custom expense tests | 78 | 0 | 0 |
| Lecturer-provided test | 1 | 0 | 0 |
| Full unittest discovery | 79 | 0 | 0 |

The root suites passed both before and after removing `week5/`, `week9/` and
`Lab Instructions/`, confirming that the retained project is self-contained.
Each run was bounded by a subprocess timeout. Static checks cover function docstrings,
function sizes, import/function usage, preserved hashes and local documentation
links. The docstring coverage map describes every production function.

Command-line smoke checks use a normal menu session and closed stdin. Temporary
working directories protect `expenses.csv` while checking add, cancel, grouping,
save/reload, invalid input, empty stdin, nested EOF and overwrite yes/no.
Successful checks terminate with status 0 and no stderr.

## Remaining manual evidence

Apply the numbering, function labels and flow changes in
[diagram_review.md](diagram_review.md) to the retained final JPG. No editable
source was supplied and no image edit is claimed. Prepare the demo explanations
listed in the checklist, including your original Copilot usage and conclusions.
No screenshots, historical commits, experiments or submission dates are fabricated.
