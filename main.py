import pygame
import os
import random

pygame.init()
pygame.font.init()

#WINDOW
WIDTH, HEIGHT = 580, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle")

#COLORS 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
LIGHT_GREY = (211, 211, 211)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

#FONTS 

TITLE_FONT = pygame.font.SysFont('broadway', 40)
LETTER_FONT = pygame.font.SysFont('helvetica', 35)
ENTER_FONT = pygame.font.SysFont('helvetica', 35)
TITLE_FONT.italic = True

#GAME VARIABLES
GUESS_LIMIT = 6
current_guess = []

WORD_LENGTH = 7
POSSIBLE_WORDS = ["CAPTURE", "SUPPOSE", "FREEDOM", "CONTROL", "MACHINE", "JUSTICE", "CONDUCT", "PROCEED", "ARRANGE", "OPPOSE", "LIBRARY", 
                      "COLLECT", "CENTRAL", "PRESENT", "COMFORT", "DESTROY", "DISCUSS", "JOURNEY", "NETWORK", "PERFORM", "EXPRESS", "PROTECT", 
                      "ACCOUNT", "REQUIRE", "CONTAIN", "ADDRESS", "HISTORY", "EXPLAIN", "MESSAGE", "PROBLEM", "PERFECT", "COMPANY", "CERTAIN", 
                      "PRODUCT", "MENTION", "ELEMENT", "MEASURE", "MISSION", "GENERAL", "CITIZEN", "SERVICE", "FEATURE", "PROMISE", "CONTACT", 
                      "FEATURES", "CAPTURED", "MEASURED", "PREVIOUS", "ANALYSIS", "SYSTEMS", "MOMENTS", "CONVINCE", "DISCOVER", "BROADCAST", 
                      "CONFUSE", "PRAISED", "INTRIGUE", "PROMOTE", "FAVORITE", "LANGUAGE", "REACTION", "MISTAKE", "CORRECT", "MILEAGE", "PLUMMET", 
                      "SCHEDULE", "BROUGHT", "REFUGEE", "FRIENDS", "OFFENSE", "FOCUSED", "LEADING", "OBSERVE", "OVERSEE", "ALLOWS", "ACCEPT", 
                      "DISTANT", "EMOTION", "PERHAPS", "CHOICES", "ATTEMPT", "REMARKS", "REMINDS", "REQUEST", "REPLIES", "CONTENT", "EXAMPLE", 
                      "EXTREME", "INSIGHT", "LIMITED", "RECENT", "SYMBOL", "VERSION"]
random_word_index = random.randint(0, 99)
correct_word = list(POSSIBLE_WORDS[random_word_index])
print(correct_word)

SUPPORTED_CHARACTERS = ["Q","W","E","R","T","Y","U","I","O","P","A","S","D","F","G","H","J","K","L","ENTER","Z","X","C","V","B","N","M","<"]

grid_rectangles = []
grid_buttons = []

#MISC
FPS = 60

class Letter: 
    def __init__(self, left_x, top_y): 
        self.foreground_color = None
        self.background_color = WHITE
        self.outline_color = GREY
        self.left_x = left_x
        self.top_y = top_y
        self.character = None
        self.letter_text = None
        self.WIDTH = 50
        self.HEIGHT = 50

    def draw(self): 

        letter_rect = pygame.Rect(self.left_x, self.top_y, self.WIDTH, self.HEIGHT)

        if self.outline_color != None:
            pygame.draw.rect(WIN, self.outline_color, letter_rect, width = 1)
        else: 
            pygame.draw.rect(WIN, self.background_color, letter_rect)

        

    def type_guess(self, character): 

        if len(current_guess) < WORD_LENGTH:
            
            self.outline_color = BLACK
            self.foreground_color = BLACK
            self.character = character
            self.letter_text = LETTER_FONT.render(self.character, 1, self.foreground_color)
            
            current_guess.append(self.character)
            return True
        
        return False
    
    def delete_guess(self): 

        if len(current_guess) > 0: 
            
            current_guess.pop()
            
            self.outline_color = GREY
            self.foreground_color = None
            self.character = None
            self.letter_text = None
            return True
        
        return False
