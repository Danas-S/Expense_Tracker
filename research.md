Q. What is the percentage variation of energy use that can be caused by different prompting styles for genAI-assisted programming?

A. Different prompting styles for genAI-assisted programming can cause energy use variations ranging from a 7% reduction to a 99% reduction depending on the technique and configuration. Research on the Llama 3 model shows that one-shot and few-shot prompting with custom tags reduced energy consumption by 99% and 83% respectively compared to default zero-shot configurations.

Q. What prompt characteristics contribute to better energy efficiency? List at least three and explain them.

A. 1. Explicit Energy Efficiency Directives: Simply instructing the model to generate "energy efficient" code can trigger its internal knowledge on green practices, acting as a baseline for optimization.

2. Chain-of-Thought Prompting: This technique asks the model to "think step-by-step" and provide a rationale for its optimization decisions. Research shows it can consistently reduce energy consumption in some models by guiding more deliberate and efficient reasoning. 

3. Use of Custom Tags and Structure: Incorporating specific tags and structured explanations in the prompt helps the model parse the request more efficiently. Studies found this can significantly reduce energy use by up to 99% in some cases—by improving the clarity of the task for the model's inference process. 

Q. Do the energy-optimal prompt characteristics vary across genAI instances (products)?

A. Yes, energy optimal prompt characteristics vary significantly across different generative AI, as energy consumption is influenced by the specific model architecture, task type, and provider infrastructure rather than just prompt length. 

Q. Three pieces of of information you should not type into prompts in order to preserve privacy, both your own and that of others

A. 1. Personal Identifiable Information such as names, addresses, phone numbers, or email addresses

2. Financial data like bank account details, credit card numbersor payslips.

3. Health information like medical records, diagnoses, or medications 

Week 9 expenses.py improvement notes

Chosen improvements (3 aspects)
1. Invalid-header overwrite flow should exit on "no".
2. Expense table uses hard-coded column widths.
3. Menu options are hard-coded into strings and duplicated logic.

Improvement 1
- Who is affected and how: users are affected because choosing "no" after being asked to overwrite an invalid file should safely stop processing, but continuing can hide file problems and lead to incorrect assumptions about loaded data.
- Prompt used: "If the CSV header is invalid and the user answers no to overwrite, update the function to exit the program cleanly instead of continuing with an empty list."
- Solution summary: `_load_or_validate_file` now returns `None` when overwrite is declined, leaving the file unchanged. `load_or_create_expenses` propagates that status and `main` returns before entering the menu. A successful load or confirmed overwrite still returns a list. The lower-level helper no longer terminates the application; EOF at confirmation also reaches main for a clean exit.

Improvement 2
- Who is affected and how: users and maintainers are affected by fixed column widths because output alignment breaks with longer values and code is harder to adapt.
- Prompt used: "Refactor display_expenses to calculate table column widths dynamically from headers and actual expense values, and keep amount right-aligned."
- Solution summary: `display_expenses` builds display rows with headings from `PROMPTS`, and `_print_expense_table` computes each column width from all headings and values. Long descriptions and categories remain complete, amounts stay right-aligned with two decimal places, and the border matches the table width.

Improvement 3
- Who is affected and how: users and developers are affected by hard-coded menu numbers/text because inconsistencies can appear when menu options are changed.
- Prompt used: "Replace hard-coded menu option numbers in strings and menu dispatch with shared constants, and generate menu text/prompt dynamically from one source of truth."
- Solution summary: `MENU_ITEMS` pairs shared option constants with keys in `PROMPTS`, so all user-facing labels remain in the required dictionary. `VALID_MENU_CHOICES` is derived from these items; the menu display, input prompt and invalid-choice message use this configuration. `_handle_menu_choice` uses the same constants and pauses in one place after a completed operation.

Repair provenance: The prompt quotations above are the original recorded prompts. This later repair used OpenAI Codex following the supplied repository-repair request; it does not represent a new Copilot experiment. The sustainability and privacy research above has been retained unchanged.
