import random
import json
import requests

TRIVIA_API_URL = "https://opentdb.com/api.php?amount=1&type=multiple"
SCORES_FILE = "scores.json"

scores = {}
current_question = None
current_answer = None

# Load scores from file
def load_scores():
    global scores
    try:
        with open(SCORES_FILE, "r") as f:
            scores = json.load(f)
    except FileNotFoundError:
        scores = {}

# Save scores to file
def save_scores():
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f)

# Fetch a trivia question
def get_trivia_question():
    global current_question, current_answer
    response = requests.get(TRIVIA_API_URL).json()
    question_data = response["results"][0]
    current_question = question_data["question"]
    correct_answer = question_data["correct_answer"]
    options = question_data["incorrect_answers"] + [correct_answer]
    random.shuffle(options)
    current_answer = correct_answer.lower()
    return current_question, options

# Main loop to test the trivia functionality
def main():
    load_scores()
    while True:
        question, options = get_trivia_question()
        print(f"Trivia Time!\n{question}")
        for i, opt in enumerate(options, 1):
            print(f"{i}. {opt}")
        
        answer = input("Your answer: ").strip().lower()
        if answer == current_answer:
            print("Correct!")
        else:
            print(f"Wrong! The correct answer was: {current_answer}")
        
        save_scores()
        cont = input("Do you want another question? (yes/no): ").strip().lower()
        if cont != "yes":
            break

if __name__ == "__main__":
    main()


