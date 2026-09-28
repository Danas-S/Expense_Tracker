"""Unit tests for expenses.py

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
    _get_text_input,
    _create_expense_dict,
    save_expenses,
    get_valid_date,
    get_valid_amount,
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
        self.assertEqual(result[0]["description"], "Groceries")
    
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["no"])
    def test_user_prompted_for_overwrite_if_header_missing(self, mock_input, mock_print):
        """Check that user is prompted for overwrite if header is missing"""
        # Create invalid file
        with open(self.test_file, "w") as f:
            f.write("invalid,header\n")
        
        result = load_or_create_expenses(self.test_file)
        self.assertEqual(result, [])
    
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
        self.assertIn("invalid,header", content)


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
        mock_print.assert_called()


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
        mock_print.assert_called()
    
    @patch("builtins.print")
    def test_no_expenses_message(self, mock_print):
        """Check that no expenses shows appropriate message"""
        display_expenses([])
        mock_print.assert_called()
        # Check that "No expenses found" was printed
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any("No expenses found" in str(call) for call in calls))
    
    @patch("builtins.print")
    def test_amounts_formatted_properly(self, mock_print):
        """Check that amounts are formatted properly"""
        expenses = [
            {"date": "2026-01-01", "description": "Test", "amount": 10.5, "category": "Food"}
        ]
        display_expenses(expenses)
        # Verify formatting in output
        mock_print.assert_called()


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
        group_expenses(expenses, "category")
        mock_print.assert_called()
    
    @patch("builtins.print")
    def test_no_expenses_message(self, mock_print):
        """Check that no expenses shows appropriate message"""
        group_expenses([], "date")
        # Should show no expenses message
        calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any("No expenses found" in str(call) for call in calls))


class TestGetValidDate(unittest.TestCase):
    """Tests for get_valid_date function"""
    
    @patch("builtins.input", side_effect=["2026-01-15"])
    def test_valid_dates_accepted(self, mock_input):
        """Check that valid dates are accepted"""
        result = get_valid_date()
        self.assertEqual(result, "2026-01-15")
    
    @patch("builtins.input", side_effect=["invalid", "2026-01-15"])
    @patch("builtins.print")
    def test_invalid_formats_rejected(self, mock_print, mock_input):
        """Check that invalid formats are rejected"""
        result = get_valid_date()
        self.assertEqual(result, "2026-01-15")
        mock_print.assert_called()
    
    @patch("builtins.input", side_effect=["cancel"])
    def test_cancellation_returns_none(self, mock_input):
        """Check that cancellation returns None"""
        result = get_valid_date()
        self.assertIsNone(result)
    
    @patch("builtins.input", side_effect=["2024-02-29"])
    def test_leap_years_handled(self, mock_input):
        """Check that leap years are handled"""
        result = get_valid_date()
        self.assertEqual(result, "2024-02-29")


class TestGetValidAmount(unittest.TestCase):
    """Tests for get_valid_amount function"""
    
    @patch("builtins.input", side_effect=["50.00"])
    def test_positive_numbers_accepted(self, mock_input):
        """Check that positive numbers are accepted"""
        result = get_valid_amount()
        self.assertEqual(result, 50.00)
    
    @patch("builtins.input", side_effect=["50.99"])
    def test_decimal_numbers_accepted(self, mock_input):
        """Check that decimal numbers are accepted"""
        result = get_valid_amount()
        self.assertEqual(result, 50.99)
    
    @patch("builtins.input", side_effect=["-25.00"])
    def test_negative_numbers_accepted(self, mock_input):
        """Check that negative numbers are accepted"""
        result = get_valid_amount()
        self.assertEqual(result, -25.00)
    
    @patch("builtins.input", side_effect=["not_a_number", "50.00"])
    @patch("builtins.print")
    def test_non_numeric_input_rejected(self, mock_print, mock_input):
        """Check that non-numeric input is rejected"""
        result = get_valid_amount()
        self.assertEqual(result, 50.00)
        mock_print.assert_called()
    
    @patch("builtins.input", side_effect=["cancel"])
    def test_cancellation_returns_none(self, mock_input):
        """Check that cancellation returns None"""
        result = get_valid_amount()
        self.assertIsNone(result)


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
        mock_print.assert_called()
    
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


class TestGetTextInput(unittest.TestCase):
    """Tests for _get_text_input function"""
    
    @patch("builtins.input", side_effect=["Groceries"])
    def test_text_input_returned(self, mock_input):
        """Check that text input is returned"""
        result = _get_text_input("description_prompt")
        self.assertEqual(result, "Groceries")
    
    @patch("builtins.input", side_effect=["cancel"])
    def test_cancellation_returns_none(self, mock_input):
        """Check that cancellation returns None"""
        result = _get_text_input("description_prompt")
        self.assertIsNone(result)
    
    @patch("builtins.input", side_effect=["Test Input"])
    def test_prompt_displayed_correctly(self, mock_input):
        """Check that prompt is displayed correctly"""
        result = _get_text_input("description_prompt")
        self.assertEqual(result, "Test Input")


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
        self.assertEqual(len(rows), 2)
    
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
        mock_print.assert_called_once_with(tracker.PROMPTS["invalid_choice"])
        for mock in self.actions.values():
            mock.assert_not_called()


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


if __name__ == "__main__":
    unittest.main()
