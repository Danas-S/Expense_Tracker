"""Unit tests for the Week 9 expenses.py

Tests are based on the test specifications in the docstrings of each function.
"""

import unittest
import os
import csv
import tempfile
from io import StringIO
from unittest.mock import patch, call
import expenses as tracker

from expenses import (
    load_or_create_expenses,
    _create_csv_file,
    _load_or_validate_file,
    display_expenses,
    group_expenses,
    add_expense,
    _create_expense_dict,
    save_expenses,
    get_valid_yes_no,
    get_next_id,
    _handle_menu_choice,
)


class TestLoadOrCreateExpenses(unittest.TestCase):
    """Tests for load_or_create_expenses function"""

    def setUp(self):
        """Create a temporary directory for test files"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_expenses.csv")

    def tearDown(self):
        """Clean up temporary files"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.temp_dir)

    def test_returns_list(self):
        """Check that function returns a list"""
        result = load_or_create_expenses(self.test_file)
        self.assertIsInstance(result, list)

    def test_file_created_if_not_exists(self):
        """Check that file is created if it doesn't exist"""
        self.assertFalse(os.path.exists(self.test_file))
        load_or_create_expenses(self.test_file)
        self.assertTrue(os.path.exists(self.test_file))

    def test_header_correctly_written(self):
        """Check that header line is correctly written"""
        load_or_create_expenses(self.test_file)
        with open(self.test_file, "r") as f:
            first_line = f.readline().strip()
        self.assertEqual(first_line, "id,date,description,amount,category")

    def test_data_loaded_from_valid_file(self):
        """Check that data is loaded if valid file exists"""
        # Create a valid file with data
        with open(self.test_file, "w", newline="") as f:
            f.write("id,date,description,amount,category\n")
            f.write("1,2026-01-01,Groceries,50.00,Food\n")

        result = load_or_create_expenses(self.test_file)
        self.assertEqual(len(result), 1)
        self.assertEqual(result, [{"id": "1", "date": "2026-01-01",
                                   "description": "Groceries", "amount": "50.00",
                                   "category": "Food"}])

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["no"])
    def test_user_prompted_for_overwrite_if_header_missing(self, mock_input, mock_print):
        """Check that user is prompted for overwrite if header is missing"""
        # Create invalid file
        with open(self.test_file, "w") as f:
            f.write("invalid,header\n")

        result = load_or_create_expenses(self.test_file)
        self.assertIsNone(result)
        mock_input.assert_called_once_with(tracker.PROMPTS["overwrite_prompt"])
        self.assertEqual(mock_print.call_args_list,
                         [call(tracker.PROMPTS["header_mismatch"]),
                          call(tracker.PROMPTS["file_not_overwritten"])])

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["no"])
    def test_file_not_modified_if_user_declines_overwrite(self, mock_input, mock_print):
        """Check that file is not modified if user declines overwrite"""
        # Create invalid file
        with open(self.test_file, "w") as f:
            f.write("invalid,header\n")

        load_or_create_expenses(self.test_file)

        # Check file still has invalid header
        with open(self.test_file, "r") as f:
            content = f.read()
        self.assertEqual(content, "invalid,header\n")


class TestCreateCSVFile(unittest.TestCase):
    """Tests for _create_csv_file function"""

    def setUp(self):
        """Create a temporary directory for test files"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test.csv")

    def tearDown(self):
        """Clean up temporary files"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.temp_dir)

    @patch("builtins.print")
    def test_file_created_successfully(self, mock_print):
        """Check that file is created successfully"""
        header = "id,date,description,amount,category"
        _create_csv_file(self.test_file, header)
        self.assertTrue(os.path.exists(self.test_file))

    @patch("builtins.print")
    def test_header_written_correctly(self, mock_print):
        """Check that header is written correctly"""
        header = "id,date,description,amount,category"
        _create_csv_file(self.test_file, header)
        with open(self.test_file, "r") as f:
            first_line = f.readline().strip()
        self.assertEqual(first_line, header)

    @patch("builtins.print")
    def test_appropriate_message_shown(self, mock_print):
        """Check that appropriate message is shown"""
        header = "id,date,description,amount,category"
        _create_csv_file(self.test_file, header, is_overwrite=False)
        mock_print.assert_called_once_with(tracker.PROMPTS["file_created"])


