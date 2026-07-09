import math
from utils import print_colored, Colors, get_number_input, get_input, print_sub_separator

def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b):
    if b == 0:
        return "Error: Division by zero."
    return a / b
def modulus(a, b):
    if b == 0:
        return "Error: Modulo by zero."
    return a % b
def exponent(a, b): return a ** b
def square(a): return a ** 2
def cube(a): return a ** 3
def square_root(a):
    if a < 0:
        return "Error: Cannot calculate square root of a negative number."
    return math.sqrt(a)
def percentage(part, whole):
    if whole == 0:
        return "Error: Whole value cannot be zero."
    return (part / whole) * 100

def run_calculator():
    while True:
        print("\n" + Colors.CYAN + "=== CALCULATOR ===" + Colors.ENDC)
        print("1. Addition (+)")
        print("2. Subtraction (-)")
        print("3. Multiplication (*)")
        print("4. Division (/)")
        print("5. Modulus (%)")
        print("6. Exponent (^)")
        print("7. Square")
        print("8. Cube")
        print("9. Square Root")
        print("10. Percentage")
        print("0. Back to Main Menu")
        print_sub_separator()
        
        choice = get_input("Select an operation (0-10): ")
        if choice == '0' or choice.lower() in ['back', 'exit']:
            break
            
        if choice in ['1', '2', '3', '4', '5', '6']:
            num1 = get_number_input("Enter first number: ")
            if num1 is None: continue
            num2 = get_number_input("Enter second number: ")
            if num2 is None: continue
            
            if choice == '1': print_colored(f"Result: {add(num1, num2)}", Colors.GREEN)
            elif choice == '2': print_colored(f"Result: {subtract(num1, num2)}", Colors.GREEN)
            elif choice == '3': print_colored(f"Result: {multiply(num1, num2)}", Colors.GREEN)
            elif choice == '4': print_colored(f"Result: {divide(num1, num2)}", Colors.GREEN)
            elif choice == '5': print_colored(f"Result: {modulus(num1, num2)}", Colors.GREEN)
            elif choice == '6': print_colored(f"Result: {exponent(num1, num2)}", Colors.GREEN)
            
        elif choice in ['7', '8', '9']:
            num = get_number_input("Enter the number: ")
            if num is None: continue
            if choice == '7': print_colored(f"Result: {square(num)}", Colors.GREEN)
            elif choice == '8': print_colored(f"Result: {cube(num)}", Colors.GREEN)
            elif choice == '9': print_colored(f"Result: {square_root(num)}", Colors.GREEN)
            
        elif choice == '10':
            part = get_number_input("Enter the part value: ")
            if part is None: continue
            whole = get_number_input("Enter the whole value: ")
            if whole is None: continue
            print_colored(f"Result: {percentage(part, whole)}%", Colors.GREEN)
        else:
            print_colored("Invalid choice. Please select a valid option.", Colors.FAIL)
