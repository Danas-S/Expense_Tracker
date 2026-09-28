"""Personal Expense Tracker

A program to track personal expenses with CSV storage and menu-driven interface.
"""

import csv
import os
from datetime import datetime
# PYTHON: 'from ... import ...' imports a specific symbol directly from a module.
from collections import defaultdict


MENU_DISPLAY = "1"
MENU_GROUP = "2"
MENU_ADD = "3"
MENU_SAVE = "4"
MENU_EXIT = "5"

MENU_ITEMS = [
    (MENU_DISPLAY, "menu_display"),
    (MENU_GROUP, "menu_group"),
    (MENU_ADD, "menu_add"),
    (MENU_SAVE, "menu_save"),
    (MENU_EXIT, "menu_exit"),
]
VALID_MENU_CHOICES = tuple(choice for choice, _ in MENU_ITEMS)



# PYTHON: Dictionary literal maps string keys to prompt messages (dynamic key-value object).
PROMPTS = {
    "menu_display": "Display all expenses",
    "menu_group": "Group expenses",
    "menu_add": "Add new expense",
    "menu_save": "Save expenses to file",
    "menu_exit": "Exit",
    "table_headers": ("Date", "Description", "Amount", "Category"),
    "menu_title": "\n=== Expense Tracker Menu ===",
    "menu_choice": "Enter your choice ({choices}): ",
    "invalid_choice": "Invalid choice. Please enter one of: {choices}.",
    
    "date_prompt": "Enter date (YYYY-MM-DD): ",
    "invalid_date": "Invalid date format. Please use YYYY-MM-DD.",
    "description_prompt": "Enter description: ",
    "amount_prompt": "Enter amount: ",
    "invalid_amount": "Invalid amount. Please enter a valid number.",
    "category_prompt": "Enter category: ",
    "item_prompt": "Enter expense as date,description,amount,category (or '<' to cancel): ",
    "invalid_item": "Invalid format. Use date,description,amount,category.",
    "group_prompt": "Group by date (d) or category (c)? ",
    "invalid_group": "Invalid choice. Enter 'd' or 'c'.",
    "continue_prompt": "",
    "cancel_prompt": " (or type 'cancel' to go back): ",
    
    "expense_added": "Expense added successfully!",
    "no_expenses": "No expenses found.",
    "file_created": "Created new expenses.csv file.",
    "header_mismatch": "Existing expenses.csv has incorrect format.",
    "overwrite_prompt": "Do you want to overwrite it? (yes/no): ",
    "invalid_yes_no": "Please enter 'yes' or 'no'.",
    "file_overwritten": "File overwritten.",
    "file_not_overwritten": "File not overwritten. Stopping the tracker.",
    "expenses_saved": "Expenses saved to file.",
}


# prompt: Load expenses from CSV, creating a new file with the expected header when needed.
def load_or_create_expenses(filename):
    """Load expenses from CSV file or create new file if it doesn't exist.
    
    Parameters:
    - filename (str): Path to the CSV file
    
    Returns:
    - list | None: Loaded expenses, or None when overwrite is declined
    
    Tests:
    - check that successful loading returns a list
    - check that a declined overwrite returns None
    - check that file is created if it doesn't exist
    - check that header line is correctly written
    - check that data is loaded if valid file exists
    - check that user is prompted for overwrite if header is missing
    - check that file is not modified if user declines overwrite
    """
    expected_header = "id,date,description,amount,category"
    with open(filename, "a+") as f:
        f.seek(0)
        first_line = f.readline().strip()
    if not first_line:
        _create_csv_file(filename, expected_header)
        return []
    return _load_or_validate_file(filename, expected_header)


# prompt: Create a CSV file with the provided header and show create/overwrite status.
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
    # PYTHON: 'with open(...) as ...' is a context manager that auto-closes the file.
    with open(filename, "w", newline="") as f:
        f.write(header + "\n")
    msg = "file_overwritten" if is_overwrite else "file_created"
    print(PROMPTS[msg])


