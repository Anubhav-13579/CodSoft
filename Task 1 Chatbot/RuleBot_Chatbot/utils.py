import sys
import time

# ANSI color codes for colorful terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_colored(text, color):
    """Prints text in the specified color."""
    print(f"{color}{text}{Colors.ENDC}")

def print_separator():
    """Prints a decorative separator line."""
    print_colored("=" * 50, Colors.CYAN)

def print_sub_separator():
    """Prints a smaller separator line."""
    print_colored("-" * 40, Colors.BLUE)

def clear_screen():
    """Prints newlines to simulate clearing the screen."""
    print("\n" * 50)

def display_banner():
    """Displays the Welcome Banner for the chatbot."""
    banner = r"""
  _____       _       ____        _   
 |  __ \     | |     |  _ \      | |  
 | |__) |   _| | ___ | |_) | ___ | |_ 
 |  _  / | | | |/ _ \|  _ < / _ \| __|
 | | \ \ |_| | |  __/| |_) | (_) | |_ 
 |_|  \_\__,_|_|\___||____/ \___/ \__|
                                      
    """
    print_colored(banner, Colors.HEADER)
    print_colored("   Welcome to RuleBot - Your Professional Assistant", Colors.BOLD + Colors.GREEN)
    print_separator()
    print("This chatbot can help you with calculations, conversions,")
    print("strings, numbers, passwords, and even some fun!")
    print_colored("Type 'help' at any prompt for available commands.", Colors.WARNING)
    print_colored("Type 'exit' or 'bye' to quit at any time.", Colors.WARNING)
    print_separator()
    time.sleep(1)

def get_input(prompt, color=Colors.CYAN):
    """Gets input from the user with a styled prompt."""
    try:
        user_input = input(f"{color}{prompt}{Colors.ENDC} ")
        return user_input.strip()
    except (EOFError, KeyboardInterrupt):
        return "exit"

def get_number_input(prompt, allow_float=True):
    """Safely gets a number from the user."""
    while True:
        val = get_input(prompt)
        if val.lower() in ['exit', 'quit', 'bye', 'back']:
            return None
        try:
            if allow_float:
                return float(val)
            else:
                return int(val)
        except ValueError:
            print_colored("Invalid input. Please enter a valid number.", Colors.FAIL)

def confirm_continue():
    """Waits for the user to press Enter to continue."""
    print()
    input(f"{Colors.WARNING}Press Enter to continue...{Colors.ENDC}")