class Button: 
    def __init__(self, left_x, top_y, character, width): 
        self.foreground_color = BLACK
        self.background_color = LIGHT_GREY
        self.character = character
        self.button_text = LETTER_FONT.render(self.character, 1, self.foreground_color)
        self.left_x = left_x
        self.top_y = top_y
        self.width = width
        self.HEIGHT = 60
        self.button_rect = pygame.Rect(self.left_x, self.top_y, self.width, self.HEIGHT)

    def draw(self): 

        pygame.draw.rect(WIN, self.background_color, self.button_rect)
        if self.character == "ENTER": 
            WIN.blit(self.button_text, (self.left_x + (self.width / 2) - 50, self.top_y + 10))
        else: 
            WIN.blit(self.button_text, (self.left_x + (self.width / 2) - 10, self.top_y + 10))



def draw_window(): 
    
    WIN.fill(WHITE)

    TITLE_TEXT = TITLE_FONT.render("Wordle", 1, BLACK)
    WIN.blit(TITLE_TEXT, (WIDTH // 2 - TITLE_TEXT.get_width() // 2, 25))

    for row in grid_buttons: 
        for col in row: 
            col.draw()

    for row in grid_rectangles: 
        for col in row: 
            col.draw()
            if col.letter_text != None:
                WIN.blit(col.letter_text, (col.left_x + (col.WIDTH / 2) - 10, col.top_y + 5))

    pygame.display.update()

def initialize_rectangles():

    start_y = 100

    for _ in range(6):
        start_x = 100
        row = []
        for _ in range(7): 
            new_letter = Letter(start_x, start_y)
            row.append(new_letter)
            start_x += 55
        grid_rectangles.append(row)
        start_y += 55

        button_y = 450
        button_x = 20
        row1 = []
        for i in range(10):
            new_button = Button(button_x, button_y, SUPPORTED_CHARACTERS[i], 50)
            row1.append(new_button)
            button_x += 55
        grid_buttons.append(row1)

        button_y = 520
        button_x = 50
        row2 = []
        for i in range(10, 19):
            new_button = Button(button_x, button_y, SUPPORTED_CHARACTERS[i], 50)
            row2.append(new_button)
            button_x += 55
        grid_buttons.append(row2)

        

        button_y = 590
        button_x = 20
        row3 = []
        enter_button = Button(button_x, button_y, SUPPORTED_CHARACTERS[19], 120)
        row3.append(enter_button)
        button_x += 125
        for i in range(20, 28):
            new_button = Button(button_x, button_y, SUPPORTED_CHARACTERS[i], 50)
            row3.append(new_button)
            button_x += 55
        grid_buttons.append(row3)

 


def enter_guess(row): 

        
        for i in range(7):
            current_letter = grid_rectangles[row][i]
            if current_guess[i] == correct_word[i]:
                current_letter.background_color = GREEN
            elif current_guess[i] in correct_word: 
                current_letter.background_color = YELLOW
            else: 
                current_letter.background_color = GREY
            current_letter.outline_color = None

        if current_guess == correct_word: 
            return True

        return False


def main():
    
    clock = pygame.time.Clock()
    run = True

    initialize_rectangles()

    
    is_guess_successful = False
    is_deletion_successful = False

    current_guess_row = 0
    current_guess_col = 0
    number_of_guesses = 0
    
    while run: 
        clock.tick(FPS)
        if number_of_guesses >= GUESS_LIMIT: 
            run = False
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                character_input  = None
                for row in grid_buttons: 
                    for col in row: 
                        if col.button_rect.collidepoint(event.pos): 
                            character_input = col.character

                if character_input != None:
                    if character_input == "ENTER": 
                        if current_guess_col != 7: 
                            break
                        is_guess_correct = enter_guess(current_guess_row)
                        if is_guess_correct == True: 
                            print("YOU WON")
                        else: 
                            current_guess.clear()
                            current_guess_row += 1
                            number_of_guesses += 1
                            is_guess_successful = False
                            is_deletion_successful = False
                            current_guess_col = 0
                    elif character_input == "<":
                        if current_guess_col <= 0: 
                            break
                        else: 
                            current_letter = grid_rectangles[current_guess_row][current_guess_col - 1]
                            is_deletion_successful = current_letter.delete_guess()
                            if is_deletion_successful: 
                                current_guess_col -= 1 
                    else:
                        current_letter = grid_rectangles[current_guess_row][current_guess_col]
                        is_guess_successful = current_letter.type_guess(character_input)
                        if is_guess_successful:
                            current_guess_col += 1
                
        draw_window()

if __name__ == "__main__": 
    main()