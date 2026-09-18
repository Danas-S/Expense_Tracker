import unittest
from unittest.mock import patch
from expenses import main
from io import StringIO

GIVEN_TEST_INPUTS = [
    "1",                                     # Top-level menu option for listing items
    "",                                      # Go back to the main menu

    "3",                                     # Top-level menu option for adding an item
    "01/03/26,Bread and milk,5,groceries",   # Item information as required
    "",                                      # Go back to the main menu

    "3",                                     # Top-level menu option for adding an item
    "02/03/26,Scrabble, 24.99, games",       # Item information with some spaces
    "",                                      # Go back to the main menu

    "3",                                     # Top-level menu option for adding an item
    "<",                                     # String for cancelling the item
    "",                                      # Go back to the main menu

    "2",                                     # Top-level menu option for grouping items
    "c",                                     # Category chosen as grouping column
    "",                                      # Go back to the main menu

    "4",                                     # Top-level menu option for saving the data
    "",                                      # Go back to the main menu

    "5"                                      # Top-level menu option for exiting the program
]
 
INITIAL_FILE_CONTENT = \
    "id,date,description,amount,category\n" \
    "1,01/01/26,Weekly shop,50.00,groceries\n"
FILE_CONTENT_AFTER_TEST = \
    "id,date,description,amount,category\n" \
    "1,01/01/26,Weekly shop,50.00,groceries\n" \
    "2,01/03/26,Bread and milk,5,groceries\n" \
    "3,02/03/26,Scrabble,24.99,games\n"


class TestExpensesMain(unittest.TestCase):
    
    fake_file = StringIO(INITIAL_FILE_CONTENT)
    fake_file.close = lambda: None
    
    def fake_open(self, *args, **kwargs):
        mode = args[1] if len(args) > 1 else kwargs.get('mode', 'r')
        if 'w' in mode:
            self.fake_file.truncate(0)
            self.fake_file.seek(0)
        elif 'a' in mode or 'r' in mode:
            self.fake_file.seek(0)
        return self.fake_file

    def test_main(self):
        """Test the main function with a sequence of inputs that cover various functionalities of the expenses program,
        including listing items, sorting, grouping, adding items, and saving data.

        After this test runs successfully, the csv file should have two additional lines:
        2,01/03/26,T-shirt,15.00,clothes
        3,02/03/26,Scrabble,24.99,games
        """
        with patch('builtins.open', side_effect=self.fake_open) as m:
            # patch the input function to return the given test inputs in sequence
            with patch('builtins.input', side_effect=GIVEN_TEST_INPUTS):
                main()
        
            assert ("expenses.csv", "a+") in [call[0] for call in m.call_args_list]
            assert ("expenses.csv", "w") in [call[0] for call in m.call_args_list]
        
        self.assertEqual(self.fake_file.getvalue(), FILE_CONTENT_AFTER_TEST)