# prompt: Return None when overwrite is declined so main owns the exit decision.
def _load_or_validate_file(filename, expected_header):
    """Validate CSV header and load data or recreate file.
    
    Parameters:
    - filename (str): Path to the CSV file
    - expected_header (str): Expected header line
    
    Returns:
    - list | None: Loaded expenses, or None when overwrite is declined
    
    Tests:
    - check that valid file is loaded
    - check that invalid header triggers overwrite prompt
    - check that file is recreated if user confirms
    - check that declining preserves the file and returns None without SystemExit
    """
    with open(filename, "r") as f:
        first_line = f.readline().strip()
    
    if first_line != expected_header:
        print(PROMPTS["header_mismatch"])
        if not get_valid_yes_no(PROMPTS["overwrite_prompt"]):
            print(PROMPTS["file_not_overwritten"])
            return None
        _create_csv_file(filename, expected_header, is_overwrite=True)
        return []
    
    expenses = []
    # PYTHON: csv.DictReader yields each CSV row as a dictionary keyed by header names.
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            expenses.append(row)
    return expenses


# prompt: Display expenses using dynamic column widths based on current data instead of fixed literals.
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
    - check that long values remain complete in dynamically sized columns
    """
    if not expenses:
        print(PROMPTS["no_expenses"])
        return
    
    rows = [PROMPTS["table_headers"]]
    for expense in expenses:
        rows.append((expense["date"], expense["description"],
                     f"${float(expense['amount']):.2f}", expense["category"]))
    _print_expense_table(rows)


# prompt: Print complete rows with widths that fit their headers and data.
def _print_expense_table(rows):
    """Print a table sized to its headers and formatted expense rows.

    Parameters:
    - rows (list): Header tuple followed by tuples of four display strings

    Returns:
    - None

    Tests:
    - check that long descriptions and categories are not truncated
    - check that each column fits its heading and every value
    - check that amounts are right-aligned and borders match the table width
    """
    # PYTHON: A list comprehension collects each column's maximum string length.
    widths = [max(len(row[column]) for row in rows) for column in range(4)]
    date_w, desc_w, amount_w, category_w = widths
    border = "=" * (sum(widths) + 3)
    print("\n" + border)
    # PYTHON: enumerate supplies both the position and value while looping.
    for index, row in enumerate(rows):
        print(f"{row[0]:<{date_w}} {row[1]:<{desc_w}} {row[2]:>{amount_w}} {row[3]:<{category_w}}")
        if index == 0:
            print(border)
    print(border + "\n")


# prompt: Group expenses by date or category and print summed totals.
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
    header = group_by.capitalize()
    print(f"{header:<30} {'Total':>15}")
    print("="*50)
    for key in sorted(groups.keys()):
        amount = f"${groups[key]:.2f}"
        print(f"{key:<30} {amount:>15}")
    print("="*50 + "\n")
    
    return dict(groups)


# prompt: Collect one comma-separated expense record from input and append it when valid.
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
        date, description, amount, category = parsed_item
        expenses.append(_create_expense_dict(date, description, amount, category, expenses))
        print(PROMPTS["expense_added"])
        return True



# prompt: Parse and validate a comma-separated expense line.
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



# prompt: Validate date strings against supported app formats.
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



# prompt: Get free-text input for a prompt key with cancel support.
def _get_text_input(prompt_key):
    """Get text input from user with cancel support.
    
    Parameters:
    - prompt_key (str): Key for PROMPTS dictionary
    
    Returns:
    - str: User input or None if cancelled
    
    Tests:
    - check that text input is returned
    - check that cancellation returns None
    - check that prompt is displayed correctly
    """
    user_input = input(PROMPTS[prompt_key] + PROMPTS["cancel_prompt"])
    return None if user_input.lower() == "cancel" else user_input



# prompt: Build a normalized expense dictionary with next sequential ID.
def _create_expense_dict(date, description, amount, category, expenses):
    """Create an expense dictionary with auto-generated ID.
    
    Parameters:
    - date (str): Expense date
    - description (str): Expense description
    - amount (float): Expense amount
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


# prompt: Save all in-memory expense rows to CSV storage.
def save_expenses(expenses, filename):
    """Save all expenses to CSV file.
    
    Parameters:
    - expenses (list): List of expense dictionaries
    - filename (str): Path to the CSV file
    
    Returns:
    - bool: True if save was successful, False otherwise
    
    Tests:
    - check that file is created with correct format
    - check that all expenses are written correctly
    - check that header line is included
    - check that amount is formatted correctly in file
    """
    try:
        # PYTHON: 'try/except' handles runtime errors; broad except catches any exception type.
        with open(filename, "w") as f:
            f.write("id,date,description,amount,category\n")
            for expense in expenses:
                amount_text = str(expense["amount"])
                row = (
                    f"{expense['id']},{expense['date']},{expense['description']},"
                    f"{amount_text},{expense['category']}\n"
                )
                f.write(row)
        print(PROMPTS["expenses_saved"])
        return True
    except Exception:
        return False


