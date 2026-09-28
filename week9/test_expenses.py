"""Regression tests for the three Week 9 improvements."""

import os
import tempfile
import unittest
from io import StringIO
from unittest.mock import call, patch

import expenses as tracker


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
        rows = [tracker.PROMPTS["table_headers"], ("d", "x", "$1.00", "c")]
        with patch("sys.stdout", new_callable=StringIO) as output:
            tracker._print_expense_table(rows)
        lines = output.getvalue().strip("\n").splitlines()
        self.assertEqual(lines[1], "Date Description Amount Category")
        self.assertEqual(len(lines[3]), len(lines[1]))
        self.assertEqual(lines[0], "=" * len(lines[1]))


if __name__ == "__main__":
    unittest.main()
