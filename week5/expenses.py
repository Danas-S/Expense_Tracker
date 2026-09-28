"""Personal Expense Tracker

A program to track personal expenses with CSV storage and menu-driven interface.
"""

import csv
# PYTHON: 'from ... import ...' imports a specific symbol directly from a module.
from datetime import datetime
from collections import defaultdict

CSV_FIELDS = ("id", "date", "description", "amount", "category")
CSV_HEADER = ",".join(CSV_FIELDS)


# PYTHON: Dictionary literal maps string keys to prompt messages (dynamic key-value object).
PROMPTS = {
    "table_headers": {"date": "Date", "description": "Description",
                      "amount": "Amount", "category": "Category"},
    "total_heading": "Total",
    "menu_title": "\n=== Expense Tracker Menu ===",
    "menu_options": "\n1. Display all expenses\n2. Group expenses\n3. Add new expense\n4. Save expenses to file\n5. Exit",
    "menu_choice": "Enter your choice (1-5): ",
    "invalid_choice": "Invalid choice. Please enter a number between 1 and 5.",

    "item_prompt": "Enter expense as date,description,amount,category (or '<' to cancel): ",
    "invalid_item": "Invalid format. Use date,description,amount,category.",
    "group_prompt": "Group by date (d) or category (c)? ",
    "invalid_group": "Invalid choice. Enter 'd' or 'c'.",
    "continue_prompt": "",

    "expense_added": "Expense added successfully!",
    "no_expenses": "No expenses found.",
    "file_created": "Created new expenses.csv file.",
    "header_mismatch": "Existing expenses.csv has incorrect format.",
    "overwrite_prompt": "Do you want to overwrite it? (yes/no): ",
    "invalid_yes_no": "Please enter 'yes' or 'no'.",
    "file_overwritten": "File overwritten.",
    "file_not_overwritten": "File not overwritten. Treating as empty.",
    "expenses_saved": "Expenses saved to file.",
    "save_failed": "Could not save expenses to file.",
}


# load_or_create_expenses
def load_or_create_expenses(filename):
    """Load expenses from CSV file or create new file if it doesn't exist.

    Parameters:
    - filename (str): Path to the CSV file

    Returns:
    - list: List of expense dictionaries with keys: id, date, description, amount, category

    Tests:
    - check that function returns a list
    - check that file is created if it doesn't exist
    - check that header line is correctly written
    - check that data is loaded if valid file exists
    - check that user is prompted for overwrite if header is missing
    - check that file is not modified if user declines overwrite
    """
    # PYTHON: 'with open(...) as ...' is a context manager that auto-closes the file.
    with open(filename, "a+") as f:
        f.seek(0)
        first_line = f.readline().strip()
    if not first_line:
        _create_csv_file(filename, CSV_HEADER)
        return []
    return _load_or_validate_file(filename, CSV_HEADER)


def _create_csv_file(filename, header, is_overwrite=False):
    """Create a new CSV file with the specified header.

    Parameters:
    - filename (str): Path to the CSV file
    - header (str): Header line to write
    - is_overwrite (bool): True if overwriting existing file

    Returns:
    - None

    Tests:
    - check that file is created successfully
    - check that header is written correctly
    - check that appropriate message is shown
    """
    with open(filename, "w", newline="") as f:
        f.write(header + "\n")
    # PYTHON: A conditional expression selects one value using if/else on one line.
    msg = "file_overwritten" if is_overwrite else "file_created"
    print(PROMPTS[msg])


def _load_or_validate_file(filename, expected_header):
    """Validate CSV header and load data or recreate file.

    Parameters:
    - filename (str): Path to the CSV file
    - expected_header (str): Expected header line

    Returns:
    - list: Loaded expenses, or an empty list if overwrite is declined

    Tests:
    - check that valid file is loaded
    - check that invalid header triggers overwrite prompt
    - check that file is recreated if user confirms
    """
    with open(filename, "r") as f:
        first_line = f.readline().strip()

    if first_line != expected_header:
        print(PROMPTS["header_mismatch"])
        if not get_valid_yes_no(PROMPTS["overwrite_prompt"]):
            print(PROMPTS["file_not_overwritten"])
            return []
        _create_csv_file(filename, expected_header, is_overwrite=True)
        return []

    expenses = []
    # PYTHON: csv.DictReader yields each CSV row as a dictionary keyed by header names.
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            expenses.append(row)
    return expenses


