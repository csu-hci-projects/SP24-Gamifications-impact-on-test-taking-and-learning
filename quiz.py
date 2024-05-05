import sys, os
import time
import random
import pygame
import utils
import constants
from dialogs import DialogInput, TransitionScreen, QuizDialogInput

# ------------------------------------------------------------
#                    class MultipleChoiceQuiz
# ------------------------------------------------------------

class MultipleChoiceQuiz:
    def __init__(self, user_name, quiz_name, width=600, height=600):
        self.width = width
        self.height = height
        self.user_name = user_name
        self.quiz_name = quiz_name
        self.init_pygame()
        self.prompt_text = "Multiple Choice:"
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
        self.input_inbounds = True
        self.answer_options = []
        self.correct_answer_index = 0

    #Function to initialize some default rectangles that need to be rendered
    def _initialize_rectangles(self):
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        offset = int((long_thin_rectangle_height * 1.25))
        self.prompt_rect = pygame.Rect(10, 10, self.width - 20, 40)
        self.input_rect = pygame.Rect(10, self.height - offset, long_thin_rectangle_width, long_thin_rectangle_height)

    #Function to read from the csv file user created and make into flashcards
    def read_data(self):
        self.flashcards = csvToArray(self.quiz_name)

    #Function to shuffle the multiple choice answers shown to the user
    def shuffle_answers(self, index):
        correct_answer = list(self.flashcards.values())[index]
        all_answers = list(self.flashcards.values())
        all_answers.remove(correct_answer)

        random.shuffle(all_answers)
        answer_options = all_answers[:3]

        insert_index = random.randint(0, 3)
        answer_options.insert(insert_index, correct_answer)

        return answer_options, insert_index

    #Function to initialize pygame
    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Multiple Choice Quiz")
        self.font = pygame.font.Font(None, 35)

    #Handle events function to deal with user input
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    if not self.quiz_completed:
                        self.user_input = self.user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if not self.quiz_completed and len(self.user_input.strip()) > 0:
                        if self.user_input.strip().upper() in ['A', 'B', 'C', 'D']:
                            self.answer_entered = True
                            self.input_inbounds = True
                        else:
                            self.input_inbounds = False
                            #Debug print statement
                            #print("Invalid input. Please enter A, B, C, or D.")
                    elif self.quiz_completed:
                        self.keep_looping = False
                else:
                    if not self.quiz_completed:
                        self.user_input += event.unicode

    #Draw function to display stuff to the user on the python application
    def draw(self):
        self.screen.fill(self.BG_COLOR)

        prompt_surface = self.font.render(self.prompt_text, True, constants.BLACK)
        self.screen.blit(prompt_surface, self.prompt_rect)

        if self.current_index < len(self.flashcards):

            directions = "When field is complete, press enter to continue"
            directions_surface = self.font.render(directions, True, constants.BLACK)
            directions_rect = directions_surface.get_rect(left = self.prompt_rect.left, top = self.prompt_rect.bottom+10)
            self.screen.blit(directions_surface, directions_rect)

            question = list(self.flashcards.keys())[self.current_index]
            question_surface = self.font.render("Question: " + question, True, constants.BLACK)
            question_rect = question_surface.get_rect(topleft=(directions_rect.left, directions_rect.bottom + 10))
            self.screen.blit(question_surface, question_rect)

            answer_option1 = self.answer_options[self.current_index][0][0]
            answer_surface1 = self.font.render("A) " + answer_option1, True, constants.BLACK)
            answer_rect1 = answer_surface1.get_rect(topleft=(question_rect.left, question_rect.bottom + 10))
            self.screen.blit(answer_surface1, answer_rect1)

            answer_option2 = self.answer_options[self.current_index][0][1]
            answer_surface2 = self.font.render("B) " + answer_option2, True, constants.BLACK)
            answer_rect2 = answer_surface2.get_rect(topleft=(answer_rect1.left, answer_rect1.bottom + 10))
            self.screen.blit(answer_surface2, answer_rect2)

            answer_option3 = self.answer_options[self.current_index][0][2]
            answer_surface3 = self.font.render("C) " + answer_option3, True, constants.BLACK)
            answer_rect3 = answer_surface3.get_rect(topleft=(answer_rect2.left, answer_rect2.bottom + 10))
            self.screen.blit(answer_surface3, answer_rect3)

            answer_option4 = self.answer_options[self.current_index][0][3]
            answer_surface4 = self.font.render("D) " + answer_option4, True, constants.BLACK)
            answer_rect4 = answer_surface4.get_rect(topleft=(answer_rect3.left, answer_rect3.bottom + 10))
            self.screen.blit(answer_surface4, answer_rect4)

            pygame.draw.rect(self.screen, self.text_background_color, self.input_rect)


            input_surface = self.font.render(self.user_input, True, constants.BLACK)
            input_rect = input_surface.get_rect(topleft=(self.input_rect.x + 10, self.input_rect.y + 5))
            self.screen.blit(input_surface, input_rect)
            pygame.display.flip()

            if self.answer_entered and not self.quiz_completed:
                self.correct_answer_index = self.answer_options[self.current_index][1]
                correct_answer = self.answer_options[self.current_index][0][self.correct_answer_index]
                correct_letter = letter = chr(ord('A') + self.correct_answer_index)
                user_answer = self.user_input.strip().upper()
                selected_answer_index = ord(user_answer) - ord('A')
                user_answer_spelled = self.answer_options[self.current_index][0][selected_answer_index]
                if selected_answer_index == self.correct_answer_index:
                    self.correct_counter += 1
                    feedback_text = f"Choice {self.user_input} ({correct_answer}) was Correct!"
                    self.screen.fill(constants.GREEN)
                    feedback_surface = self.font.render(feedback_text, True, constants.BLACK)
                    feedback_rect = feedback_surface.get_rect(center=(self.width // 2, self.height // 2))
                    self.screen.blit(feedback_surface, feedback_rect)
                else:
                    feedback_line1 = f"Choice {self.user_input} ({user_answer_spelled}) was incorrect."
                    feedback_line2 = f"The correct answer was: {correct_letter} ({correct_answer})"
                    self.screen.fill(constants.RED)
                    feedback_surface_line1 = self.font.render(feedback_line1, True, constants.BLACK)
                    feedback_rect_line1 = feedback_surface_line1.get_rect(center=(self.width // 2, self.height // 2 - 20))
                    self.screen.blit(feedback_surface_line1, feedback_rect_line1)

                    feedback_surface_line2 = self.font.render(feedback_line2, True, constants.BLACK)
                    feedback_rect_line2 = feedback_surface_line2.get_rect(center=(self.width // 2, self.height // 2 + 20))
                    self.screen.blit(feedback_surface_line2, feedback_rect_line2)

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
                            elif event.type == pygame.TEXTINPUT:
                                if event.text.isalpha() and len(self.user_input) < 1:
                                    self.user_input += event.text

                self.current_index += 1
                self.user_input = ""
                self.answer_entered = False
            elif (len(self.user_input)>0 and not self.user_input.strip().upper() in ['A', 'B', 'C', 'D']):
                warning = "Invalid input. Please enter A, B, C, or D."
                warning_surface = self.font.render(warning, True, constants.BLACK)
                warning_rect = warning_surface.get_rect(left = self.prompt_rect.left, top = self.input_rect.bottom-80)
                self.screen.blit(warning_surface, warning_rect)

        else:
            self.quiz_completed = True
            self.keep_looping = False

        pygame.display.flip()

    #Function to display the quiz results to the user upon quiz completion
    def display_score_screen(self, time_taken):
        num_correct = self.correct_counter

        total_questions = len(self.flashcards)
        percentage_score = (num_correct / total_questions) * 100 if total_questions > 0 else 0
        
        self.screen.fill(constants.PURPLE3)

        summary_text = "Multiple Choice Quiz Summary:"
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
        self.answer_options = []
        #Debug print statement
        #print(self.flashcards)
        for index in range(len(self.flashcards)):
            shuffled_answers = self.shuffle_answers(index)
            self.answer_options.append(shuffled_answers)

        start_time = time.time()
        self.keep_looping = True
        while self.keep_looping:
            self.handle_events()
            self.draw()
        end_time = time.time()
        time_taken = end_time - start_time
        self.display_score_screen(time_taken)


# ------------------------------------------------------------
#                    class FillInTheBlankQuiz
# ------------------------------------------------------------
class FillInTheBlankQuiz:
    def __init__(self, user_name, quiz_name, width=600, height=600):
        self.width = width
        self.height = height
        self.user_name = user_name
        self.quiz_name = quiz_name
        self.init_pygame()
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

    #Function to initialize some default rectangles that need to be rendered
    def _initialize_rectangles(self):
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        offset = int((long_thin_rectangle_height * 1.25))
        self.prompt_rect = pygame.Rect(10, 10, self.width - 20, 40)
        self.input_rect = pygame.Rect(10, self.height - offset, long_thin_rectangle_width, long_thin_rectangle_height)

    #Function to read from the csv file user created and make into flashcards
    def read_data(self):
        self.flashcards = csvToArray(self.quiz_name)

    #Function to initialize pygame
    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Fill in the Blank Quiz")
        self.font = pygame.font.Font(None, 35)

    #Handle events function to deal with user input
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    if not self.quiz_completed:
                        self.user_input = self.user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if not self.quiz_completed and len(self.user_input.strip()) > 0:
                        self.answer_entered = True
                    elif self.quiz_completed:
                        self.keep_looping = False
                else:
                    if not self.quiz_completed:
                        self.user_input += event.unicode

    #Draw function to display stuff to the user on the python application
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
                    feedback_text = f"\"{self.user_input}\" was Correct!"
                    self.screen.fill(constants.GREEN)
                    feedback_surface = self.font.render(feedback_text, True, constants.BLACK)
                    feedback_rect = feedback_surface.get_rect(center=(self.width // 2, self.height // 2))
                    self.screen.blit(feedback_surface, feedback_rect)
                else:
                    feedback_line1 = f"\"{self.user_input}\" was incorrect."
                    feedback_line2 = f"The correct answer is: \"{correct_answer}\""
                    self.screen.fill(constants.RED)
                    feedback_surface_line1 = self.font.render(feedback_line1, True, constants.BLACK)
                    feedback_rect_line1 = feedback_surface_line1.get_rect(center=(self.width // 2, self.height // 2 - 20))
                    self.screen.blit(feedback_surface_line1, feedback_rect_line1)

                    feedback_surface_line2 = self.font.render(feedback_line2, True, constants.BLACK)
                    feedback_rect_line2 = feedback_surface_line2.get_rect(center=(self.width // 2, self.height // 2 + 20))
                    self.screen.blit(feedback_surface_line2, feedback_rect_line2)

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

    #Function to display the quiz results to the user upon quiz completion
    def display_score_screen(self, time_taken):
        num_correct = self.correct_counter

        total_questions = len(self.flashcards)
        percentage_score = (num_correct / total_questions) * 100 if total_questions > 0 else 0
        
        self.screen.fill(constants.PURPLE3)

        summary_text = "Fill In the Blank Quiz Summary:"
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
            self.handle_events()
            self.draw()
        end_time = time.time()
        time_taken = end_time - start_time
        self.display_score_screen(time_taken)

# ------------------------------------------------------------
#                    class MixedQuiz
# ------------------------------------------------------------
class MixedQuiz:
    def __init__(self, user_name, quiz_name, width=600, height=600):
        self.width = width
        self.height = height
        self.user_name = user_name
        self.quiz_name = quiz_name
        self.init_pygame()
        self.prompt_text = "Mixed Choice:"
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
        self.input_inbounds = True
        self.answer_options = []
        self.correct_answer_index = 0
        self.option_choice = []

    #Function to initialize some default rectangles that need to be rendered
    def _initialize_rectangles(self):
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        offset = int((long_thin_rectangle_height * 1.25))
        self.prompt_rect = pygame.Rect(10, 10, self.width - 20, 40)
        self.input_rect = pygame.Rect(10, self.height - offset, long_thin_rectangle_width, long_thin_rectangle_height)

    #Function to read from the csv file user created and make into flashcards
    def read_data(self):
        self.flashcards = csvToArray(self.quiz_name)

    #Function to shuffle the multiple choice answers shown to the user
    def shuffle_answers(self, index):
        correct_answer = list(self.flashcards.values())[index]
        all_answers = list(self.flashcards.values())
        all_answers.remove(correct_answer)

        random.shuffle(all_answers)
        answer_options = all_answers[:3]

        insert_index = random.randint(0, 3)
        answer_options.insert(insert_index, correct_answer)

        return answer_options, insert_index

    #Function to initialize pygame
    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Mixed Quiz")
        self.font = pygame.font.Font(None, 35)

    #Handle events function to deal with user input
    def handle_events(self):
        if self.current_index < len(self.flashcards):
            if self.option_choice[self.current_index]:
                self.prompt_text = "Multiple Choice:"
                #Multiple Choice
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.keep_looping = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.keep_looping = False
                        elif event.key == pygame.K_BACKSPACE:
                            if not self.quiz_completed:
                                self.user_input = self.user_input[:-1]
                        elif event.key == pygame.K_RETURN:
                            if not self.quiz_completed and len(self.user_input.strip()) > 0:
                                if self.user_input.strip().upper() in ['A', 'B', 'C', 'D']:
                                    self.answer_entered = True
                                    self.input_inbounds = True
                                else:
                                    self.input_inbounds = False
                                    #Debug print statement
                                    #print("Invalid input. Please enter A, B, C, or D.")
                            elif self.quiz_completed:
                                self.keep_looping = False
                        else:
                            if not self.quiz_completed:
                                self.user_input += event.unicode
            else:
                #Fill In the Blank
                self.prompt_text = "Fill In The Blank:"
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.keep_looping = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.keep_looping = False
                        elif event.key == pygame.K_BACKSPACE:
                            if not self.quiz_completed:
                                self.user_input = self.user_input[:-1]
                        elif event.key == pygame.K_RETURN:
                            if not self.quiz_completed and len(self.user_input.strip()) > 0:
                                self.answer_entered = True
                            elif self.quiz_completed:
                                self.keep_looping = False
                        else:
                            if not self.quiz_completed:
                                self.user_input += event.unicode
        else:
            self.quiz_completed = True
            self.keep_looping = False

    #Draw function to display stuff to the user on the python application
    def draw(self):
        if self.current_index < len(self.flashcards):
            if self.option_choice[self.current_index]:
                #Multiple Choice
                self.screen.fill(self.BG_COLOR)

                prompt_surface = self.font.render(self.prompt_text, True, constants.BLACK)
                self.screen.blit(prompt_surface, self.prompt_rect)

                if self.current_index < len(self.flashcards):

                    directions = "When field is complete, press enter to continue"
                    directions_surface = self.font.render(directions, True, constants.BLACK)
                    directions_rect = directions_surface.get_rect(left = self.prompt_rect.left, top = self.prompt_rect.bottom+10)
                    self.screen.blit(directions_surface, directions_rect)

                    question = list(self.flashcards.keys())[self.current_index]
                    question_surface = self.font.render("Question: " + question, True, constants.BLACK)
                    question_rect = question_surface.get_rect(topleft=(directions_rect.left, directions_rect.bottom + 10))
                    self.screen.blit(question_surface, question_rect)

                    answer_option1 = self.answer_options[self.current_index][0][0]
                    answer_surface1 = self.font.render("A) " + answer_option1, True, constants.BLACK)
                    answer_rect1 = answer_surface1.get_rect(topleft=(question_rect.left, question_rect.bottom + 10))
                    self.screen.blit(answer_surface1, answer_rect1)

                    answer_option2 = self.answer_options[self.current_index][0][1]
                    answer_surface2 = self.font.render("B) " + answer_option2, True, constants.BLACK)
                    answer_rect2 = answer_surface2.get_rect(topleft=(answer_rect1.left, answer_rect1.bottom + 10))
                    self.screen.blit(answer_surface2, answer_rect2)

                    answer_option3 = self.answer_options[self.current_index][0][2]
                    answer_surface3 = self.font.render("C) " + answer_option3, True, constants.BLACK)
                    answer_rect3 = answer_surface3.get_rect(topleft=(answer_rect2.left, answer_rect2.bottom + 10))
                    self.screen.blit(answer_surface3, answer_rect3)

                    answer_option4 = self.answer_options[self.current_index][0][3]
                    answer_surface4 = self.font.render("D) " + answer_option4, True, constants.BLACK)
                    answer_rect4 = answer_surface4.get_rect(topleft=(answer_rect3.left, answer_rect3.bottom + 10))
                    self.screen.blit(answer_surface4, answer_rect4)

                    pygame.draw.rect(self.screen, self.text_background_color, self.input_rect)


                    input_surface = self.font.render(self.user_input, True, constants.BLACK)
                    input_rect = input_surface.get_rect(topleft=(self.input_rect.x + 10, self.input_rect.y + 5))
                    self.screen.blit(input_surface, input_rect)
                    pygame.display.flip()

                    if self.answer_entered and not self.quiz_completed and self.input_inbounds:
                        self.correct_answer_index = self.answer_options[self.current_index][1]
                        correct_answer = self.answer_options[self.current_index][0][self.correct_answer_index]
                        correct_letter = letter = chr(ord('A') + self.correct_answer_index)
                        user_answer = self.user_input.strip().upper()
                        selected_answer_index = ord(user_answer) - ord('A')
                        user_answer_spelled = self.answer_options[self.current_index][0][selected_answer_index]
                        if selected_answer_index == self.correct_answer_index:
                            self.correct_counter += 1
                            feedback_text = f"Choice {self.user_input} ({correct_answer}) was Correct!"
                            self.screen.fill(constants.GREEN)
                            feedback_surface = self.font.render(feedback_text, True, constants.BLACK)
                            feedback_rect = feedback_surface.get_rect(center=(self.width // 2, self.height // 2))
                            self.screen.blit(feedback_surface, feedback_rect)
                        else:
                            feedback_line1 = f"Choice {self.user_input} ({user_answer_spelled}) was incorrect."
                            feedback_line2 = f"The correct answer was: {correct_letter} ({correct_answer})"
                            self.screen.fill(constants.RED)
                            feedback_surface_line1 = self.font.render(feedback_line1, True, constants.BLACK)
                            feedback_rect_line1 = feedback_surface_line1.get_rect(center=(self.width // 2, self.height // 2 - 20))
                            self.screen.blit(feedback_surface_line1, feedback_rect_line1)

                            feedback_surface_line2 = self.font.render(feedback_line2, True, constants.BLACK)
                            feedback_rect_line2 = feedback_surface_line2.get_rect(center=(self.width // 2, self.height // 2 + 20))
                            self.screen.blit(feedback_surface_line2, feedback_rect_line2)

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
                                    elif event.type == pygame.TEXTINPUT:
                                        if event.text.isalpha() and len(self.user_input) < 1:
                                            self.user_input += event.text

                        self.current_index += 1
                        self.user_input = ""
                        self.answer_entered = False
                    elif not self.input_inbounds:
                        warning = "Invalid input. Please enter A, B, C, or D."
                        warning_surface = self.font.render(warning, True, constants.BLACK)
                        warning_rect = warning_surface.get_rect(left = self.prompt_rect.left, top = self.input_rect.bottom-80)
                        self.screen.blit(warning_surface, warning_rect)

                else:
                    self.quiz_completed = True
                    self.keep_looping = False

                pygame.display.flip()
            else:
                #Fill In the Blank
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
                            feedback_text = f"\"{self.user_input}\" was Correct!"
                            self.screen.fill(constants.GREEN)
                            feedback_surface = self.font.render(feedback_text, True, constants.BLACK)
                            feedback_rect = feedback_surface.get_rect(center=(self.width // 2, self.height // 2))
                            self.screen.blit(feedback_surface, feedback_rect)
                        else:
                            feedback_line1 = f"\"{self.user_input}\" was incorrect."
                            feedback_line2 = f"The correct answer is: \"{correct_answer}\""
                            self.screen.fill(constants.RED)
                            feedback_surface_line1 = self.font.render(feedback_line1, True, constants.BLACK)
                            feedback_rect_line1 = feedback_surface_line1.get_rect(center=(self.width // 2, self.height // 2 - 20))
                            self.screen.blit(feedback_surface_line1, feedback_rect_line1)

                            feedback_surface_line2 = self.font.render(feedback_line2, True, constants.BLACK)
                            feedback_rect_line2 = feedback_surface_line2.get_rect(center=(self.width // 2, self.height // 2 + 20))
                            self.screen.blit(feedback_surface_line2, feedback_rect_line2)

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
        else:
            self.quiz_completed = True
            self.keep_looping = False

    #Function to display the quiz results to the user upon quiz completion
    def display_score_screen(self, time_taken):
        num_correct = self.correct_counter

        total_questions = len(self.flashcards)
        percentage_score = (num_correct / total_questions) * 100 if total_questions > 0 else 0
        
        self.screen.fill(constants.PURPLE3)

        summary_text = "Mixed Quiz Summary:"
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
        self.answer_options = []
        #Debug print statement
        #print(self.flashcards)
        for index in range(len(self.flashcards)):
            shuffled_answers = self.shuffle_answers(index)
            self.answer_options.append(shuffled_answers)

        self.option_choice = [bool(random.getrandbits(1)) for _ in range(len(self.flashcards))]
        #Debug print statement
        #print(self.option_choice)
        
        for index in range(len(self.flashcards)):
            self.option_choice

        start_time = time.time()
        self.keep_looping = True
        while self.keep_looping:
            self.handle_events()
            self.draw()
        end_time = time.time()
        time_taken = end_time - start_time
        self.display_score_screen(time_taken)
    
# *********************************************
# *********************************************

#Function to convert a csv file into flashcards the user can view
#Function also shuffles the questions up to not appear repetitive
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

    #Debug print statement
    #print("UNSHUFFLED CARDS:", flashcards)
    temp = list(flashcards.items())
    random.shuffle(temp)
    flashcards_shuffled = dict(temp)
    #Debug print statement
    #print("SHUFFLED CARDS: ", flashcards_shuffled)
    return flashcards_shuffled

#Handler for when multiple choice is selected by user
def handle_multiple_choice_quiz(user_name, quiz_name):
    #Debug print statement
    #print("MULTIPLE CHOICE SELECTED")
    mydialog = MultipleChoiceQuiz(user_name, quiz_name)
    mydialog.main()

#Handler for when fill in the blank is selected by user
def handle_fill_in_blank_quiz(user_name, quiz_name):
    #Debug print statement
    #print("FILL IN THE BLANK SELECTED")
    mydialog = FillInTheBlankQuiz(user_name, quiz_name)
    mydialog.main()

#Handler for when a mix of multiple choice/fill in the blank is selected by user
def handle_mixed_quiz(user_name, quiz_name):
    #Debug print statement
    #print("MIXED QUIZ SELECTED")
    mydialog = MixedQuiz(user_name, quiz_name)
    mydialog.main()
        
def main(user_name, quiz_name, quiz_type):
    #Debug print statement
    #print(f"Starting {quiz_type} quiz: {quiz_name} for user: {user_name}")

    # Selecting appropriate quiz handler based on quiz type
    if quiz_type == "multiple choices":
        handle_multiple_choice_quiz(user_name, quiz_name)
    elif quiz_type == "fill in the blank":
        handle_fill_in_blank_quiz(user_name, quiz_name)
    elif quiz_type == "mixed quiz":
        handle_mixed_quiz(user_name, quiz_name)
    else:
        raise ValueError("Invalid quiz type selected")

if __name__ == "__main__":
    user_name = "Soyboy227"
    quiz_name = "StateCapitals"
    quiz_type = "mixed quiz"
    main(user_name, quiz_name, quiz_type)