import random
from utils import print_colored, Colors, get_input, get_number_input, print_sub_separator

jokes = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "Why did the developer go broke? Because he used up all his cache.",
    "How many programmers does it take to change a light bulb? None, that's a hardware problem."
]

quotes = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Code is like humor. When you have to explain it, it's bad. - Cory House",
    "First, solve the problem. Then, write the code. - John Johnson",
    "Make it work, make it right, make it fast. - Kent Beck"
]

facts = [
    "Python was named after the British comedy group Monty Python.",
    "The first computer virus was created in 1983 and was called the 'Elk Cloner'.",
    "There are over 700 programming languages in the world.",
    "The first computer mouse was made of wood."
]

def run_fun_zone():
    while True:
        print("\n" + Colors.CYAN + "=== FUN ZONE ===" + Colors.ENDC)
        print("1. Random Joke")
        print("2. Random Motivational Quote")
        print("3. Random Fact")
        print("4. Coin Toss")
        print("5. Dice Roll")
        print("6. Guess the Number Game")
        print("7. Rock Paper Scissors")
        print("0. Back to Main Menu")
        print_sub_separator()
        
        choice = get_input("Select an option (0-7): ")
        
        if choice == '0' or choice.lower() in ['back', 'exit']:
            break
            
        if choice == '1':
            print_colored(random.choice(jokes), Colors.GREEN)
        elif choice == '2':
            print_colored(random.choice(quotes), Colors.GREEN)
        elif choice == '3':
            print_colored(random.choice(facts), Colors.GREEN)
        elif choice == '4':
            print_colored(f"Result: {random.choice(['Heads', 'Tails'])}", Colors.GREEN)
        elif choice == '5':
            print_colored(f"Result: {random.randint(1, 6)}", Colors.GREEN)
        elif choice == '6':
            play_guess_number()
        elif choice == '7':
            play_rock_paper_scissors()
        else:
            print_colored("Invalid option.", Colors.FAIL)

def play_guess_number():
    number_to_guess = random.randint(1, 100)
    print("\nI have selected a number between 1 and 100. Try to guess it!")
    attempts = 0
    while True:
        guess = get_number_input("Your guess: ", allow_float=False)
        if guess is None:
            break
        attempts += 1
        if guess < number_to_guess:
            print_colored("Too low!", Colors.WARNING)
        elif guess > number_to_guess:
            print_colored("Too high!", Colors.WARNING)
        else:
            print_colored(f"Congratulations! You guessed the number in {attempts} attempts.", Colors.GREEN)
            break

def play_rock_paper_scissors():
    choices = ['rock', 'paper', 'scissors']
    print("\nLet's play Rock, Paper, Scissors!")
    while True:
        user_choice = get_input("Enter rock, paper, or scissors (or 'back' to quit): ").lower()
        if user_choice in ['back', 'exit', 'quit']:
            break
        if user_choice not in choices:
            print_colored("Invalid choice. Please choose rock, paper, or scissors.", Colors.FAIL)
            continue
            
        bot_choice = random.choice(choices)
        print(f"I chose: {bot_choice}")
        
        if user_choice == bot_choice:
            print_colored("It's a tie!", Colors.WARNING)
        elif (user_choice == 'rock' and bot_choice == 'scissors') or \
             (user_choice == 'paper' and bot_choice == 'rock') or \
             (user_choice == 'scissors' and bot_choice == 'paper'):
            print_colored("You win!", Colors.GREEN)
        else:
            print_colored("You lose!", Colors.FAIL)