# prompt: Re-prompt until a valid date (or cancel) is entered.
def get_valid_date():
    """Prompt user for a valid date in YYYY-MM-DD format.
    
    Parameters:
    - None
    
    Returns:
    - str: Valid date string or None if cancelled
    
    Tests:
    - check that valid dates are accepted
    - check that invalid formats are rejected
    - check that cancellation returns None
    - check that leap years are handled
    """
    while True:
        user_input = input(PROMPTS["date_prompt"] + PROMPTS["cancel_prompt"])
        if user_input.lower() == "cancel":
            return None
        if _is_valid_date_text(user_input):
            return user_input
        else:
            print(PROMPTS["invalid_date"])



# prompt: Re-prompt until a valid numeric amount (or cancel) is entered.
def get_valid_amount():
    """Prompt user for a valid amount number.
    
    Parameters:
    - None
    
    Returns:
    - float: Valid amount or None if cancelled
    
    Tests:
    - check that positive numbers are accepted
    - check that decimal numbers are accepted
    - check that negative numbers are accepted
    - check that non-numeric input is rejected
    - check that cancellation returns None
    """
    while True:
        user_input = input(PROMPTS["amount_prompt"] + PROMPTS["cancel_prompt"])
        if user_input.lower() == "cancel":
            return None
        try:
            return float(user_input)
        except ValueError:
            print(PROMPTS["invalid_amount"])



# prompt: Re-prompt until yes/no input is provided and return as boolean.
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



# prompt: Compute the next expense ID based on existing entries.
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
    return max(int(expense["id"]) for expense in expenses) + 1


# prompt: Build and return the numbered menu text from MENU_ITEMS.
def _build_menu_options_text():
    """Build printable menu options text from menu items.

    Parameters:
    - None

    Returns:
    - str: Formatted menu options text

    Tests:
    - check that all menu items appear in order
    - check that option numbers and labels are formatted consistently
    """
    lines = [f"{choice}. {PROMPTS[label_key]}" for choice, label_key in MENU_ITEMS]
    return "\n" + "\n".join(lines)


# prompt: Build the menu choice input prompt from current valid options.
def _build_menu_choice_prompt():
    """Build a dynamic menu-choice prompt listing valid options.

    Parameters:
    - None

    Returns:
    - str: Prompt text showing valid menu choices

    Tests:
    - check that all valid choices are included in prompt text
    - check that prompt format remains consistent
    """
    choices_text = ", ".join(VALID_MENU_CHOICES)
    return PROMPTS["menu_choice"].format(choices=choices_text)


# prompt: Run the interactive expense tracker loop until user exits.
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
    - check that a declined overwrite exits before entering the menu
    - check that EOF at startup, the menu or a nested operation exits cleanly
    """
    try:
        filename = "expenses.csv"
        expenses = load_or_create_expenses(filename)
        if expenses is None:
            return

        while True:
            print(PROMPTS["menu_title"])
            print(_build_menu_options_text())
            choice = input(_build_menu_choice_prompt())
            if not _handle_menu_choice(choice, expenses, filename):
                return
    except EOFError:
        return


# prompt: Execute behavior for a selected menu option.
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
    if choice == MENU_EXIT:
        return False
    if choice == MENU_DISPLAY:
        display_expenses(expenses)
    elif choice == MENU_GROUP:
        _handle_group_choice(expenses)
    elif choice == MENU_ADD:
        add_expense(expenses)
    elif choice == MENU_SAVE:
        save_expenses(expenses, filename)
    else:
        choices_text = ", ".join(VALID_MENU_CHOICES)
        print(PROMPTS["invalid_choice"].format(choices=choices_text))
        return True
    _wait_for_enter()
    return True


# prompt: Ask for grouping mode and display grouped totals when valid.
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



# prompt: Pause until the user presses enter to continue.
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