# display_expenses
def display_expenses(expenses):
    """Display all expenses in a formatted table.

    Parameters:
    - expenses (list): List of expense dictionaries

    Returns:
    - None

    Tests:
    - check that table is displayed correctly with all columns
    - check that no expenses shows appropriate message
    - check that amounts are formatted properly
    """
    if not expenses:
        print(PROMPTS["no_expenses"])
        return

    print("\n" + "="*70)
    headings = PROMPTS["table_headers"]
    # PYTHON: f-string supports inline formatting/alignment inside braces.
    print(f"{headings['date']:<12} {headings['description']:<20} {headings['amount']:>12} {headings['category']:<15}")
    print("="*70)
    for expense in expenses:
        date = expense["date"]
        # PYTHON: Slice syntax [:19] returns a substring without modifying original text.
        desc = expense["description"][:19]
        amount = f"${float(expense['amount']):.2f}"
        category = expense["category"][:14]
        print(f"{date:<12} {desc:<20} {amount:>12} {category:<15}")
    print("="*70 + "\n")


# group_expenses
def group_expenses(expenses, group_by):
    """Group expenses by date or category and display sums.

    Parameters:
    - expenses (list): List of expense dictionaries
    - group_by (str): 'date' or 'category' to determine grouping

    Returns:
    - dict: Dictionary with groups as keys and total amounts as values

    Tests:
    - check that expenses are correctly grouped by date
    - check that expenses are correctly grouped by category
    - check that sums are calculated correctly
    - check that results are displayed in table format
    """
    if not expenses:
        print(PROMPTS["no_expenses"])
        return {}

    # PYTHON: defaultdict(float) auto-creates missing keys with 0.0 default values.
    groups = defaultdict(float)
    for expense in expenses:
        key = expense[group_by]
        groups[key] += float(expense["amount"])

    print("\n" + "="*50)
    header = PROMPTS["table_headers"][group_by]
    print(f"{header:<30} {PROMPTS['total_heading']:>15}")
    print("="*50)
    for key in sorted(groups.keys()):
        amount = f"${groups[key]:.2f}"
        print(f"{key:<30} {amount:>15}")
    print("="*50 + "\n")

    return dict(groups)


# add_expense
def add_expense(expenses):
    """Prompt user to enter a new expense and add to expenses list.

    Parameters:
    - expenses (list): List of expense dictionaries

    Returns:
    - bool: True if added, False if cancelled with '<' or input reaches EOF

    Tests:
    - check that valid expense is added to the list
    - check that cancellation is handled
    - check that invalid inputs are rejected with re-prompt
    - check that ID is correctly assigned
    - check that all required fields are collected
    - check that EOF cancels without changing the list
    """
    while True:
        try:
            raw_item = input(PROMPTS["item_prompt"]).strip()
        except EOFError:
            return False
        if raw_item == "<":
            return False
        parsed_item = _parse_expense_line(raw_item)
        if parsed_item is None:
            print(PROMPTS["invalid_item"])
            continue
        # PYTHON: Sequence unpacking assigns one value to each name in order.
        date, description, amount, category = parsed_item
        expenses.append(_create_expense_dict(date, description, amount, category, expenses))
        print(PROMPTS["expense_added"])
        return True


def _parse_expense_line(raw_item):
    """Parse a single-line expense entry in csv-like format.

    Parameters:
    - raw_item (str): User text in format date,description,amount,category

    Returns:
    - tuple | None: (date, description, amount, category) or None if invalid

    Tests:
    - check that valid item line is parsed
    - check that spaces around values are stripped
    - check that invalid format returns None
    - check that invalid amount returns None
    - check that invalid date returns None
    """
    # PYTHON: A list comprehension makes a list by stripping each input field.
    parts = [part.strip() for part in raw_item.split(",")]
    if len(parts) != 4:
        return None
    date, description, amount_text, category = parts
    if not _is_valid_date_text(date):
        return None
    try:
        float(amount_text)
    except ValueError:
        return None
    return date, description, amount_text, category


def _is_valid_date_text(date_text):
    """Validate supported date formats used in the app.

    Parameters:
    - date_text (str): Date text to validate

    Returns:
    - bool: True when date is valid in supported formats

    Tests:
    - check that DD/MM/YY dates are accepted
    - check that YYYY-MM-DD dates are accepted
    - check that invalid dates are rejected
    """
    for date_format in ("%d/%m/%y", "%Y-%m-%d"):
        try:
            datetime.strptime(date_text, date_format)
            return True
        except ValueError:
            continue
    return False


def _create_expense_dict(date, description, amount, category, expenses):
    """Create an expense dictionary with auto-generated ID.

    Parameters:
    - date (str): Expense date
    - description (str): Expense description
    - amount (str | float): Expense amount; keep its original representation
    - category (str): Expense category
    - expenses (list): Existing expenses list

    Returns:
    - dict: Expense dictionary

    Tests:
    - check that all fields are included
    - check that ID is correctly assigned
    - check that amount type is preserved
    """
    return {
        "id": str(get_next_id(expenses)),
        "date": date,
        "description": description,
        "amount": amount,
        "category": category
    }