class TestDisplayExpenses(unittest.TestCase):
    """Tests for display_expenses function"""

    @patch("builtins.print")
    def test_table_displayed_correctly(self, mock_print):
        """Check that table is displayed correctly with all columns"""
        expenses = [
            {"date": "2026-01-01", "description": "Groceries", "amount": 50.00, "category": "Food"},
            {"date": "2026-01-02", "description": "Gas", "amount": 40.00, "category": "Transport"}
        ]
        display_expenses(expenses)
        lines = [args[0] for args, _ in mock_print.call_args_list]
        for heading in ("Date", "Description", "Amount", "Category"):
            self.assertIn(heading, lines[1])
        for value in ("2026-01-01", "Groceries", "$50.00", "Food"):
            self.assertIn(value, lines[3])
        for value in ("2026-01-02", "Gas", "$40.00", "Transport"):
            self.assertIn(value, lines[4])

    @patch("builtins.print")
    def test_no_expenses_message(self, mock_print):
        """Check that no expenses shows appropriate message"""
        display_expenses([])
        mock_print.assert_called_once_with(tracker.PROMPTS["no_expenses"])

    @patch("builtins.print")
    def test_amounts_formatted_properly(self, mock_print):
        """Check that amounts are formatted properly"""
        expenses = [
            {"date": "2026-01-01", "description": "Test", "amount": 10.5, "category": "Food"}
        ]
        display_expenses(expenses)
        lines = [args[0] for args, _ in mock_print.call_args_list]
        self.assertIn("$10.50", lines[3])
        self.assertNotIn("$10.500", lines[3])


class TestGroupExpenses(unittest.TestCase):
    """Tests for group_expenses function"""

    @patch("builtins.print")
    def test_grouped_by_date(self, mock_print):
        """Check that expenses are correctly grouped by date"""
        expenses = [
            {"date": "2026-01-01", "description": "Groceries", "amount": 50.00, "category": "Food"},
            {"date": "2026-01-01", "description": "Gas", "amount": 40.00, "category": "Transport"},
            {"date": "2026-01-02", "description": "Movie", "amount": 15.00, "category": "Entertainment"}
        ]
        result = group_expenses(expenses, "date")
        self.assertEqual(result["2026-01-01"], 90.00)
        self.assertEqual(result["2026-01-02"], 15.00)

    @patch("builtins.print")
    def test_grouped_by_category(self, mock_print):
        """Check that expenses are correctly grouped by category"""
        expenses = [
            {"date": "2026-01-01", "description": "Groceries", "amount": 50.00, "category": "Food"},
            {"date": "2026-01-01", "description": "Restaurant", "amount": 30.00, "category": "Food"},
            {"date": "2026-01-02", "description": "Gas", "amount": 40.00, "category": "Transport"}
        ]
        result = group_expenses(expenses, "category")
        self.assertEqual(result["Food"], 80.00)
        self.assertEqual(result["Transport"], 40.00)

    @patch("builtins.print")
    def test_sums_calculated_correctly(self, mock_print):
        """Check that sums are calculated correctly"""
        expenses = [
            {"date": "2026-01-01", "description": "A", "amount": 25.50, "category": "Food"},
            {"date": "2026-01-01", "description": "B", "amount": 74.50, "category": "Food"}
        ]
        result = group_expenses(expenses, "category")
        self.assertEqual(result["Food"], 100.00)

    @patch("builtins.print")
    def test_results_displayed_in_table_format(self, mock_print):
        """Check that results are displayed in table format"""
        expenses = [
            {"date": "2026-01-01", "description": "Test", "amount": 50.00, "category": "Food"}
        ]
        self.assertEqual(group_expenses(expenses, "category"), {"Food": 50.0})
        lines = [args[0] for args, _ in mock_print.call_args_list]
        self.assertEqual(lines[1].split(), ["Category", "Total"])
        self.assertEqual(lines[3].split(), ["Food", "$50.00"])
        self.assertEqual(lines[0].strip(), "=" * 50)
        self.assertEqual(lines[-1].strip(), "=" * 50)

    @patch("builtins.print")
    def test_no_expenses_message(self, mock_print):
        """Check that no expenses shows appropriate message"""
        self.assertEqual(group_expenses([], "date"), {})
        mock_print.assert_called_once_with(tracker.PROMPTS["no_expenses"])


class TestGetValidYesNo(unittest.TestCase):
    """Tests for get_valid_yes_no function"""

    @patch("builtins.input", side_effect=["yes"])
    def test_yes_returns_true(self, mock_input):
        """Check that 'yes' returns True"""
        result = get_valid_yes_no("Proceed?")
        self.assertTrue(result)

    @patch("builtins.input", side_effect=["no"])
    def test_no_returns_false(self, mock_input):
        """Check that 'no' returns False"""
        result = get_valid_yes_no("Proceed?")
        self.assertFalse(result)

    @patch("builtins.input", side_effect=["YES"])
    def test_case_insensitive_yes(self, mock_input):
        """Check that case-insensitive input works"""
        result = get_valid_yes_no("Proceed?")
        self.assertTrue(result)

    @patch("builtins.input", side_effect=["invalid", "yes"])
    @patch("builtins.print")
    def test_invalid_input_rejected(self, mock_print, mock_input):
        """Check that invalid input is rejected with re-prompt"""
        result = get_valid_yes_no("Proceed?")
        self.assertTrue(result)
        mock_print.assert_called_once_with(tracker.PROMPTS["invalid_yes_no"])
        self.assertEqual(mock_input.call_args_list, [call("Proceed?"), call("Proceed?")])

    @patch("builtins.input", side_effect=["y"])
    def test_y_returns_true(self, mock_input):
        """Check that 'y' returns True"""
        result = get_valid_yes_no("Proceed?")
        self.assertTrue(result)

    @patch("builtins.input", side_effect=["n"])
    def test_n_returns_false(self, mock_input):
        """Check that 'n' returns False"""
        result = get_valid_yes_no("Proceed?")
        self.assertFalse(result)


