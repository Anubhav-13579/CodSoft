from utils import print_colored, Colors, get_number_input, get_input, print_sub_separator

def run_converter():
    while True:
        print("\n" + Colors.CYAN + "=== UNIT CONVERTER ===" + Colors.ENDC)
        print("1. Celsius to Fahrenheit")
        print("2. Fahrenheit to Celsius")
        print("3. Kilometers to Miles")
        print("4. Miles to Kilometers")
        print("5. Kilograms to Pounds")
        print("6. Pounds to Kilograms")
        print("7. Centimeters to Inches")
        print("8. Inches to Centimeters")
        print("9. Minutes to Hours")
        print("10. Hours to Minutes")
        print("0. Back to Main Menu")
        print_sub_separator()
        
        choice = get_input("Select an option (0-10): ")
        
        if choice == '0' or choice.lower() in ['back', 'exit']:
            break
            
        if choice not in [str(i) for i in range(1, 11)]:
            print_colored("Invalid option. Try again.", Colors.FAIL)
            continue
            
        value = get_number_input("Enter the value to convert: ")
        if value is None:
            continue
            
        if choice == '1':
            result = (value * 9/5) + 32
            print_colored(f"{value}°C = {result:.2f}°F", Colors.GREEN)
        elif choice == '2':
            result = (value - 32) * 5/9
            print_colored(f"{value}°F = {result:.2f}°C", Colors.GREEN)
        elif choice == '3':
            result = value * 0.621371
            print_colored(f"{value} km = {result:.2f} miles", Colors.GREEN)
        elif choice == '4':
            result = value / 0.621371
            print_colored(f"{value} miles = {result:.2f} km", Colors.GREEN)
        elif choice == '5':
            result = value * 2.20462
            print_colored(f"{value} kg = {result:.2f} lbs", Colors.GREEN)
        elif choice == '6':
            result = value / 2.20462
            print_colored(f"{value} lbs = {result:.2f} kg", Colors.GREEN)
        elif choice == '7':
            result = value / 2.54
            print_colored(f"{value} cm = {result:.2f} inches", Colors.GREEN)
        elif choice == '8':
            result = value * 2.54
            print_colored(f"{value} inches = {result:.2f} cm", Colors.GREEN)
        elif choice == '9':
            result = value / 60
            print_colored(f"{value} minutes = {result:.2f} hours", Colors.GREEN)
        elif choice == '10':
            result = value * 60
            print_colored(f"{value} hours = {result:.2f} minutes", Colors.GREEN)
