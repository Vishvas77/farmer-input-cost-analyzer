# validation.py
# Small, reusable input-validation helpers.
# Each function keeps asking until the user gives valid input,
# so the program never crashes on bad input.

def get_non_empty_input(prompt):
    """Ask for text; reject empty input and keep asking."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def get_positive_amount(prompt):
    """Ask for a cost amount; accept only a number that is 0 or more."""
    while True:
        text = input(prompt).strip()
        try:
            amount = float(text)
            if amount < 0:
                print("Amount cannot be negative. Please try again.")
                continue
            return amount
        except ValueError:
            print("Please enter a valid number (example: 8000).")


def get_menu_choice(prompt, lowest, highest):
    """Ask for a menu number; accept only an integer between lowest and highest."""
    while True:
        text = input(prompt).strip()
        try:
            choice = int(text)
            if lowest <= choice <= highest:
                return choice
            print(f"Please enter a number between {lowest} and {highest}.")
        except ValueError:
            print("Please enter a valid number.")
