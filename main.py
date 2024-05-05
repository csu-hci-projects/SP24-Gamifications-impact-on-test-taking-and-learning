import quiz
import create
import utils
from create import CreateQuizName, CreateQuizQuestions
from dialogs import DialogInput, TransitionScreen, QuizDialogInput
import os, sys

def goodbye():
    mydialog = TransitionScreen()
    mydialog.main()
    sys.exit()

def select_quiz_type():
    options = ["Multiple Choices", "Fill in the Blank", "Mixed Quiz"]
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
    if what_to_do == "make/edit a quiz":
        create.main()
    elif what_to_do == "take a quiz":
        quiz_name = get_quiz_name()
        if quiz_name == "quit":
            return False  
        quiz_type = select_quiz_type() 
        quiz.main(user_name, quiz_name, quiz_type)  
    elif what_to_do == "make/edit a quiz":
        create.main()
    else:
        s = "I don't recognize this: {}".format(what_to_do)
        raise ValueError(s)
    return True


def select_prequiz_actions():
    show_list = ["                       **** MAIN MENU ****"]
    show_list.append(" ")
    show_list.append("What would you like to do?")
    show_list.append(" ")
    mylist = ["Make/Edit a quiz"]
    mylist.append("Take a quiz")
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
    files = [i.replace(".csv", "").upper() for i in files ]
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
    mytext = ["Quiz Main Menu"]
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
    keep_looping = True
    while keep_looping == True:
        keep_looping = sub_loop(user_name)

if __name__ == "__main__":
    user_name = "Soyboy227"
    main(user_name)