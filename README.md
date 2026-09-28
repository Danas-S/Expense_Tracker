# Expense_Tracker
A Personal Expense Tracker in Python for the GenAI-Assisted Programming module at TU Dublin.

The code in this repository was written with the assistance of GitHub Copilot. This repair pass used OpenAI Codex for debugging, test updates and refinement.

The root `expenses.py` is the authoritative tracker, combining the original
assignment with the corrected file handling, dynamic tables and menu configuration.
Run it from this directory with `python expenses.py`.

Run the tests from this directory:

```text
python -m unittest test_expenses
python -m unittest test_expenses_given
python -m unittest discover -v
```

