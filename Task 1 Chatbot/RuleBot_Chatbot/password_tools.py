import string
import random
import re
from utils import print_colored, Colors, get_input, get_number_input, print_sub_separator

def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password is too short (minimum 8 characters).")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Password should contain at least one uppercase letter.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Password should contain at least one lowercase letter.")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Password should contain at least one number.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Password should contain at least one special character.")

    if score == 5:
        return "Strong", feedback
    elif score >= 3:
        return "Moderate", feedback
    else:
        return "Weak", feedback

def generate_password(length=12):
    if length < 4:
        return "Error: Length must be at least 4 to include all character types."
    
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special = string.punctuation

    all_characters = uppercase + lowercase + digits + special

    password = [
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(digits),
        random.choice(special)
    ]

    password += random.choices(all_characters, k=length-4)
    random.shuffle(password)

    return "".join(password)

def run_password_tools():
    while True:
        print("\n" + Colors.CYAN + "=== PASSWORD TOOLS ===" + Colors.ENDC)
        print("1. Password Strength Checker")
        print("2. Random Password Generator")
        print("0. Back to Main Menu")
        print_sub_separator()
        
        choice = get_input("Select an option (0-2): ")
        
        if choice == '0' or choice.lower() in ['back', 'exit']:
            break
            
        if choice == '1':
            password = get_input("Enter a password to check: ")
            strength, feedback = check_password_strength(password)
            
            color = Colors.GREEN if strength == "Strong" else (Colors.WARNING if strength == "Moderate" else Colors.FAIL)
            print_colored(f"Strength: {strength}", color)
            
            if feedback:
                print("Tips to improve:")
                for tip in feedback:
                    print_colored(f" - {tip}", Colors.WARNING)
                    
        elif choice == '2':
            length = get_number_input("Enter desired password length (min 4): ", allow_float=False)
            if length is None:
                continue
            if length < 4:
                print_colored("Length must be at least 4.", Colors.FAIL)
                continue
            new_password = generate_password(length)
            print_colored(f"Generated Password: {new_password}", Colors.GREEN)
        else:
            print_colored("Invalid option.", Colors.FAIL)
