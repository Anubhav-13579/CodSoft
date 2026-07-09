from utils import print_colored, Colors, get_input, print_sub_separator

qa_dict = {
    "what is ai?": "AI (Artificial Intelligence) is the simulation of human intelligence processes by machines, especially computer systems.",
    "what is machine learning?": "Machine Learning (ML) is a subset of AI that focuses on building systems that learn from data, improving their accuracy over time without being explicitly programmed.",
    "what is deep learning?": "Deep Learning is a specialized form of machine learning that involves neural networks with many layers (deep neural networks) to model complex patterns in data.",
    "what is python?": "Python is a high-level, interpreted programming language known for its simplicity and readability, widely used in web development, data science, and AI.",
    "what is data science?": "Data Science is an interdisciplinary field that uses scientific methods, processes, algorithms, and systems to extract knowledge and insights from structured and unstructured data.",
    "difference between ai and ml": "AI is the broader concept of machines being able to carry out tasks in a smart way, whereas ML is an application of AI based on the idea that we should give machines access to data and let them learn for themselves.",
    "difference between compiler and interpreter": "A compiler translates the entire source code into machine code before execution, whereas an interpreter translates and executes the code line by line.",
    "difference between ram and rom": "RAM (Random Access Memory) is volatile memory used for temporary storage of data being actively used by the CPU. ROM (Read-Only Memory) is non-volatile and stores permanent instructions like the computer's BIOS."
}

def run_study_assistant():
    print("\n" + Colors.CYAN + "=== STUDY ASSISTANT ===" + Colors.ENDC)
    print("Welcome to the Study Assistant! You can ask questions like:")
    print(" - What is AI?")
    print(" - Difference between AI and ML")
    print(" - What is Python?")
    print_colored("Type 'list' to see all available questions.", Colors.WARNING)
    print_colored("Type 'back' or 'exit' to return to the main menu.", Colors.WARNING)
    print_sub_separator()
    
    while True:
        question = get_input("Ask a question: ")
        question_lower = question.lower().strip()
        
        if question_lower in ['back', 'exit', 'quit']:
            break
        elif question_lower == 'list':
            print("\nAvailable Questions:")
            for q in qa_dict.keys():
                print(f" - {q.title()}?")
            print()
            continue
            
        found = False
        for key in qa_dict:
            if key in question_lower:
                print_colored(f"Answer: {qa_dict[key]}", Colors.GREEN)
                found = True
                break
                
        if not found:
            print_colored("Sorry, I don't know the answer to that. Type 'list' to see what I know.", Colors.FAIL)
