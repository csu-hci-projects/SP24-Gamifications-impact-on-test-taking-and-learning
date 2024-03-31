import time
import random

def create_flashcards():
    flashcards = {}
    
    while True:
        question = input("Enter a question (or type 'quiz' to stop and start the quiz): ")
        if question.lower() == 'quiz':
            break
        
        answer = input("Enter the answer: ")
        flashcards[question] = answer
    
    return flashcards

def fill_in_the_blank_quiz(flashcards):
    num_correct = 0
    num_questions = len(flashcards)
    print("\nLet's begin the Fill in the Blank quiz!\n")
    start_time = time.time()
    for question, answer in flashcards.items():
        user_answer = input(f"What is the answer to this question?\n{question}\nYour answer: ")
        if user_answer.lower() == answer.lower():
            print("Correct!\n")
            num_correct += 1
        else:
            print(f"Sorry, the correct answer is: {answer}\n")
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"You got {num_correct} out of {num_questions} questions correct.")
    print(f"Time taken: {elapsed_time:.2f} seconds")

def multiple_choice_quiz(flashcards):
    num_correct = 0
    num_questions = len(flashcards)

    print("\nLet's begin the Multiple Choice quiz!\n")

    start_time = time.time()
    unique_answers = list(set(flashcards.values()))

    for question, answer in flashcards.items():
        answer_choices = random.sample(unique_answers, min(4, len(unique_answers)))

        if answer not in answer_choices:
            answer_choices.append(answer)
        while len(answer_choices) < 4:
            extra_choice = random.choice(unique_answers)
            if extra_choice not in answer_choices:
                answer_choices.append(extra_choice)
        
        random.shuffle(answer_choices)
        print(f"Question: {question}")

        for i, choice in enumerate(answer_choices):
            print(f"{chr(97 + i)}. {choice}")

        user_choice = input("Choose the correct option (a, b, c, or d): ").lower()
        correct_choice = chr(97 + answer_choices.index(answer))

        if user_choice == correct_choice:
            print("Correct!\n")
            num_correct += 1
        else:
            print(f"Incorrect. The correct answer is: {correct_choice}. {answer}\n")
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"You answered {num_correct} out of {num_questions} questions correctly.")
    print(f"Time taken: {elapsed_time:.2f} seconds")

def main():
    print("Welcome to the Flashcard Quiz!")
    flashcards = create_flashcards()
    
    print("\nFlashcards Created:")
    for question, answer in flashcards.items():
        print(f"Question: {question}")
        print(f"Answer: {answer}\n")
    
    choice = input("Type 'f' for Fill in the Blank or 'm' for Multiple Choice: ").lower()
    
    if choice == 'f':
        fill_in_the_blank_quiz(flashcards)
    elif choice == 'm':
        multiple_choice_quiz(flashcards)
    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main()
