import csv
import sys, os
import pygame
import utils
import constants
from myclasses import FlashCards
from dialogs import DialogInput, TransitionScreen, QuizDialogInput

# ------------------------------------------------------------
#                    class CreateQuizName
# ------------------------------------------------------------

class CreateQuizName:
    def __init__(self, width=600, height=600):
        self.width = width
        self.height = height
        self.init_pygame()
        self.clock = pygame.time.Clock()
        self.quiz_name = ""
        self.prompt_text = "Enter the name for your quiz:"
        self.font = pygame.font.Font(None, 35)
        self._initialize_rectangles()
        self.text_background_color = constants.LIGHTGREY
        self.BG_COLOR = constants.WHITE
        self.keep_looping = True

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Quiz Name Input")

    def _initialize_rectangles(self):
        long_thin_rectangle_width = self.width - 20
        long_thin_rectangle_height = 45
        offset = int((long_thin_rectangle_height * 1.25))
        self.prompt_rect = pygame.Rect(10, 10, self.width - 20, 40)
        self.input_rect = pygame.Rect(10, self.height - offset, long_thin_rectangle_width, long_thin_rectangle_height)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    self.quiz_name = self.quiz_name[:-1]
                elif event.key == pygame.K_RETURN:
                    self.keep_looping = False
                else:
                    self.quiz_name += event.unicode

    def draw(self):
        self.screen.fill(self.BG_COLOR)

        prompt_surface = self.font.render(self.prompt_text, True, constants.BLACK)
        self.screen.blit(prompt_surface, self.prompt_rect)

        pygame.draw.rect(self.screen, self.text_background_color, self.input_rect)

        # Render the input text surface
        input_surface = self.font.render(self.quiz_name, True, constants.BLACK)
        input_rect = input_surface.get_rect(topleft=(self.input_rect.x + 10, self.input_rect.y + 5))  # Adjust the position
        self.screen.blit(input_surface, input_rect)
        pygame.display.flip()

    def main(self):
        while self.keep_looping:
            self.clock.tick(constants.FRAME_RATE)
            self.handle_events()
            self.draw()
        return self.quiz_name

# ------------------------------------------------------------
#                    class CreateQuizQuestions
# ------------------------------------------------------------

class CreateQuizQuestions:
    def __init__(self, quiz_name, width=800, height=600):
        self.quiz_name = quiz_name
        self.width = width
        self.height = height
        self.init_pygame()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 35)
        self.question = ""
        self.answer = ""
        self.prompt_text = "Enter a question:"
        self.prompt_text_answer = "Enter the answer:"
        self.text_background_color = constants.LIGHTGREY
        self.BG_COLOR = constants.WHITE
        self.keep_looping = True
        self.input_rect = pygame.Rect(10, 50, self.width - 20, 40)

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Create Quiz Questions")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key == pygame.K_RETURN:
                    if self.answer:  # Save the question-answer pair when both are provided
                        self.add_question_to_csv()
                        self.question = ""
                        self.answer = ""
                        self.prompt_text = "Enter a question:"
                        self.prompt_text_answer = "Enter the answer:"
                    elif self.question:  # Switch to answer input when question is provided
                        self.prompt_text = self.prompt_text_answer
                    else:
                        self.keep_looping = False
                elif event.key == pygame.K_BACKSPACE:
                    if self.prompt_text == self.prompt_text_answer:
                        self.answer = self.answer[:-1]
                    else:
                        self.question = self.question[:-1]
                else:
                    if self.prompt_text == self.prompt_text_answer:
                        self.answer += event.unicode
                    else:
                        self.question += event.unicode

    def draw(self):
        self.screen.fill(self.BG_COLOR)

        # Draw question prompt
        prompt_surface = self.font.render(self.prompt_text, True, constants.BLACK)
        self.screen.blit(prompt_surface, (10, 10))

        # Draw input rectangle
        pygame.draw.rect(self.screen, self.text_background_color, self.input_rect)

        # Render the input text surface
        if self.prompt_text == self.prompt_text_answer:
            input_surface = self.font.render(self.answer, True, constants.BLACK)
        else:
            input_surface = self.font.render(self.question, True, constants.BLACK)
        input_rect = input_surface.get_rect(topleft=(self.input_rect.x + 10, self.input_rect.y + 5))
        self.screen.blit(input_surface, input_rect)

        pygame.display.flip()

    def add_question_to_csv(self):
        file_path = os.path.join("data", "quizzes", f"{self.quiz_name}.csv")
        with open(file_path, "a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([self.question, self.answer])

    def main(self):
        while self.keep_looping:
            self.clock.tick(constants.FRAME_RATE)
            self.handle_events()
            self.draw()

def main():
    mydialog = CreateQuizName()
    quiz_name = mydialog.main()
    print("QUIZ NAME IS: ", quiz_name)
    mydialog = CreateQuizQuestions(quiz_name)
    mydialog.main()
    

if __name__ == "__main__":
    main()
