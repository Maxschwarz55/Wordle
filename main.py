import pygame
import os

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
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

#FONTS 

TITLE_FONT = pygame.font.SysFont('broadway', 40)
LETTER_FONT = pygame.font.SysFont('helvetica', 35)
TITLE_FONT.italic = True

#GAME VARIABLES
GUESS_LIMIT = 6
current_guess = []

WORD_LENGTH = 7
correct_word = ["B", "A", "A", "A", "A", "A", "B"]

grid_rectangles = []

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
    

def draw_window(): 
    
    WIN.fill(WHITE)

    TITLE_TEXT = TITLE_FONT.render("Wordle", 1, BLACK)
    WIN.blit(TITLE_TEXT, (WIDTH // 2 - TITLE_TEXT.get_width() // 2, 25))

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
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_a and current_guess_col < 7:
                    current_letter = grid_rectangles[current_guess_row][current_guess_col]
                    is_guess_successful = current_letter.type_guess("A")
                    if is_guess_successful:
                        current_guess_col += 1
                if event.key == pygame.K_b and current_guess_col < 7: 
                    current_letter = grid_rectangles[current_guess_row][current_guess_col]
                    is_guess_successful = current_letter.type_guess("B")
                    if is_guess_successful:
                        current_guess_col += 1
                if event.key == pygame.K_c and current_guess_col < 7: 
                    current_letter = grid_rectangles[current_guess_row][current_guess_col]
                    is_guess_successful = current_letter.type_guess("C")
                    if is_guess_successful:
                        current_guess_col += 1         
                if event.key == pygame.K_BACKSPACE and current_guess_col > 0: 
                    current_letter = grid_rectangles[current_guess_row][current_guess_col - 1]
                    is_deletion_successful = current_letter.delete_guess()
                    if is_deletion_successful: 
                        current_guess_col -= 1
                if event.key == pygame.K_RETURN and current_guess_col == 7:
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
                
        draw_window()

if __name__ == "__main__": 
    main()