# save_expenses
def save_expenses(expenses, filename):
    """Save all expenses to CSV file.

    Parameters:
    - expenses (list): List of expense dictionaries
    - filename (str): Path to the CSV file

    Returns:
    - bool: True on success, False on a file I/O error; programming errors propagate

    Tests:
    - check that file is created with correct format
    - check that all expenses are written correctly
    - check that header line is included
    - check that amount text is preserved in the file
    - check that CSV quoting survives loading and saving
    - check that I/O errors return False with a message
    - check that unexpected programming errors are not hidden
    """
    try:
        with open(filename, "w") as f:
            # PYTHON: DictWriter writes named fields and quotes commas and quotes correctly.
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(expenses)
        print(PROMPTS["expenses_saved"])
        return True
    except OSError:
        print(PROMPTS["save_failed"])
        return False


def get_valid_yes_no(prompt):
    """Prompt user for yes/no response.

    Parameters:
    - prompt (str): The prompt to display

    Returns:
    - bool: True for 'yes', False for 'no'; EOFError propagates to main

    Tests:
    - check that 'yes' returns True
    - check that 'no' returns False
    - check that case-insensitive input works
    - check that invalid input is rejected with re-prompt
    - check that EOF propagates without retrying
    """
    while True:
        response = input(prompt).lower()
        # PYTHON: Tuple membership test checks multiple accepted values concisely.
        if response in ("yes", "y"):
            return True
        elif response in ("no", "n"):
            return False
        else:
            print(PROMPTS["invalid_yes_no"])


def get_next_id(expenses):
    """Get the next ID for a new expense.

    Parameters:
    - expenses (list): List of expense dictionaries

    Returns:
    - int: Next ID number

    Tests:
    - check that ID is 1 for empty list
    - check that ID increments correctly for existing expenses
    """
    if not expenses:
        return 1
    # PYTHON: A generator supplies converted IDs to max without a temporary list.
    return max(int(expense["id"]) for expense in expenses) + 1


# main
def main():
    """Run the menu, returning cleanly on exit or EOF from any input operation.

    Parameters:
    - None

    Returns:
    - None

    Tests:
    - check that menu is displayed repeatedly
    - check that all menu options work
    - check that invalid choices are handled
    - check that exit terminates the program
    - check that EOF at startup, the menu or a nested operation exits cleanly
    """
    try:
        filename = "expenses.csv"
        expenses = load_or_create_expenses(filename)

        while True:
            print(PROMPTS["menu_title"])
            print(PROMPTS["menu_options"])
            choice = input(PROMPTS["menu_choice"])
            if not _handle_menu_choice(choice, expenses, filename):
                return
    except EOFError:
        return


def _handle_menu_choice(choice, expenses, filename):
    """Handle a menu choice and execute corresponding action.

    Parameters:
    - choice (str): User's menu choice
    - expenses (list): List of expense dictionaries
    - filename (str): Path to expenses CSV file

    Returns:
    - bool: False if user chose to exit, True otherwise

    Tests:
    - check that each menu choice executes correct function
    - check that exit returns False
    - check that invalid choice shows error message
    """
    if choice == "5":
        return False
    if choice == "1":
        display_expenses(expenses)
    elif choice == "2":
        _handle_group_choice(expenses)
    elif choice == "3":
        add_expense(expenses)
    elif choice == "4":
        save_expenses(expenses, filename)
    else:
        print(PROMPTS["invalid_choice"])
        return True
    _wait_for_enter()
    return True


def _handle_group_choice(expenses):
    """Prompt for grouping mode; propagate EOF to main if input ends.

    Parameters:
    - expenses (list): List of expense dictionaries

    Returns:
    - None

    Tests:
    - check that 'd' groups by date
    - check that 'c' groups by category
    - check that invalid group input is re-prompted
    - check that EOF propagates without retrying
    """
    while True:
        group_choice = input(PROMPTS["group_prompt"]).strip().lower()
        if group_choice == "d":
            group_expenses(expenses, "date")
            return
        if group_choice == "c":
            group_expenses(expenses, "category")
            return
        print(PROMPTS["invalid_group"])


def _wait_for_enter():
    """Pause until user presses enter, returning immediately on EOF.

    Parameters:
    - None

    Returns:
    - None

    Tests:
    - check that function consumes one input call
    - check that EOF returns without retrying
    """
    try:
        input(PROMPTS["continue_prompt"])
    except EOFError:
        return


# PYTHON: '__name__ == "__main__"' runs main() only when this file is executed directly.
if __name__ == "__main__":
    main()
