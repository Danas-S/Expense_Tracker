# Expense Tracker repair and lab review

This review covers the supplied Week 5 and Week 9 lab screenshots, both
implementations, all current tests, the research notes and both supplied JPG
diagrams. The root program and tests originally matched Week 5 byte for byte;
they have received the same repairs so root discovery is safe too.

## Behaviour and decomposition

- Each version remains a single `expenses.py` with `main` as its entry point.
- The menu retains five options. Entry is one `date,description,amount,category`
  line; `<` cancels. Both `DD/MM/YY` and `YYYY-MM-DD` remain supported.
- Entered amount text is retained when saving, including `50.00` versus `5`.
  Displayed amounts use two decimal places. CSV quoting is handled by the
  standard-library writer, so loaded descriptions with commas/quotes survive saving.
- Expense-entry EOF returns `False`; pause EOF returns normally. Grouping and
  overwrite-confirmation EOF propagate to `main`, which returns cleanly. Helpers
  do not terminate the process. EOF never grants overwrite permission.
- Week 5 keeps its original behaviour of returning an empty list on a declined
  overwrite. Week 9 improves this: the validation helper and loader return
  `None`, and `main` stops before showing the menu. The file stays unchanged.
- Week 9 still demonstrates the three recorded improvements: safer invalid-header
  handling, data-sized table columns, and menu configuration shared by its labels,
  prompts and dispatch. The original research answers and prompt quotations remain.

## Lab requirements checked

All production functions contain a description, `Parameters`, `Returns` and
`Tests` in their docstrings. The longest function is 17 code lines, including
the `def` line and excluding docstrings, comments and blank lines. The obsolete
`_get_text_input`, `get_valid_date`, `get_valid_amount` and `os` import were removed;
current parsing and date validation have their own tests. All remaining production
functions are called by the application and exercised by the automated suites.

All textual prompts, menu labels, table headings and status/error messages are
in `PROMPTS`. CSV field names are data-format constants. Repeated menu pauses
and CSV header definitions were consolidated. Python-specific constructs have
`# PYTHON:` explanations, including comprehensions, generators, unpacking,
context managers, f-strings, dictionaries, CSV readers/writers, `defaultdict`,
slicing where used, and the module entry-point guard. No third-party dependency
or production package was introduced.

The lecturer's root and Week 5 files were not edited. Week 9 has an identical
copy, including the original assertions and exact CSV expectations. The stale
custom tests remain byte-for-byte in `before/test_expenses_original.py.txt`;
unittest discovery cannot import that historical text file. Current input mocks
use finite sequences or explicit `EOFError`; an unexpected mock retry fails
instead of returning an invalid value forever. Production code does not catch
mock-specific `StopIteration` or broad `Exception` to conceal mistakes.

## Docstring test coverage map

The named test classes are in each week's `test_expenses.py`, except the
Week 9-specific classes and the immutable lecturer `TestExpensesMain`.

| Production function | Automated tests covering the stated contract |
| --- | --- |
| `load_or_create_expenses` | `TestLoadOrCreateExpenses`, `TestFileRoundTrip`, `TestEndOfInput`; Week 9 `TestWeek9FileValidation` |
| `_create_csv_file` | `TestCreateCSVFile`, overwrite/empty-file cases in `TestFileRoundTrip` |
| `_load_or_validate_file` | `TestLoadOrCreateExpenses`, `TestFileRoundTrip`; Week 9 `TestWeek9FileValidation` |
| `display_expenses` | `TestDisplayExpenses`; Week 9 `TestWeek9Table` |
| `_print_expense_table` (Week 9) | `TestWeek9Table`: long text, wide amounts, borders, heading minimums, right alignment |
| `group_expenses` | `TestGroupExpenses`: date/category sums, table output and empty list |
| `add_expense` | `TestAddExpense`, `TestFileRoundTrip`: complete record, `<`, retries, IDs, EOF, save after add |
| `_parse_expense_line` | `TestParsing`: both date formats, amount text, whitespace, field counts, invalid date/amount |
| `_is_valid_date_text` | `TestParsing`: supported formats, real dates and leap years |
| `_create_expense_dict` | `TestCreateExpenseDict`, `TestParsing`: fields, IDs, numeric/string amounts |
| `save_expenses` | `TestSaveExpenses`, `TestFileRoundTrip`: exact rows, headers, quoting, I/O failure and unexpected errors |
| `get_valid_yes_no` | `TestGetValidYesNo`, `TestEndOfInput`: yes/no, aliases, case, retry, EOF |
| `get_next_id` | `TestGetNextId`, `TestParsing`: empty list, sequential IDs, unsorted IDs with gaps |
| `_build_menu_options_text` (Week 9) | `TestWeek9Menu`: exact interface, changed dictionary labels, configured order/numbers |
| `_build_menu_choice_prompt` (Week 9) | `TestWeek9Menu`: default and changed valid-choice lists |
| `main` | `TestMainMenu`, `TestEndOfInput`, lecturer `TestExpensesMain`; Week 9 `TestWeek9FileValidation` |
| `_handle_menu_choice` | `TestHandleMenuChoice`: all five routes, exact arguments, pauses, no unrelated calls |
| `_handle_group_choice` | `TestGroupChoice`, `TestEndOfInput`: date/category, retry and EOF |
| `_wait_for_enter` | `TestEndOfInput`: Enter and EOF each consume one input call |

## Validation commands and results

Run these commands separately from inside **each** week folder:

```text
python -m unittest test_expenses
python -m unittest test_expenses_given
python -m unittest discover -v
```

| Suite | Tests | Failures | Errors |
| --- | ---: | ---: | ---: |
| Week 5 custom | 67 | 0 | 0 |
| Week 5 lecturer | 1 | 0 | 0 |
| Week 9 custom | 78 | 0 | 0 |
| Week 9 lecturer regression | 1 | 0 | 0 |

Discovery runs 68 tests in Week 5, 79 in Week 9 and 68 at the root. Each invocation
was bounded by a subprocess timeout. A call-tracing check confirmed all 16 Week 5
and 19 Week 9 production functions execute during their automated tests.

Separate command-line smoke checks use temporary working directories and closed
stdin, protecting the repository CSV files. Empty input, EOF during entry/grouping/
pauses, and EOF during invalid-header confirmation terminate with status 0 and
no stderr. Week 9 `no` preserves an invalid file and shows no menu; `yes` writes
the expected header and allows the menu to continue.

## Remaining manual evidence and demo

The supplied final diagram is an image, with no editable source. Its exact
numbering, label and flow changes are listed in
[week9/diagram_review.md](week9/diagram_review.md). No image edit is claimed.

The existing history was retained; the new commits record actual repair stages.
They do not reconstruct the lab's original function-by-function development
process, original submission date or a Copilot experiment. The research answers
were preserved rather than re-researched in this code repair.

For the demo, explain the original decomposition, one function and its tests,
the stale mock that caused the hang, EOF handling, and each of the three Week 9
improvements. Be ready to discuss your original Copilot usage and conclusions.
Capture screenshots if you need them for the demo; none have been fabricated.
