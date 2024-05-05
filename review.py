import sys, os
import csv
import time
import random
import pygame
import utils
import constants
import pandas as pd
from dialogs import DialogInput, TransitionScreen, QuizDialogInput

# ------------------------------------------------------------
#                    class ReviewFlashCards
# ------------------------------------------------------------

class ReviewFlashcards:
    def __init__(self, user_name, quiz_name, width=600, height=600):
        self.width = width
        self.height = height
        self.user_name = user_name
        self.quiz_name = quiz_name
        self.BG_COLOR = constants.WHITE
        self.text_background_color = constants.LIGHTGREY
        self.prompt_text = "Reviewing Quiz: "
        self.current_page = 0
        self.flashcards_per_page = 10
        self.flashcards = parse_flashcards(self.quiz_name)
        self.num_flashcards = len(self.flashcards)
        self.num_pages = (self.num_flashcards + self.flashcards_per_page - 1) // self.flashcards_per_page
        self.init_pygame()
        self._initialize_rectangles()
        self.font = pygame.font.Font(None, 35)
        self.keep_looping = True
        self.user_input = ""
        self.chosen_index = 0
        self.input_check = False

    #Function to initialize some default rectangles that need to be rendered
    def _initialize_rectangles(self):
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        offset = int((long_thin_rectangle_height * 1.25))
        self.prompt_rect = pygame.Rect(10, 10, self.width - 20, 40)
        self.input_rect = pygame.Rect(10, self.height - offset, long_thin_rectangle_width, long_thin_rectangle_height)

    #Function to initialize pygame
    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Flashcard Review")

    #Handle events function to deal with user input
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_LEFT:
                    self.current_page = max(0, self.current_page - 1)
                elif event.key == pygame.K_RIGHT:
                    self.current_page = min(self.num_pages - 1, self.current_page + 1)
                elif event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(self.user_input.strip()) > 0:
                        if(utils.is_int(self.user_input)):
                            if(int(self.user_input) > 0 or int(self.user_input) <= self.num_flashcards):
                                #Debug Print Statement
                                #print("USER INPUT IS INT:", self.user_input)
                                self.chosen_index = int(self.user_input) - 1
                                self.keep_looping = False
                                self.input_check = True
                                #Debug Print Statement
                                #print("USER CHOSEN INDEX:", self.chosen_index)
                else:
                    self.user_input += event.unicode
                
    #Draw function to display stuff to the user on the python application
    def draw(self):
        self.screen.fill(self.BG_COLOR)
        prompt_surface = self.font.render(self.prompt_text + self.quiz_name, True, constants.BLACK)
        self.screen.blit(prompt_surface, (10, 10))

        pygame.draw.rect(self.screen, self.text_background_color, self.input_rect)

        directions1 = "Scroll using arrow keys or hit ESC key to exit"
        directions2 = "Type number of a flashcard and hit enter to edit"
        directions_surface1 = self.font.render(directions1, True, constants.BLACK)
        directions_surface2 = self.font.render(directions2, True, constants.BLACK)
        directions_rect1 = directions_surface1.get_rect(left=10, top=40)
        directions_rect2 = directions_surface2.get_rect(left=10, top=70)
        self.screen.blit(directions_surface1, directions_rect1)
        self.screen.blit(directions_surface2, directions_rect2)

        input_surface = self.font.render(self.user_input, True, constants.BLACK)
        input_rect = input_surface.get_rect(topleft=(self.input_rect.x + 10, self.input_rect.y + 5))  # Adjust the position
        self.screen.blit(input_surface, input_rect)

        start_index = self.current_page * self.flashcards_per_page
        end_index = min((self.current_page + 1) * self.flashcards_per_page, self.num_flashcards)

        y_offset = 110
        for i in range(start_index, end_index):
            question = list(self.flashcards.keys())[i]
            answer = self.flashcards[question]
            text = f"{i + 1}. {question} - {answer}"
            text_surface = self.font.render(text, True, constants.BLACK)
            text_rect = text_surface.get_rect(x=20, y=y_offset)
            self.screen.blit(text_surface, text_rect)
            y_offset += 40

        if(len(self.user_input)>0 and not utils.is_int(self.user_input)):
            warning = f"Invalid input. Enter a number between 1 and {self.num_flashcards}"
            warning_surface = self.font.render(warning, True, constants.BLACK)
            warning_rect = warning_surface.get_rect(left = self.prompt_rect.left, top = self.input_rect.bottom-80)
            self.screen.blit(warning_surface, warning_rect)
        elif(len(self.user_input)>0 and utils.is_int(self.user_input)):
            if(int(self.user_input) <= 0 or int(self.user_input) > self.num_flashcards):
                warning = f"Invalid input. Enter a number between 1 and {self.num_flashcards}"
                warning_surface = self.font.render(warning, True, constants.BLACK)
                warning_rect = warning_surface.get_rect(left = self.prompt_rect.left, top = self.input_rect.bottom-80)
                self.screen.blit(warning_surface, warning_rect)

        pygame.display.flip()

    def main(self):
        self.flashcards = parse_flashcards(self.quiz_name)
        self.num_flashcards = len(self.flashcards)
        self.num_pages = (self.num_flashcards + self.flashcards_per_page - 1) // self.flashcards_per_page

        while self.keep_looping:
            self.handle_events()
            self.draw()
        if(self.input_check):
            return self.chosen_index
        else:
            return self.input_check