class TestGetNextId(unittest.TestCase):
    """Tests for get_next_id function"""

    def test_id_is_one_for_empty_list(self):
        """Check that ID is 1 for empty list"""
        result = get_next_id([])
        self.assertEqual(result, 1)

    def test_id_increments_correctly(self):
        """Check that ID increments correctly for existing expenses"""
        expenses = [
            {"id": "1", "date": "2026-01-01", "description": "Test", "amount": 50.00, "category": "Food"},
            {"id": "2", "date": "2026-01-02", "description": "Test", "amount": 50.00, "category": "Food"},
            {"id": "3", "date": "2026-01-03", "description": "Test", "amount": 50.00, "category": "Food"}
        ]
        result = get_next_id(expenses)
        self.assertEqual(result, 4)


class TestCreateExpenseDict(unittest.TestCase):
    """Tests for _create_expense_dict function"""

    def test_all_fields_included(self):
        """Check that all fields are included"""
        result = _create_expense_dict("2026-01-01", "Groceries", 50.00, "Food", [])
        self.assertIn("id", result)
        self.assertIn("date", result)
        self.assertIn("description", result)
        self.assertIn("amount", result)
        self.assertIn("category", result)

    def test_id_correctly_assigned(self):
        """Check that ID is correctly assigned"""
        expenses = [{"id": "1", "date": "2026-01-01", "description": "Test", "amount": 50.00, "category": "Food"}]
        result = _create_expense_dict("2026-01-02", "Test", 50.00, "Food", expenses)
        self.assertEqual(result["id"], "2")

    def test_amount_type_preserved(self):
        """Check that amount type is preserved"""
        result = _create_expense_dict("2026-01-01", "Test", 50.00, "Food", [])
        self.assertIsInstance(result["amount"], float)


class TestAddExpense(unittest.TestCase):
    """Tests for the current one-line expense interface."""

    @patch("builtins.input", side_effect=["2026-01-15,Groceries,50.00,Food"])
    @patch("builtins.print")
    def test_valid_expense_added(self, mock_print, mock_input):
        """A single input collects every field and preserves the amount text."""
        expenses = []
        self.assertTrue(add_expense(expenses))
        self.assertEqual(expenses, [{"id": "1", "date": "2026-01-15",
                                    "description": "Groceries", "amount": "50.00",
                                    "category": "Food"}])
        mock_input.assert_called_once_with(tracker.PROMPTS["item_prompt"])
        mock_print.assert_called_once_with(tracker.PROMPTS["expense_added"])

    @patch("builtins.input", side_effect=["<"])
    def test_cancellation_handled(self, mock_input):
        """The '<' cancellation leaves existing records unchanged."""
        expenses = [{"id": "1", "description": "Existing"}]
        original = [dict(expenses[0])]
        self.assertFalse(add_expense(expenses))
        self.assertEqual(expenses, original)
        mock_input.assert_called_once_with(tracker.PROMPTS["item_prompt"])

    @patch("builtins.input", side_effect=["invalid", "2026-01-15,Groceries,50.00,Food"])
    @patch("builtins.print")
    def test_invalid_inputs_rejected(self, mock_print, mock_input):
        """Invalid input is rejected once, then the valid record is added."""
        expenses = []
        self.assertTrue(add_expense(expenses))
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0]["description"], "Groceries")
        self.assertEqual(mock_input.call_count, 2)
        self.assertEqual(mock_print.call_args_list,
                         [call(tracker.PROMPTS["invalid_item"]),
                          call(tracker.PROMPTS["expense_added"])])

    @patch("builtins.input", side_effect=["2026-01-15,Groceries,50.00,Food"])
    @patch("builtins.print")
    def test_id_correctly_assigned(self, mock_print, mock_input):
        """An existing ID of 1 gives the next item ID 2."""
        expenses = [{"id": "1", "date": "2026-01-01", "description": "Test",
                     "amount": "10", "category": "Food"}]
        self.assertTrue(add_expense(expenses))
        self.assertEqual(len(expenses), 2)
        self.assertEqual(expenses[1]["id"], "2")
        mock_input.assert_called_once_with(tracker.PROMPTS["item_prompt"])

    @patch("builtins.input", side_effect=EOFError)
    def test_eof_cancels_expense(self, mock_input):
        """EOF cancels once without changing existing records."""
        expenses = [{"id": "1"}]
        self.assertFalse(add_expense(expenses))
        self.assertEqual(expenses, [{"id": "1"}])
        mock_input.assert_called_once_with(tracker.PROMPTS["item_prompt"])

    @patch("builtins.input", side_effect=["invalid", EOFError])
    @patch("builtins.print")
    def test_invalid_then_eof_cancels(self, mock_print, mock_input):
        """An exhausted input sequence cancels after the validation message."""
        expenses = []
        self.assertFalse(add_expense(expenses))
        self.assertEqual(expenses, [])
        self.assertEqual(mock_input.call_count, 2)
        mock_print.assert_called_once_with(tracker.PROMPTS["invalid_item"])


