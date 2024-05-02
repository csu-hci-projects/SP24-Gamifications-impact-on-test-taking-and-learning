import sys, os
import time
import pygame
import utils
import constants
from myclasses import FlashCards
from dialogs import DialogInput, TransitionScreen, QuizDialogInput
'''
# ------------------------------------------------------------
#                    class DialogQuiz
# ------------------------------------------------------------
class DialogQuiz:
    def __init__(self, user_name, quiz_name, percent_threshold=None, quiz_type=None, width=600, height=600, line_width=40):
        self.user_name = user_name
        self.quiz_name = quiz_name
        self.percent_threshold = percent_threshold
        self.quiz_type = quiz_type
        # ---- ---- ---- ----
        self.flashcards = None
        self.current_index = 1
        # --------------------------------------
        self.width = width
        self.height = height
        self.line_width = line_width
        # --------------------------------------
        self.init_pygame()
        self.all_sprites = pygame.sprite.Group()
        # --------------------------------------
        self.input_text_color = constants.UGLY_PINK
        self.text_background_color = constants.LIGHTGREY
        # --------------------------------------
        self.text = ""
        self.user_text = ""
        self.big_window_background_color = constants.WHITE
        self.user_text_rect_background_color = constants.WHITE
        self.text_color = constants.BLACK
        self._initialize_rectangles()
        # --------------------------------------
        self.message = ""
        self.keep_looping = True
        self.x = self.user_rect.x + 10
        self.y = self.user_rect.y

    def read_data(self):
        self.flashcards = FlashCards(self.user_name, self.quiz_name, self.percent_threshold)
        was_successful = self.flashcards.read_data()
        if was_successful not in [True, False]: raise ValueError("Error")
        if was_successful == False:
            return False
        # ---- ----
        self.current_index = 1
        self.display_list = self.flashcards.display_question()
        # ----
        self.choices = ["1", "2", "3", "<SPACE>"]
        s = ", ".join(self.choices)
        self.display_choices = "Choices: {}".format(s)
        return True

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("{}".format(constants.TITLE))
        self.clock = pygame.time.Clock()
        self.BG_COLOR = constants.WHITE
        self.font = pygame.font.Font(None, 35)

    def reload(self):
        self.flashcards = FlashCards(self.user_name, self.quiz_name, self.percent_threshold)
        self.flashcards.read_data()
        self.current_index = 1
        self.display_list = self.flashcards.display_question()
        # ----
        self.choices = ["1", "2", "3", "<SPACE>"]
        s = ", ".join(self.choices)
        self.display_choices = "Choices: {}".format(s)

    def _initialize_rectangles(self):
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        offset = int((long_thin_rectangle_height * 1.25))
        self.user_rect = pygame.Rect(10,
                                     self.height - offset,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)
        self.user_rect2 = pygame.Rect(10,
                                     self.height - offset - 540,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height + 30)
        self.user_rect3 = pygame.Rect(10,
                                     self.height - offset - 465,
                                     long_thin_rectangle_width,
                                     long_thin_rectangle_height)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                self.text_background_color = constants.LIGHTGREY
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.text = self.user_text.lower().strip()
                    if not self.text in self.choices:
                        self.text_background_color = constants.RED
                        self.user_text = ""
                        return False
                    self.display_list, is_correct = self.flashcards.calculate_result(self.text)
                    if is_correct == True:
                        self.BG_COLOR = constants.GREEN1
                    else:
                        self.BG_COLOR = constants.RED1
                    self.text = ""
                    self.user_text = ""
                elif event.key == pygame.K_SPACE:
                    if event.key == pygame.K_n:
                        self.user_text += event.unicode
                    # ----
                    if self.flashcards.answer_was_given() == False:
                        mytext = ["No answer has been given!"]
                        mytext.append(" ")
                        mytext.append("Press <Return> to continue...")
                        mydialog = DialogInput(mytext, [], show_possible_responses=False)
                        mydialog.main()
                        return False
                    # ---- ----
                    self.BG_COLOR = constants.WHITE
                    question_set = self.flashcards.load_next_question()
                    if question_set == False:
                        mytext = []
                        mytext.append(self.flashcards.get_score())
                        mytext.append(" ")
                        mytext.append("Would you like to take the quiz again?")
                        mydialogs = QuizDialogInput(mytext, ["y", "n"])
                        message = mydialogs.main()
                        if message == "y":
                            self.flashcards.save_data()
                            self.reload()
                        elif message == "n":
                            self.flashcards.save_data()
                            self.keep_looping = False
                        else:
                            raise ValueError("Error")
                    elif question_set == True:
                        self.display_list = self.flashcards.display_question()
                    else:
                        raise ValueError("Error")
                else:
                    self.user_text += event.unicode

    def draw(self):
        # -----------------------------------------
        self.screen.fill(self.BG_COLOR)
        if self.keep_looping == True:
            # -----------------------------------------
            pygame.draw.rect(self.screen, constants.GREY5, self.user_rect2)
            pygame.draw.rect(self.screen, constants.GREY6, self.user_rect3)
            # -----------------------------------------
            utils.talk_dialog(self.screen, self.display_list, self.font, width_offset=20,
                              height_offset=20, line_length=60,
                              color=constants.BLACK)
            # -----------------------------------------
            pygame.draw.rect(self.screen, self.text_background_color, self.user_rect)
            # -----------------------------------------
            if len(self.choices) != 0:
                utils.talk_dialog(self.screen, self.display_choices, self.font,
                                  width_offset=self.x, height_offset=self.y-40,
                                  line_length=60,
                                  color=constants.BLACK)
            utils.talk_dialog(self.screen, self.user_text, self.font,
                              width_offset=self.x, height_offset=self.y,
                              line_length=60,
                              color=constants.BLACK)
        pygame.display.flip()

    def main(self):
        while self.keep_looping:
            self.clock.tick(constants.FRAME_RATE)
            self.handle_events()
            self.draw()
'''
# ------------------------------------------------------------
#                    class MultipleChoiceQuiz
# ------------------------------------------------------------
class MultipleChoiceQuiz:
    def __init__(self, user_name, quiz_name, percent_threshold=None, width=600, height=600, line_width=40):
        self.user_name = user_name
        self.quiz_name = quiz_name
        self.percent_threshold = percent_threshold
        self.flashcards = None
        self.current_index = 1
        self.width = width
        self.height = height
        self.line_width = line_width
        self.init_pygame()

    def read_data(self):
        self.flashcards = FlashCards(self.user_name, self.quiz_name, self.percent_threshold)
        was_successful = self.flashcards.read_data()
        if was_successful is not True:
            raise ValueError("Error reading quiz data")

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("{}".format(constants.TITLE))
        self.clock = pygame.time.Clock()
        self.BG_COLOR = constants.WHITE
        self.font = pygame.font.Font(None, 35)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                self.text_background_color = constants.LIGHTGREY
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.text = self.user_text.lower().strip()
                    if not self.text in self.choices:
                        self.text_background_color = constants.RED
                        self.user_text = ""
                        return False
                    self.display_list, is_correct = self.flashcards.calculate_result(self.text)
                    if is_correct == True:
                        self.BG_COLOR = constants.GREEN1
                    else:
                        self.BG_COLOR = constants.RED1
                    self.text = ""
                    self.user_text = ""
                elif event.key == pygame.K_SPACE:
                    if event.key == pygame.K_n:
                        self.user_text += event.unicode
                    if self.flashcards.answer_was_given() == False:
                        mytext = ["No answer has been given!"]
                        mytext.append(" ")
                        mytext.append("Press <Return> to continue...")
                        mydialog = DialogInput(mytext, [], show_possible_responses=False)
                        mydialog.main()
                        return False
                    self.BG_COLOR = constants.WHITE
                    question_set = self.flashcards.load_next_question()
                    if question_set == False:
                        mytext = []
                        mytext.append(self.flashcards.get_score())
                        mytext.append(" ")
                        mytext.append("Would you like to take the quiz again?")
                        mydialogs = QuizDialogInput(mytext, ["y", "n"])
                        message = mydialogs.main()
                        if message == "y":
                            self.flashcards.save_data()
                            self.reload()
                        elif message == "n":
                            self.flashcards.save_data()
                            self.keep_looping = False
                        else:
                            raise ValueError("Error")
                    elif question_set == True:
                        self.display_list = self.flashcards.display_question()
                    else:
                        raise ValueError("Error")
                else:
                    self.user_text += event.unicode

    def draw(self):
        self.screen.fill(self.BG_COLOR)
        if self.keep_looping == True:
            pygame.draw.rect(self.screen, constants.GREY5, self.user_rect2)
            pygame.draw.rect(self.screen, constants.GREY6, self.user_rect3)
            utils.talk_dialog(self.screen, self.display_list, self.font, width_offset=20,
                              height_offset=20, line_length=60,
                              color=constants.BLACK)
            pygame.draw.rect(self.screen, self.text_background_color, self.user_rect)
            if len(self.choices) != 0:
                utils.talk_dialog(self.screen, self.display_choices, self.font,
                                  width_offset=self.x, height_offset=self.y-40,
                                  line_length=60,
                                  color=constants.BLACK)
            utils.talk_dialog(self.screen, self.user_text, self.font,
                              width_offset=self.x, height_offset=self.y,
                              line_length=60,
                              color=constants.BLACK)
        pygame.display.flip()

    def main(self):
        self.read_data()
        self.keep_looping = True
        while self.keep_looping:
            self.clock.tick(constants.FRAME_RATE)
            self.handle_events()
            self.draw()