# ------------------------------------------------------------
#                    class EditFlashcard
# ------------------------------------------------------------     

class EditFlashcard:
    def __init__(self, user_name, quiz_name, chosen_index, width=600, height=600):
        self.width = width
        self.height = height
        self.user_name = user_name
        self.quiz_name = quiz_name
        self.chosen_index = chosen_index
        self.BG_COLOR = constants.WHITE
        self.text_background_color = constants.LIGHTGREY
        self.prompt_text = "Editing a Flashcard: "
        self.flashcards = parse_flashcards(self.quiz_name)
        self._initialize_rectangles()
        self.init_pygame()
        self.font = pygame.font.Font(None, 35)
        self.keep_looping = True
        self.user_input = list(self.flashcards.values())[self.chosen_index]

    #Function to initialize some default rectangles that need to be rendered
    def _initialize_rectangles(self):
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        offset = int((long_thin_rectangle_height * 1.25))
        self.prompt_rect = pygame.Rect(10, 10, self.width - 20, 40)
        self.input_rect = pygame.Rect(10, self.height - offset, long_thin_rectangle_width, long_thin_rectangle_height)

    #Function to initialize pygame
    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Edit Flashcard")

    #Handle events function to deal with user input
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(self.user_input.strip()) > 0:
                        self.keep_looping = False
                        #Debug Print Statement
                        #print("USER Input:", self.user_input)
                else:
                    self.user_input += event.unicode

    #Draw function to display stuff to the user on the python application
    def draw(self):
        self.screen.fill(self.BG_COLOR)

        prompt_surface = self.font.render(self.prompt_text, True, constants.BLACK)
        self.screen.blit(prompt_surface, self.prompt_rect)

        pygame.draw.rect(self.screen, self.text_background_color, self.input_rect)

        input_surface = self.font.render(self.user_input, True, constants.BLACK)
        input_rect = input_surface.get_rect(topleft=(self.input_rect.x + 10, self.input_rect.y + 5))  # Adjust the position
        self.screen.blit(input_surface, input_rect)

        directions1 = "Make edits to your old answer, and hit enter"
        directions2 = "Question:"
        directions3 = f"{list(self.flashcards.keys())[self.chosen_index]}"
        directions4 = "Old Answer:"
        directions5 = f"{list(self.flashcards.values())[self.chosen_index]}"
        directions_surface1 = self.font.render(directions1, True, constants.BLACK)
        directions_surface2 = self.font.render(directions2, True, constants.BLACK)
        directions_surface3 = self.font.render(directions3, True, constants.BLACK)
        directions_surface4 = self.font.render(directions4, True, constants.BLACK)
        directions_surface5 = self.font.render(directions5, True, constants.BLACK)
        directions_rect1 = directions_surface1.get_rect(left=10, top=60)
        directions_rect2 = directions_surface2.get_rect(left=10, top=100)
        directions_rect3 = directions_surface3.get_rect(left=40, top=140)
        directions_rect4 = directions_surface4.get_rect(left=10, top=180)
        directions_rect5 = directions_surface5.get_rect(left=40, top=220)
        self.screen.blit(directions_surface1, directions_rect1)
        self.screen.blit(directions_surface2, directions_rect2)
        self.screen.blit(directions_surface3, directions_rect3)
        self.screen.blit(directions_surface4, directions_rect4)
        self.screen.blit(directions_surface5, directions_rect5)

        pygame.display.flip()
    
    def main(self):
        while self.keep_looping:
            self.handle_events()
            self.draw()
        #Debug Print Statement
        #print("QuizName:", self.quiz_name)
        filename = "{}.csv".format(self.quiz_name)
        filepath = os.path.join("data", "quizzes", filename)
        df = pd.read_csv(filepath, header=None, names=["Question", "Answer"])
        df.loc[self.chosen_index, "Answer"] = self.user_input
        df.to_csv(filepath, header=False, index=False)

#Function that reads csv file into a dict to be used as flashcards
def parse_flashcards(quiz_name):
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

def main(user_name,quiz_name):
    mydialog = ReviewFlashcards(user_name, quiz_name)
    chosen_index = mydialog.main()
    if(utils.is_int(chosen_index)):
        mydialog = EditFlashcard(user_name, quiz_name, chosen_index)
        mydialog.main()

if __name__ == "__main__":
    user_name = "Soyboy227"
    quiz_name = "StateCapitals"
    flashcards_app = ReviewFlashcards(user_name,quiz_name)
    flashcards_app.main()