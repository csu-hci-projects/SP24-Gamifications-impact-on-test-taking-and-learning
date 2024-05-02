import quiz
import create
import utils
from create import CreateQuizName, CreateQuizQuestions
from dialogs import DialogInput, TransitionScreen, QuizDialogInput
import os, sys
from myclasses import UserScores
# os.environ['SDL_VIDEO_CENTERED'] = '1'

def goodbye():
    mydialog = TransitionScreen()
    mydialog.main()
    sys.exit()
'''
def sub_loop(user_name):
    quiz_name = get_quiz_name()
    if quiz_name == "quit":
        goodbye()
    what_to_do = select_action()
    # ---- ----
    if what_to_do == "take the quiz":
        quiz.main(user_name, quiz_name)
    elif what_to_do == "review your accumulated score":
        read_stats(user_name, quiz_name)
    elif what_to_do == "reset your scores":
        reset_stats(user_name, quiz_name)
    else:
        s = "I don't recognize this: {}".format(what_to_do)
        raise ValueError(s)
    # ---- ----
    return True
'''
def select_quiz_type():
    options = ["Multiple Choices", "Fill in the Blank"]
    show_list = ["What type of quiz would you like to take?"]
    show_list.append(" ")
    show_list_body = [f"{i+1}) {option}" for i, option in enumerate(options)]
    possible_choices = list(range(1, len(options)+1))
    mydialog = QuizDialogInput(show_list + show_list_body, possible_choices, show_possible_responses=False, line_width=50)
    quiz_type = int(mydialog.main())
    return options[quiz_type - 1].lower()  


def sub_loop(user_name):
    what_to_do = select_prequiz_actions()
    # ---- ----
    if what_to_do == "take a quiz":
        quiz_name = get_quiz_name()
        if quiz_name == "quit":
            return False  # Handles exit case if user selects 'quit'
        quiz_type = select_quiz_type()  # Get the quiz type from the user
        quiz.main(user_name, quiz_name, quiz_type)  # Pass the quiz type to your quiz function
    elif what_to_do == "make a quiz":
        create.main()
    elif what_to_do == "review your accumulated score":
        quiz_name = get_quiz_name()
        read_stats(user_name, quiz_name)
    elif what_to_do == "reset your scores":
        quiz_name = get_quiz_name()
        reset_stats(user_name, quiz_name)
    else:
        s = "I don't recognize this: {}".format(what_to_do)
        raise ValueError(s)
    return True


def select_prequiz_actions():
    show_list = ["What would you like to do?"]
    show_list.append(" ")
    mylist = ["Take a quiz"]
    mylist.append("Make a quiz")
    mylist.append("Review your accumulated score")
    mylist.append("Reset your scores")
    show_list_body = ["{}) {}".format(count+1, i) for count, i in enumerate(mylist)]
    possible_choices = list(range(1, len(mylist)+1))
    mydialog = QuizDialogInput(show_list + show_list_body, possible_choices, show_possible_responses=False, line_width=50)
    what_to_do = int(mydialog.main())
    what_to_do = mylist[what_to_do-1].lower().strip()
    return what_to_do


def select_quiz_actions():
    show_list = ["What would you like to do with this quiz?"]
    show_list.append(" ")
    mylist = ["Take the quiz"]
    mylist.append("Review your accumulated score")
    mylist.append("Reset your scores")
    show_list_body = ["{}) {}".format(count+1, i) for count, i in enumerate(mylist)]
    possible_choices = list(range(1, len(mylist)+1))
    mydialog = QuizDialogInput(show_list + show_list_body, possible_choices, show_possible_responses=False, line_width=50)
    what_to_do = int(mydialog.main())
    what_to_do = mylist[what_to_do-1].lower().strip()
    return what_to_do

def reset_stats(user_name, quiz_name):
    filename = "{}.txt".format(quiz_name)
    filepath = os.path.join("data", "users", user_name, "scores", filename)
    if os.path.isfile(filepath) == False: raise ValueError("Error")
    # ---- ----
    mylist = utils.read_data_file(filepath, 5)
    # ---- ----
    big_list = []
    myindex = 0
    for _ in range(len(mylist)):
        s = "user_name: {}\n".format(user_name)
        s += "quiz_name: {}\n".format(quiz_name)
        s += "question_index: {}\n".format(myindex)
        s += "times_question_correct: 0\n"
        s += "times_question_presented: 0\n\n"
        big_list.append(s)
        myindex += 1
    # ---- ----
    # filepath = os.path.join("data", "testing.txt")
    with open(filepath, "w") as f:
        for elem in big_list:
            f.write(elem)
    # ---- ----
    text_list = ["All questions have been reset!"]
    text_list.append(" ")
    text_list.append("Press <Return> to continue...")
    mydialog = DialogInput(text_list, [], show_possible_responses=False)
    mydialog.main()

def read_stats(user_name, quiz_name):
    myclass = UserScores(user_name, quiz_name)
    myclass.read_data()
    total_score = myclass.get_score_across_questions()
    print(total_score)
    mydialog = DialogInput(total_score, [], show_possible_responses=False)
    mydialog.main()


def is_int(value):
        """Check if the given value can be converted to an integer."""
        try:
            int(value)
            return True
        except ValueError:
            return False


def get_quiz_name():
    filedir = os.path.join("data", "quizzes")
    files = os.listdir(filedir)
    files = [i.replace(".txt", "").upper() for i in files ]
    # ---- ---- ---- ----
    mylist = []
    mycounter = 1
    for elem in files:
        s = "{}) {}".format(mycounter, elem)
        mylist.append(s)
        mycounter += 1
    # ---- ---- ---- ----
    mylist.append(" ")
    mylist.append("{}) Exit the program".format(mycounter))
    mytext = ["                       **** MAIN MENU ****"]
    mytext.append(" ")
    mytext.append("Pick an option:")
    mytext.append(" ")
    mytext += mylist
    mytext.append(" ")
    # mytext.append("Press <Return> to continue...")
    possible_choices = list(range(1, len(files)+2))
    mydialog = QuizDialogInput(mytext, possible_choices, show_possible_responses=False, line_width=50)
    message = mydialog.main()
    if message is None:
        return "quit" # empty string passed b/c user closed window by pressing <ESC>
    if is_int(message) == False:
        s = "Message is: {}\n".format(message)
        s += "Message is of type: {}".format(type(message))
        raise ValueError(s)
    quiz_number = int(message)
    if quiz_number <= len(files):
        quiz_name = files[quiz_number-1].lower().replace(" ", "_")
    else:
        return "quit"
    return quiz_name


def main(user_name):
    #Shows splashscreen of team logo when code is ran
    mydialog = TransitionScreen()
    mydialog.main()
    # ---- ----
    keep_looping = True
    while keep_looping == True:
        keep_looping = sub_loop(user_name)
    # ---- ----

if __name__ == "__main__":
    user_name = "chris"
    main(user_name)