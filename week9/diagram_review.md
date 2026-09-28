# Manual diagram corrections

Reviewed `../expensediagram.jpg` (the original paper photograph),
`../expensediagramfinal.jpg`, and their identical copies in `../week5/`.
There is no separate Week 9 final diagram or editable diagram source in the
supplied repository. The final JPG has the right broad startup/menu/expense
branches, but its menu numbers are not a mapping to the original components.
Many boxes lack a description ending in a bracketed function name, and the
startup box is clipped at the right edge. The image has not been altered.

The numbering below is a proposed review mapping, not numbering that existed
on the original paper. Add matching numbers to an annotated copy of the original
and the revised final diagram, retaining the untouched photograph as evidence.
Keep the menu option numbers 1-5 separate from these component numbers.

| Component number | Original component / current box | Required final label |
| --- | --- | --- |
| 0 | Expense Tracking / Start Program | Run expense tracker [main] |
| 10 | Start up; check if file exists / Load or create expenses.csv | Load or create expense file [load_or_create_expenses] |
| 11 | Create file | Create or overwrite CSV with the header [_create_csv_file] |
| 12 | Check header; read data from file | Validate header and read expense rows [_load_or_validate_file] |
| 13 | Ask permission to overwrite | Ask for overwrite confirmation [get_valid_yes_no] |
| 20 | Menu / Display Menu Options | Run the menu loop [main] |
| 21 | User Choice | Dispatch the chosen operation [_handle_menu_choice] |
| 22 | Invalid input / Show invalid choice message | Report an invalid menu choice [_handle_menu_choice] |
| 23 | Wait for Enter (added after original) | Pause before returning to the menu [_wait_for_enter] |
| 30 | Display expense items in a table / display_expenses() | Prepare and display expenses [display_expenses] |
| 31 | New Week 9 child of display | Print table using widths from headings and data [_print_expense_table] |
| 40 | Group items by date or category / Ask Group Type | Choose date or category [_handle_group_choice] |
| 41 | group_expenses() | Group expenses and display totals [group_expenses] |
| 50 | Input new expense / Input expense and Add to expense list | Read one expense line and append a valid expense [add_expense] |
| 51 | Original Date / Valid format? date check | Validate either supported date format [_is_valid_date_text] |
| 52 | Original Description, Amount, Category / Valid format? | Split and validate all four entered fields [_parse_expense_line] |
| 53 | Create expense dictionary | Create the expense record [_create_expense_dict] |
| 54 | Assign ID | Find the next unused sequential ID [get_next_id] |
| 60 | Save current list / save_expenses() | Save current expenses to CSV [save_expenses] |
| 70 | Exit / End Program | Finish the application [main] |

For Week 9, add two small children of component 20:

- **24:** Build the numbered menu from configured labels [_build_menu_options_text]
- **25:** Build the valid-choice input prompt [_build_menu_choice_prompt]

Components 31, 24 and 25 are additions to the original decomposition. Week 5
does not have these helpers. The original four field bubbles represent data in
one line, not four prompts; do not label them with the removed `get_valid_date`,
`get_valid_amount` or `_get_text_input` functions.

Correct or add these flow connections:

1. Startup: missing/empty file goes to 11, then menu. A valid header loads rows
   through 12, then menu. An invalid header goes to 13; `yes` goes to 11.
2. Week 9 `no`: 12 returns `None`, 10 propagates it, and 0/70 (`main`) finishes
   before the menu. Week 5's retained baseline instead returns an empty list.
3. Add: `<` or EOF returns `False` without appending; otherwise validate the
   single line. Invalid data prints the error and retries entry. Valid data gets
   an ID and is appended once, then goes to 23 and back to the menu. Ensure the
   curved arrow does not send a successful addition straight back into entry.
4. Group: invalid `d`/`c` input retries component 40. A valid choice goes through
   41, then 23, then menu.
5. EOF at the main menu, overwrite confirmation or grouping reaches `main` and
   ends cleanly. Pause EOF returns immediately; if stdin remains exhausted, the
   next main-menu read ends the program. Helpers do not call `SystemExit`.
6. Option 5 finishes without a pause. Options 1-4 pause once after returning
   normally. An invalid menu option returns directly to the menu.

Re-export with enough space for the full startup label, readable text and no
literal `\n` strings in boxes. Save the revised improved diagram as
`week9/expensediagramfinal.jpg` (or PNG) and commit that actual manual change.
The same bracketed descriptions and matching numbers are needed if submitting
the older Week 5 final image as well.
