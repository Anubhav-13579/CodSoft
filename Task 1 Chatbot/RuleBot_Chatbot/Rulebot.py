import datetime
import string_utils
import number_utils
from calculator import run_calculator
from converter import run_converter
from study import run_study_assistant
from fun_zone import run_fun_zone
from password_tools import run_password_tools
from utils import (
    Colors, print_colored, print_separator, clear_screen, display_banner,
    get_input, get_number_input, confirm_continue
)

# --- Sub-menus for String and Number Utilities ---

def run_string_utilities():
    while True:
        print("\n" + Colors.CYAN + "=== STRING UTILITIES ===" + Colors.ENDC)
        print("1. Reverse String")
        print("2. Palindrome Checker")
        print("3. Count Characters/Words/Vowels/Consonants")
        print("4. Case Conversion (Upper/Lower/Capitalize)")
        print("5. Remove Extra Spaces")
        print("6. Replace Word")
        print("0. Back to Main Menu")
        
        choice = get_input("Select an option (0-6): ")
        if choice == '0' or choice.lower() in ['back', 'exit']:
            break
            
        if choice not in [str(i) for i in range(1, 7)]:
            print_colored("Invalid choice.", Colors.FAIL)
            continue
            
        text = get_input("Enter your string: ")
        
        if choice == '1':
            print_colored(f"Reversed: {string_utils.reverse_string(text)}", Colors.GREEN)
        elif choice == '2':
            is_pal = string_utils.is_palindrome(text)
            print_colored(f"Is Palindrome: {'Yes' if is_pal else 'No'}", Colors.GREEN)
        elif choice == '3':
            print_colored(f"Characters: {string_utils.count_characters(text)}", Colors.GREEN)
            print_colored(f"Words: {string_utils.count_words(text)}", Colors.GREEN)
            print_colored(f"Vowels: {string_utils.count_vowels(text)}", Colors.GREEN)
            print_colored(f"Consonants: {string_utils.count_consonants(text)}", Colors.GREEN)
        elif choice == '4':
            print_colored(f"Uppercase: {string_utils.to_uppercase(text)}", Colors.GREEN)
            print_colored(f"Lowercase: {string_utils.to_lowercase(text)}", Colors.GREEN)
            print_colored(f"Capitalized: {string_utils.capitalize_sentence(text)}", Colors.GREEN)
        elif choice == '5':
            print_colored(f"Cleaned: {string_utils.remove_extra_spaces(text)}", Colors.GREEN)
        elif choice == '6':
            old = get_input("Word to replace: ")
            new = get_input("New word: ")
            print_colored(f"Result: {string_utils.replace_word(text, old, new)}", Colors.GREEN)

def run_number_utilities():
    while True:
        print("\n" + Colors.CYAN + "=== NUMBER UTILITIES ===" + Colors.ENDC)
        print("1. Even/Odd Checker")
        print("2. Prime Number Checker")
        print("3. Armstrong Number Checker")
        print("4. Fibonacci Series")
        print("5. Factorial")
        print("6. LCM & GCD")
        print("0. Back to Main Menu")
        
        choice = get_input("Select an option (0-6): ")
        if choice == '0' or choice.lower() in ['back', 'exit']:
            break
            
        if choice in ['1', '2', '3', '4', '5']:
            num = get_number_input("Enter an integer: ", allow_float=False)
            if num is None: continue
            
            if choice == '1':
                print_colored(f"Result: {number_utils.is_even_or_odd(num)}", Colors.GREEN)
            elif choice == '2':
                print_colored(f"Is Prime: {'Yes' if number_utils.is_prime(num) else 'No'}", Colors.GREEN)
            elif choice == '3':
                print_colored(f"Is Armstrong: {'Yes' if number_utils.is_armstrong(num) else 'No'}", Colors.GREEN)
            elif choice == '4':
                print_colored(f"Fibonacci sequence (first {num} terms): {number_utils.fibonacci_series(num)}", Colors.GREEN)
            elif choice == '5':
                res = number_utils.factorial(num)
                if res is None:
                    print_colored("Factorial not defined for negative numbers.", Colors.FAIL)
                else:
                    print_colored(f"Factorial: {res}", Colors.GREEN)
                    
        elif choice == '6':
            a = get_number_input("Enter first number: ", allow_float=False)
            if a is None: continue
            b = get_number_input("Enter second number: ", allow_float=False)
            if b is None: continue
            print_colored(f"LCM: {number_utils.calculate_lcm(a, b)}", Colors.GREEN)
            print_colored(f"GCD: {number_utils.calculate_gcd(a, b)}", Colors.GREEN)

# --- General Conversations ---

