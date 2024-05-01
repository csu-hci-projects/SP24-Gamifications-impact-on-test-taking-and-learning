import csv

def create_quiz_csv(quiz_name):
    questions = []
    while True:
        question_text = input("Enter the question text (or type 'done' to finish): ")
        if question_text.lower() == 'done':
            break

        options = []
        for option_label in ['A', 'B', 'C', 'D']:
            option_text = input(f"Enter option {option_label}: ")
            options.append(option_text)

        correct_answer = input("Enter the correct answer (A, B, C, or D): ")

        # Add the question details to the list
        questions.append({'question': question_text, 'options': options, 'correct_answer': correct_answer})

    # Write the questions to a CSV file
    csv_file_path = f"data/quizzes/{quiz_name}.csv"
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['Question', 'Option A', 'Option B', 'Option C', 'Option D', 'Correct Answer']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for question in questions:
            writer.writerow({
                'Question': question['question'],
                'Option A': question['options'][0],
                'Option B': question['options'][1],
                'Option C': question['options'][2],
                'Option D': question['options'][3],
                'Correct Answer': question['correct_answer']
            })

    print(f"Quiz '{quiz_name}' created successfully at '{csv_file_path}'")

def main():
    quiz_name = input("Enter the name of the quiz: ")
    create_quiz_csv(quiz_name)

if __name__ == "__main__":
    main()