class TestSaveExpenses(unittest.TestCase):
    """Tests for save_expenses function"""

    def setUp(self):
        """Create a temporary directory for test files"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_expenses.csv")

    def tearDown(self):
        """Clean up temporary files"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.temp_dir)

    @patch("builtins.print")
    def test_file_created_with_correct_format(self, mock_print):
        """Check that file is created with correct format"""
        expenses = [
            {"id": "1", "date": "2026-01-01", "description": "Groceries", "amount": 50.00, "category": "Food"}
        ]
        result = save_expenses(expenses, self.test_file)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_file))

    @patch("builtins.print")
    def test_all_expenses_written_correctly(self, mock_print):
        """Check that all expenses are written correctly"""
        expenses = [
            {"id": "1", "date": "2026-01-01", "description": "Groceries", "amount": 50.00, "category": "Food"},
            {"id": "2", "date": "2026-01-02", "description": "Gas", "amount": 40.00, "category": "Transport"}
        ]
        save_expenses(expenses, self.test_file)

        with open(self.test_file, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        self.assertEqual(rows, [
            {"id": "1", "date": "2026-01-01", "description": "Groceries",
             "amount": "50.0", "category": "Food"},
            {"id": "2", "date": "2026-01-02", "description": "Gas",
             "amount": "40.0", "category": "Transport"}])
        mock_print.assert_called_once_with(tracker.PROMPTS["expenses_saved"])

    @patch("builtins.print")
    def test_header_line_included(self, mock_print):
        """Check that header line is included"""
        expenses = [
            {"id": "1", "date": "2026-01-01", "description": "Test", "amount": 50.00, "category": "Food"}
        ]
        save_expenses(expenses, self.test_file)

        with open(self.test_file, "r") as f:
            first_line = f.readline().strip()
        self.assertEqual(first_line, "id,date,description,amount,category")

    @patch("builtins.print")
    def test_amount_formatted_correctly_in_file(self, mock_print):
        """Check that amount is formatted correctly in file"""
        expenses = [
            {"id": "1", "date": "2026-01-01", "description": "Test", "amount": 50.50, "category": "Food"}
        ]
        save_expenses(expenses, self.test_file)

        with open(self.test_file, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        self.assertEqual(rows[0]["amount"], "50.5")


class TestHandleMenuChoice(unittest.TestCase):
    """Isolate menu dispatch from terminal input and file I/O."""

    def setUp(self):
        """Patch collaborators so no menu test can wait on real input."""
        self.expenses = []
        self.filename = "test_expenses.csv"
        self.actions = {}
        for name in ("display_expenses", "_handle_group_choice", "add_expense",
                     "save_expenses", "_wait_for_enter"):
            patcher = patch("expenses." + name)
            self.actions[name] = patcher.start()
            self.addCleanup(patcher.stop)

    def check_action(self, choice, name, *args):
        """Assert exact dispatch, one pause, and no unrelated operation."""
        self.assertTrue(_handle_menu_choice(choice, self.expenses, self.filename))
        self.actions[name].assert_called_once_with(*args)
        self.actions["_wait_for_enter"].assert_called_once_with()
        for other_name, mock in self.actions.items():
            if other_name not in (name, "_wait_for_enter"):
                mock.assert_not_called()

    def test_menu_choice_1_displays_expenses(self):
        """Option 1 displays the current list."""
        self.check_action("1", "display_expenses", self.expenses)

    def test_menu_choice_2_opens_group_menu(self):
        """Option 2 lets the grouping helper choose date or category."""
        self.check_action("2", "_handle_group_choice", self.expenses)

    def test_menu_choice_3_adds_expense(self):
        """Option 3 adds an expense."""
        self.check_action("3", "add_expense", self.expenses)

    def test_menu_choice_4_saves_expenses(self):
        """Option 4 saves the list to the selected file."""
        self.check_action("4", "save_expenses", self.expenses, self.filename)

    def test_menu_choice_5_returns_false(self):
        """Option 5 exits without another action or pause."""
        self.assertFalse(_handle_menu_choice("5", self.expenses, self.filename))
        for mock in self.actions.values():
            mock.assert_not_called()

    @patch("builtins.print")
    def test_invalid_choice_shows_error(self, mock_print):
        """Option 6 is invalid and keeps the menu running."""
        self.assertTrue(_handle_menu_choice("6", self.expenses, self.filename))
        mock_print.assert_called_once_with(tracker.PROMPTS["invalid_choice"].format(choices=", ".join(tracker.VALID_MENU_CHOICES)))
        for mock in self.actions.values():
            mock.assert_not_called()


class TestParsing(unittest.TestCase):
    """Exercise the current parser instead of separate field-input prompts."""

    def test_valid_line_and_amount_text(self):
        """Both supported date forms and numeric forms preserve entered text."""
        for date in ("15/01/26", "2026-01-15"):
            for amount in ("50", "50.00", "-25.50", "0"):
                with self.subTest(date=date, amount=amount):
                    self.assertEqual(tracker._parse_expense_line(
                        f"{date},Groceries,{amount},Food"),
                        (date, "Groceries", amount, "Food"))

    def test_spaces_stripped(self):
        """Spaces around all four values are stripped."""
        self.assertEqual(tracker._parse_expense_line(
            " 2026-01-15 , Groceries , 50.00 , Food "),
            ("2026-01-15", "Groceries", "50.00", "Food"))

    def test_invalid_lines(self):
        """Wrong field counts, invalid amounts and invalid dates return None."""
        for raw in ("", "invalid", "2026-01-15,Tea,2", "2026-01-15,Tea,2,Food,extra",
                    "2026-01-15,Tea,abc,Food", "2026-02-30,Tea,2,Food",
                    "bad,Tea,2,Food"):
            with self.subTest(raw=raw):
                self.assertIsNone(tracker._parse_expense_line(raw))

    def test_supported_dates_and_leap_years(self):
        """Real dates in either supported format are accepted."""
        for date in ("2026-01-15", "15/01/26", "2024-02-29", "29/02/24"):
            with self.subTest(date=date):
                self.assertTrue(tracker._is_valid_date_text(date))
        for date in ("2026-02-29", "31/04/26", "2026/01/15", "nonsense", ""):
            with self.subTest(date=date):
                self.assertFalse(tracker._is_valid_date_text(date))

    def test_unsorted_ids_continue_after_maximum(self):
        """IDs continue from the largest existing ID even when rows have gaps."""
        self.assertEqual(get_next_id([{"id": "10"}, {"id": "2"}, {"id": "5"}]), 11)

    def test_create_dict_preserves_string_amount(self):
        """Creating a record preserves amount text and every named field."""
        self.assertEqual(_create_expense_dict("2026-01-15", "Tea", "2.00", "Food", []),
                         {"id": "1", "date": "2026-01-15", "description": "Tea",
                          "amount": "2.00", "category": "Food"})


class TestGroupChoice(unittest.TestCase):
    """The grouping submenu validates its own choices."""

    @patch("expenses.group_expenses")
    def test_date_and_category_routes(self, mock_group):
        """Date and category are selected inside the submenu."""
        expenses = [{"id": "1"}]
        for choice, key in (("d", "date"), ("c", "category"), (" C ", "category")):
            with self.subTest(choice=choice), patch("builtins.input", side_effect=[choice]) as mock_input:
                tracker._handle_group_choice(expenses)
                mock_group.assert_called_once_with(expenses, key)
                mock_input.assert_called_once_with(tracker.PROMPTS["group_prompt"])
                mock_group.reset_mock()

    @patch("expenses.group_expenses")
    @patch("builtins.input", side_effect=["wrong", "d"])
    @patch("builtins.print")
    def test_invalid_group_reprompts(self, mock_print, mock_input, mock_group):
        """Invalid submenu input prints an error before accepting a valid choice."""
        tracker._handle_group_choice([])
        mock_group.assert_called_once_with([], "date")
        mock_print.assert_called_once_with(tracker.PROMPTS["invalid_group"])
        self.assertEqual(mock_input.call_count, 2)


class TestFileRoundTrip(unittest.TestCase):
    """Real temporary files check loading, overwriting and saving new items."""

    def setUp(self):
        """Keep test files outside the project's expenses.csv."""
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.filename = os.path.join(directory.name, "expenses.csv")
        self.header = "id,date,description,amount,category"

    @patch("builtins.print")
    def test_empty_file_receives_header(self, mock_print):
        """An empty file is initialised just like a missing file."""
        with open(self.filename, "w"):
            pass
        self.assertEqual(load_or_create_expenses(self.filename), [])
        with open(self.filename) as handle:
            self.assertEqual(handle.read(), self.header + "\n")
        mock_print.assert_called_once_with(tracker.PROMPTS["file_created"])

    @patch("builtins.input", side_effect=["yes"])
    @patch("builtins.print")
    def test_helper_overwrites_invalid_header(self, mock_print, mock_input):
        """The validation helper replaces an invalid file only after consent."""
        with open(self.filename, "w") as handle:
            handle.write("invalid,header\n")
        self.assertEqual(_load_or_validate_file(self.filename, self.header), [])
        with open(self.filename) as handle:
            self.assertEqual(handle.read(), self.header + "\n")
        mock_input.assert_called_once_with(tracker.PROMPTS["overwrite_prompt"])
        self.assertEqual(mock_print.call_args_list,
                         [call(tracker.PROMPTS["header_mismatch"]),
                          call(tracker.PROMPTS["file_overwritten"])])

    @patch("builtins.input", side_effect=["2026-01-15,Groceries,50.00,Food"])
    @patch("builtins.print")
    def test_load_add_save_reload(self, mock_print, mock_input):
        """Loaded rows survive saving alongside a newly entered row."""
        original = self.header + "\n1,01/01/26,Tea,2,Food\n"
        with open(self.filename, "w") as handle:
            handle.write(original)
        expenses = _load_or_validate_file(self.filename, self.header)
        self.assertEqual(expenses, [{"id": "1", "date": "01/01/26",
                                    "description": "Tea", "amount": "2", "category": "Food"}])
        self.assertTrue(add_expense(expenses))
        with open(self.filename) as handle:
            self.assertEqual(handle.read(), original)
        self.assertTrue(save_expenses(expenses, self.filename))
        with open(self.filename) as handle:
            self.assertEqual(handle.read(), original + "2,2026-01-15,Groceries,50.00,Food\n")
        self.assertEqual(load_or_create_expenses(self.filename), expenses)

    @patch("builtins.print")
    def test_save_empty_list_writes_header(self, mock_print):
        """Saving no expenses still writes a valid header."""
        self.assertTrue(save_expenses([], self.filename))
        with open(self.filename) as handle:
            self.assertEqual(handle.read(), self.header + "\n")

    @patch("builtins.print")
    def test_csv_quoting_survives_load_and_save(self, mock_print):
        """Saving a loaded CSV preserves descriptions containing commas and quotes."""
        text = self.header + '\n1,2026-01-15,"Tea, ""large""",2.00,Food\n'
        with open(self.filename, "w") as handle:
            handle.write(text)
        expenses = load_or_create_expenses(self.filename)
        self.assertEqual(expenses[0]["description"], 'Tea, "large"')
        self.assertTrue(save_expenses(expenses, self.filename))
        self.assertEqual(load_or_create_expenses(self.filename), expenses)
        with open(self.filename) as handle:
            self.assertEqual(handle.read(), text)

    @patch("builtins.open", side_effect=PermissionError("read-only location"))
    @patch("builtins.print")
    def test_save_io_error_returns_false(self, mock_print, mock_open):
        """A file error gives a useful message and a False return value."""
        self.assertFalse(save_expenses([], self.filename))
        mock_open.assert_called_once_with(self.filename, "w")
        mock_print.assert_called_once_with(tracker.PROMPTS["save_failed"])

    @patch("builtins.open", side_effect=RuntimeError("unexpected bug"))
    def test_save_does_not_hide_programming_errors(self, mock_open):
        """Unexpected errors propagate instead of being reported as a failed save."""
        with self.assertRaisesRegex(RuntimeError, "unexpected bug"):
            save_expenses([], self.filename)
        mock_open.assert_called_once_with(self.filename, "w")


class TestMainMenu(unittest.TestCase):
    """Check menu repetition with invalid input and a successful operation."""

    @patch("expenses.load_or_create_expenses", return_value=[])
    @patch("expenses.display_expenses")
    @patch("expenses._wait_for_enter")
    @patch("builtins.input", side_effect=["6", "1", "5"])
    @patch("builtins.print")
    def test_repeats_after_invalid_and_valid_choices(self, mock_print, mock_input,
                                                   mock_pause, mock_display, mock_load):
        """An invalid option and a display both return to the five-option menu."""
        self.assertIsNone(tracker.main())
        mock_display.assert_called_once_with([])
        mock_pause.assert_called_once_with()
        mock_load.assert_called_once_with("expenses.csv")
        self.assertEqual(mock_input.call_count, 3)
        self.assertEqual(mock_print.call_args_list.count(call(tracker.PROMPTS["menu_title"])), 3)
        mock_print.assert_any_call(tracker.PROMPTS["invalid_choice"].format(choices=", ".join(tracker.VALID_MENU_CHOICES)))


class TestEndOfInput(unittest.TestCase):
    """EOF is handled at operation and application boundaries."""

    @patch("builtins.input", side_effect=[""])
    def test_pause_consumes_one_input(self, mock_input):
        """Normal Enter returns after a single input call."""
        self.assertIsNone(tracker._wait_for_enter())
        mock_input.assert_called_once_with(tracker.PROMPTS["continue_prompt"])

    @patch("builtins.input", side_effect=EOFError)
    def test_pause_eof_returns(self, mock_input):
        """A pause never retries exhausted input."""
        self.assertIsNone(tracker._wait_for_enter())
        mock_input.assert_called_once_with(tracker.PROMPTS["continue_prompt"])

    @patch("builtins.input", side_effect=EOFError)
    def test_group_eof_propagates(self, mock_input):
        """The grouping helper leaves the application-exit decision to main."""
        with self.assertRaises(EOFError):
            tracker._handle_group_choice([])
        mock_input.assert_called_once_with(tracker.PROMPTS["group_prompt"])

    @patch("builtins.input", side_effect=EOFError)
    def test_yes_no_eof_propagates(self, mock_input):
        """EOF is not interpreted as permission to overwrite a file."""
        with self.assertRaises(EOFError):
            get_valid_yes_no("Overwrite?")
        mock_input.assert_called_once_with("Overwrite?")

    @patch("expenses.load_or_create_expenses", return_value=[])
    @patch("builtins.print")
    def test_main_menu_and_nested_eof_exit(self, mock_print, mock_load):
        """Menu, grouping, adding and display pauses all stop with exhausted stdin."""
        for text in ("", "2\n", "3\n", "1\n", "6\n"):
            with self.subTest(text=text), patch("sys.stdin", StringIO(text)):
                self.assertIsNone(tracker.main())
        self.assertEqual(mock_load.call_args_list, [call("expenses.csv")] * 5)

    @patch("builtins.input", side_effect=EOFError)
    @patch("builtins.print")
    def test_main_startup_eof_preserves_invalid_file(self, mock_print, mock_input):
        """EOF at overwrite confirmation exits before displaying the main menu."""
        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "invalid.csv")
            with open(filename, "w") as handle:
                handle.write("wrong,header\n")
            with patch("expenses.load_or_create_expenses",
                       side_effect=lambda name: load_or_create_expenses(filename)):
                self.assertIsNone(tracker.main())
            with open(filename) as handle:
                self.assertEqual(handle.read(), "wrong,header\n")
        mock_input.assert_called_once_with(tracker.PROMPTS["overwrite_prompt"])
        self.assertNotIn(call(tracker.PROMPTS["menu_title"]), mock_print.call_args_list)

    @patch("expenses.load_or_create_expenses", return_value=[])
    @patch("builtins.input", side_effect=["5"])
    @patch("builtins.print")
    def test_main_exit_option(self, mock_print, mock_input, mock_load):
        """Main exits normally with one menu selection."""
        self.assertIsNone(tracker.main())
        mock_load.assert_called_once_with("expenses.csv")
        self.assertEqual(mock_input.call_count, 1)
        self.assertIn(call(tracker.PROMPTS["menu_title"]), mock_print.call_args_list)


class TestWeek9FileValidation(unittest.TestCase):
    """Declining overwrite reports a status to main without exiting in a helper."""

    def setUp(self):
        """Create an invalid CSV without using the real expenses file."""
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.filename = os.path.join(directory.name, "invalid.csv")
        self.header = "id,date,description,amount,category"
        with open(self.filename, "w") as handle:
            handle.write("wrong,header\nkeep,this\n")

    @patch("builtins.input", side_effect=["no"])
    @patch("builtins.print")
    def test_helper_decline_returns_none(self, mock_print, mock_input):
        """The helper detects the header, returns None and preserves every byte."""
        with open(self.filename, "rb") as handle:
            before = handle.read()
        self.assertIsNone(tracker._load_or_validate_file(self.filename, self.header))
        with open(self.filename, "rb") as handle:
            self.assertEqual(handle.read(), before)
        mock_input.assert_called_once_with(tracker.PROMPTS["overwrite_prompt"])
        self.assertEqual(mock_print.call_args_list,
                         [call(tracker.PROMPTS["header_mismatch"]),
                          call(tracker.PROMPTS["file_not_overwritten"])])

    @patch("builtins.input", side_effect=["no"])
    @patch("builtins.print")
    def test_loader_propagates_none(self, mock_print, mock_input):
        """The public loader passes the declined-overwrite status to its caller."""
        self.assertIsNone(tracker.load_or_create_expenses(self.filename))
        mock_input.assert_called_once_with(tracker.PROMPTS["overwrite_prompt"])

    @patch("builtins.input", side_effect=["no"])
    @patch("builtins.print")
    def test_main_decline_exits_before_menu(self, mock_print, mock_input):
        """A real invalid header and 'no' reach main's clean-exit decision."""
        loader = tracker.load_or_create_expenses
        with patch("expenses.load_or_create_expenses",
                   side_effect=lambda name: loader(self.filename)) as mock_load:
            with patch("expenses._handle_menu_choice") as mock_menu:
                self.assertIsNone(tracker.main())
        mock_load.assert_called_once_with("expenses.csv")
        mock_menu.assert_not_called()
        mock_input.assert_called_once_with(tracker.PROMPTS["overwrite_prompt"])
        self.assertNotIn(call(tracker.PROMPTS["menu_title"]), mock_print.call_args_list)
        with open(self.filename) as handle:
            self.assertEqual(handle.read(), "wrong,header\nkeep,this\n")

    @patch("builtins.input", side_effect=["yes"])
    @patch("builtins.print")
    def test_confirm_overwrites_with_header(self, mock_print, mock_input):
        """Consent recreates the invalid file and returns an ordinary empty list."""
        self.assertEqual(tracker.load_or_create_expenses(self.filename), [])
        with open(self.filename) as handle:
            self.assertEqual(handle.read(), self.header + "\n")
        mock_input.assert_called_once_with(tracker.PROMPTS["overwrite_prompt"])
        mock_print.assert_any_call(tracker.PROMPTS["file_overwritten"])

    @patch("builtins.input", side_effect=["yes", "5"])
    @patch("builtins.print")
    def test_main_confirm_continues_to_menu(self, mock_print, mock_input):
        """An empty list after overwrite is a successful load, not a stop status."""
        loader = tracker.load_or_create_expenses
        with patch("expenses.load_or_create_expenses",
                   side_effect=lambda name: loader(self.filename)):
            self.assertIsNone(tracker.main())
        self.assertEqual(mock_input.call_count, 2)
        mock_print.assert_any_call(tracker.PROMPTS["menu_title"])


class TestWeek9Menu(unittest.TestCase):
    """Menu text and valid-choice messages use the shared configuration."""

    def test_numbered_labels_in_order(self):
        """The displayed interface keeps exactly the five required operations."""
        self.assertEqual(tracker._build_menu_options_text(),
                         "\n1. Display all expenses\n2. Group expenses"
                         "\n3. Add new expense\n4. Save expenses to file\n5. Exit")
        self.assertEqual(tracker.VALID_MENU_CHOICES, ("1", "2", "3", "4", "5"))
        self.assertEqual(tracker.VALID_MENU_CHOICES,
                         tuple(choice for choice, _ in tracker.MENU_ITEMS))

    def test_labels_are_read_from_prompt_dictionary(self):
        """Changing a configured label changes the rendered menu text."""
        with patch.dict(tracker.PROMPTS, {"menu_display": "Show entries"}):
            self.assertEqual(tracker._build_menu_options_text().splitlines()[1],
                             "1. Show entries")
        for _, label_key in tracker.MENU_ITEMS:
            self.assertIn(label_key, tracker.PROMPTS)

    def test_menu_items_control_order_and_number(self):
        """Menu generation reads the configured item pairs, not a fixed string."""
        with patch("expenses.MENU_ITEMS", [("7", "menu_exit"), ("2", "menu_group")]):
            self.assertEqual(tracker._build_menu_options_text(),
                             "\n7. Exit\n2. Group expenses")

    @patch("builtins.print")
    def test_prompt_and_error_follow_valid_choices(self, mock_print):
        """Choice prompt and invalid-choice message share the configured choices."""
        self.assertEqual(tracker._build_menu_choice_prompt(),
                         "Enter your choice (1, 2, 3, 4, 5): ")
        with patch("expenses.VALID_MENU_CHOICES", ("1", "7")):
            self.assertEqual(tracker._build_menu_choice_prompt(),
                             "Enter your choice (1, 7): ")
            self.assertTrue(tracker._handle_menu_choice("6", [], "unused.csv"))
        mock_print.assert_called_once_with("Invalid choice. Please enter one of: 1, 7.")


class TestWeek9Table(unittest.TestCase):
    """Wide values remain complete and every table column stays aligned."""

    def test_dynamic_widths_and_amount_alignment(self):
        """Long text and a large amount expand the table without truncation."""
        description = "A description longer than the old twenty character column"
        category = "A category longer than fifteen characters"
        records = [
            {"date": "2026-01-15", "description": description,
             "amount": "1234567890123.5", "category": category},
            {"date": "15/01/26", "description": "Tea", "amount": "2", "category": "Food"},
        ]
        with patch("sys.stdout", new_callable=StringIO) as output:
            tracker.display_expenses(records)
        lines = output.getvalue().strip("\n").splitlines()
        widths = (10, len(description), len("$1234567890123.50"), len(category))
        self.assertEqual(len(lines), 6)
        for index in (0, 2, 5):
            self.assertEqual(lines[index], "=" * (sum(widths) + 3))
        for index in (1, 3, 4):
            self.assertEqual(len(lines[index]), sum(widths) + 3)
        self.assertIn(description, lines[3])
        self.assertTrue(lines[3].endswith(category))
        amount_start = widths[0] + widths[1] + 2
        self.assertEqual(lines[3][amount_start:amount_start + widths[2]], "$1234567890123.50")
        self.assertEqual(lines[4][amount_start:amount_start + widths[2]], "$2.00".rjust(widths[2]))

    def test_headers_set_minimum_column_widths(self):
        """Short values still leave enough room for all four headings."""
        rows = [tuple(tracker.PROMPTS["table_headers"].values()), ("d", "x", "$1.00", "c")]
        with patch("sys.stdout", new_callable=StringIO) as output:
            tracker._print_expense_table(rows)
        lines = output.getvalue().strip("\n").splitlines()
        self.assertEqual(lines[1], "Date Description Amount Category")
        self.assertEqual(len(lines[3]), len(lines[1]))
        self.assertEqual(lines[0], "=" * len(lines[1]))


if __name__ == "__main__":
    unittest.main()