def handle_general_conversation(user_input, user_name):
    inp = user_input.lower().strip()
    
    greetings = ['hi', 'hello', 'hey', 'good morning', 'good evening', 'good afternoon']
    if any(greet in inp for greet in greetings):
        return f"Hello {user_name}! How can I assist you today?"
        
    if "how are you" in inp:
        return f"I'm just a set of rules running on your computer, but I'm doing great! How about you, {user_name}?"
        
    if "your name" in inp:
        return "My name is RuleBot, your friendly professional assistant."
        
    if "who created you" in inp:
        return "I was created by a talented Python developer to demonstrate rule-based systems."
        
    if "thank" in inp:
        return f"You're very welcome, {user_name}!"
        
    return None

# --- Main Program Logic ---

def main():
    clear_screen()
    display_banner()
    
    # Session Memory
    user_name = ""
    while not user_name:
        user_name = get_input("Hello! What is your name? ")
        if user_name.lower() in ['exit', 'bye', 'quit']:
            print_colored("Have a wonderful day! Goodbye!", Colors.GREEN)
            return
            
    print_colored(f"\nWelcome, {user_name}!", Colors.GREEN)
    
    while True:
        print("\n" + Colors.CYAN + "==========================")
        print("RULEBOT MAIN MENU")
        print("==========================" + Colors.ENDC)
        print("1. General Conversation")
        print("2. Date & Time")
        print("3. Calculator")
        print("4. String Utilities")
        print("5. Number Utilities")
        print("6. Unit Converter")
        print("7. Fun Zone")
        print("8. Study Assistant")
        print("9. Password Tools")
        print("10. Help")
        print("11. Exit")
        
        choice = get_input("\nEnter your choice (1-11): ")
        
        if choice == '11' or choice.lower() in ['exit', 'quit', 'bye']:
            print_separator()
            print_colored(f"Thank you for chatting with me, {user_name}.", Colors.GREEN)
            print_colored("Have a wonderful day!", Colors.GREEN)
            print_colored("Goodbye!", Colors.GREEN)
            break
            
        elif choice == '1' or choice.lower() == 'general conversation':
            print("\n" + Colors.CYAN + "=== GENERAL CONVERSATION ===" + Colors.ENDC)
            print("Chat with me! Type 'back' to return to the main menu.")
            while True:
                msg = get_input(f"{user_name}: ")
                if msg.lower() in ['back', 'exit', 'quit']:
                    break
                response = handle_general_conversation(msg, user_name)
                if response:
                    print_colored(f"RuleBot: {response}", Colors.GREEN)
                else:
                    print_colored("RuleBot: I'm not sure how to respond to that. Try saying hello, asking my name, or who created me.", Colors.WARNING)
                    
        elif choice == '2':
            now = datetime.datetime.now()
            print("\n" + Colors.CYAN + "=== DATE & TIME ===" + Colors.ENDC)
            print(f"Current Date: {now.strftime('%Y-%m-%d')}")
            print(f"Current Time: {now.strftime('%H:%M:%S')}")
            print(f"Current Day: {now.strftime('%A')}")
            print(f"Current Month: {now.strftime('%B')}")
            print(f"Current Year: {now.strftime('%Y')}")
            confirm_continue()
            
        elif choice == '3':
            run_calculator()
            
        elif choice == '4':
            run_string_utilities()
            
        elif choice == '5':
            run_number_utilities()
            
        elif choice == '6':
            run_converter()
            
        elif choice == '7':
            run_fun_zone()
            
        elif choice == '8':
            run_study_assistant()
            
        elif choice == '9':
            run_password_tools()
            
        elif choice == '10' or choice.lower() == 'help':
            print("\n" + Colors.CYAN + "=== HELP MENU ===" + Colors.ENDC)
            print("Welcome to RuleBot's Help section.")
            print("Navigate the main menu by typing the number of the module you want to access.")
            print("At any prompt, you can usually type 'back' to return to the previous menu.")
            print("Available Modules:")
            print(" - Calculator: Basic arithmetic operations")
            print(" - String/Number Utilities: Helper functions for math and text")
            print(" - Converter: Convert between units of measurement")
            print(" - Study Assistant: Predefined answers for common tech questions")
            print(" - Password Tools: Generate and check passwords")
            print(" - Fun Zone: Games, jokes, and quotes")
            print("\nGlobal Commands:")
            print(" 'help' - Display this help menu")
            print(" 'exit', 'quit', 'bye' - Close the application")
            confirm_continue()
            
        else:
            print_colored("I didn't understand that choice. Please enter a number between 1 and 11.", Colors.FAIL)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_colored(f"\nAn unexpected error occurred: {e}", Colors.FAIL)
        print_colored("Exiting RuleBot safely.", Colors.WARNING)