# ------------------------------------------------------------
#                    class FillInTheBlankQuiz
# ------------------------------------------------------------
class FillInTheBlankQuiz:
    def __init__(self, user_name, quiz_name, percent_threshold=None, width=600, height=600):
        self.width = width
        self.height = height
        self.user_name = user_name
        self.quiz_name = quiz_name
        self.percent_threshold = percent_threshold
        self.init_pygame()
        self.clock = pygame.time.Clock()
        self.prompt_text = "Fill In the Blank:"
        self.font = pygame.font.Font(None, 35)
        self._initialize_rectangles()
        self.text_background_color = constants.LIGHTGREY
        self.BG_COLOR = constants.WHITE
        self.keep_looping = True
        self.read_data()
        self.current_index = 0
        self.correct_counter = 0
        self.user_input = ""
        self.answer_entered = False
        self.quiz_completed = False

    def _initialize_rectangles(self):
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        offset = int((long_thin_rectangle_height * 1.25))
        self.prompt_rect = pygame.Rect(10, 10, self.width - 20, 40)
        self.input_rect = pygame.Rect(10, self.height - offset, long_thin_rectangle_width, long_thin_rectangle_height)

    def read_data(self):
        self.flashcards = csvToArray(self.quiz_name)

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Fill in the Blank Quiz")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 35)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    # Allow backspacing only when quiz is active
                    if not self.quiz_completed:
                        self.user_input = self.user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    # Check if the quiz is active and the user has provided an answer
                    if not self.quiz_completed and len(self.user_input.strip()) > 0:
                        # Mark the user as having entered an answer
                        self.answer_entered = True
                    # If the quiz is completed, allow pressing Enter to exit the quiz
                    elif self.quiz_completed:
                        self.keep_looping = False
                else:
                    # Allow inputting characters only when quiz is active
                    if not self.quiz_completed:
                        self.user_input += event.unicode

    def draw(self):
        self.screen.fill(self.BG_COLOR)

        prompt_surface = self.font.render(self.prompt_text, True, constants.BLACK)
        self.screen.blit(prompt_surface, self.prompt_rect)

        if self.current_index < len(self.flashcards):
            flashcard_key = list(self.flashcards.keys())[self.current_index]
            flashcard_surface = self.font.render(flashcard_key, True, constants.BLACK)
            flashcard_rect = flashcard_surface.get_rect(bottomleft=(self.input_rect.left + 10, self.input_rect.top - 10))
            self.screen.blit(flashcard_surface, flashcard_rect)

            pygame.draw.rect(self.screen, self.text_background_color, self.input_rect)

            input_surface = self.font.render(self.user_input, True, constants.BLACK)
            input_rect = input_surface.get_rect(topleft=(self.input_rect.x + 10, self.input_rect.y + 5))
            self.screen.blit(input_surface, input_rect)

            if self.answer_entered and not self.quiz_completed:
                user_answer = self.user_input.strip().lower()
                correct_answer = self.flashcards[flashcard_key].strip().lower()
                if user_answer == correct_answer:
                    self.correct_counter += 1
                    feedback_text = f"{self.user_input} was Correct!"
                    self.screen.fill(constants.GREEN)
                else:
                    feedback_text = f"{self.user_input} was incorrect. \n The correct answer is: {correct_answer}"
                    self.screen.fill(constants.RED)

                feedback_surface = self.font.render(feedback_text, True, constants.BLACK)
                feedback_rect = feedback_surface.get_rect(center=(self.width // 2, self.height // 2))
                self.screen.blit(feedback_surface, feedback_rect)
                continue_text = "Press Enter to continue"
                continue_surface = self.font.render(continue_text, True, constants.BLACK)
                continue_rect = continue_surface.get_rect(midtop=(self.width // 2, self.height - 50))
                self.screen.blit(continue_surface, continue_rect)

                pygame.display.flip()

                waiting_for_enter = True
                while waiting_for_enter:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                waiting_for_enter = False 

                self.current_index += 1
                self.user_input = ""
                self.answer_entered = False
            else:
                directions = "When field is complete, press enter to continue"
                directions_surface = self.font.render(directions, True, constants.BLACK)
                directions_rect = directions_surface.get_rect(left=10, top=60)
                self.screen.blit(directions_surface, directions_rect)

        else:
            self.quiz_completed = True
            self.keep_looping = False

        pygame.display.flip()

    def display_score_screen(self, time_taken):
        num_correct = self.correct_counter

        total_questions = len(self.flashcards)
        percentage_score = (num_correct / total_questions) * 100 if total_questions > 0 else 0
        
        self.screen.fill(constants.BG_COLOR)  # Use default background color

        summary_text = "Quiz Summary:"
        summary_surface = self.font.render(summary_text, True, constants.BLACK)
        summary_rect = summary_surface.get_rect(center=(self.width // 2, 50))
        self.screen.blit(summary_surface, summary_rect)

        time_text = f"Time Taken: {time_taken:.3f} seconds"
        time_surface = self.font.render(time_text, True, constants.BLACK)
        time_rect = time_surface.get_rect(center=(self.width // 2, 150))
        self.screen.blit(time_surface, time_rect)

        correct_text = f"Correct Answers: {num_correct}/{total_questions}"
        correct_surface = self.font.render(correct_text, True, constants.BLACK)
        correct_rect = correct_surface.get_rect(center=(self.width // 2, 200))
        self.screen.blit(correct_surface, correct_rect)

        percentage_text = f"Percentage Score: {percentage_score:.2f}%"
        percentage_surface = self.font.render(percentage_text, True, constants.BLACK)
        percentage_rect = percentage_surface.get_rect(center=(self.width // 2, 250))
        self.screen.blit(percentage_surface, percentage_rect)

        enter_text = "Press Enter to continue..."
        enter_surface = self.font.render(enter_text, True, constants.BLACK)
        enter_rect = enter_surface.get_rect(center=(self.width // 2, self.height - 50))
        self.screen.blit(enter_surface, enter_rect)

        pygame.display.flip()

        waiting_for_enter = True
        while waiting_for_enter:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting_for_enter = False

    def main(self):
        start_time = time.time()
        while self.keep_looping:
            self.clock.tick(constants.FRAME_RATE)
            self.handle_events()
            self.draw()
        end_time = time.time()
        time_taken = end_time - start_time
        self.display_score_screen(time_taken)


# *********************************************
# *********************************************

def csvToArray(quiz_name):
    filename = "{}.csv".format(quiz_name)
    filepath = os.path.join("data", "quizzes", filename)
    if not os.path.isfile(filepath):
        raise ValueError("File not found: {}".format(filepath))
    
    flashcards = {}
    with open(filepath, 'r') as file:
        for line in file:
            question, answer = line.strip().split(',')
            flashcards[question] = answer

    return flashcards

def handle_multiple_choice_quiz(user_name, quiz_name):
    percent_threshold = 90
    print("MULTIPLE CHOICE SELECTED")
    mydialog = MultipleChoiceQuiz(user_name, quiz_name, percent_threshold)
    was_successful = mydialog.read_data()
    if was_successful:
        mydialog.main()

def handle_fill_in_blank_quiz(user_name, quiz_name):
    percent_threshold = 90
    print("FILL IN THE BLANK SELECTED")
    mydialog = FillInTheBlankQuiz(user_name, quiz_name, percent_threshold)
    mydialog.main()
        
def main(user_name, quiz_name, quiz_type):
    print(f"Starting {quiz_type} quiz: {quiz_name} for user: {user_name}")
    # Dispatching to the appropriate quiz handler based on quiz type
    if quiz_type == "multiple choices":
        handle_multiple_choice_quiz(user_name, quiz_name)
    elif quiz_type == "fill in the blank":
        handle_fill_in_blank_quiz(user_name, quiz_name)
    else:
        raise ValueError("Invalid quiz type selected")

if __name__ == "__main__":
    user_name = "Soyboy227"
    quiz_name = "TestQuiz"
    main(user_name, quiz_name)