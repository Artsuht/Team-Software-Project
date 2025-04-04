import pygame
import sys
import os
import random  # random word selection

os.chdir("C:\\Users\\AWhit\OneDrive\\Desktop\\game project")  # specify working directory!!
pygame.init()

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("WrdGuessr")

# Colour for that highlight
YELLOW = (255, 255, 0)

# Menu images
background = pygame.image.load("main.png").convert()
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

BUTTON_WIDTH = 250
BUTTON_HEIGHT = 125
start_img = pygame.image.load("start.png").convert_alpha()
start_img = pygame.transform.scale(start_img, (BUTTON_WIDTH, BUTTON_HEIGHT))
quit_img = pygame.image.load("quit.png").convert_alpha()
quit_img = pygame.transform.scale(quit_img, (BUTTON_WIDTH, BUTTON_HEIGHT))
menu_img = pygame.image.load("menu.png").convert_alpha()
menu_img = pygame.transform.scale(menu_img, (BUTTON_WIDTH, BUTTON_HEIGHT))
next_img = pygame.image.load("next.png").convert_alpha()  
next_img = pygame.transform.scale(next_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

# In-game assets
game_background = pygame.image.load("game-screen 1.png").convert()
game_background = pygame.transform.scale(game_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
dash_img = pygame.image.load("dash.png").convert_alpha()
dash_img = pygame.transform.scale(dash_img, (50, 20)) 
with open("word set.txt", "r") as file:
    word_hint_pairs = [line.strip().split(":") for line in file.readlines()]
    words = [pair[0].lower() for pair in word_hint_pairs]  # Extract just the words
    hints = [pair[1] for pair in word_hint_pairs]  # Extract hints
guessed_letters = set()
lives = 5  # track player errors
hangman_images = [pygame.transform.scale(pygame.image.load(f"{i}.png").convert_alpha(), (800, 700)) for i in range(9)]  # define hangman image and its size
current_image_index = 8  # keep track of current hangman image

font = pygame.font.SysFont("comic sans ms", 46, bold=True)
font2 = pygame.font.SysFont("times new roman", 64, bold=True)

class Button:
    def __init__(self, image, x, y):
        self.original_image = image
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.scale_factor = 0.9
        self.is_hovered = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.is_hovered:
            pygame.draw.rect(surface, YELLOW, self.rect, 2)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        if self.is_hovered:
            scaled_size = (int(self.original_image.get_width() * self.scale_factor),
                          int(self.original_image.get_height() * self.scale_factor))
            self.image = pygame.transform.scale(self.original_image, scaled_size)
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        else:
            self.image = self.original_image
            self.rect = self.original_image.get_rect(topleft=self.rect.topleft)
        return self.is_hovered
    
    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Position buttons
button_x = WINDOW_WIDTH - 400  # 880
start_button = Button(start_img, button_x, 150)  # MENU (Start)
quit_button = Button(quit_img, button_x, 350)  # MENU (Quit)
menu_button = Button(menu_img, button_x, 350)  # WIN_ALL (Menu)
game_quit_button = Button(quit_img, 10, WINDOW_HEIGHT - BUTTON_HEIGHT - 10)  # GAME (Quit)
game_menu_button = Button(menu_img, WINDOW_WIDTH - BUTTON_WIDTH - 10, WINDOW_HEIGHT - BUTTON_HEIGHT - 10)  # GAME (Menu)
success_loss_menu_button = Button(menu_img, button_x, 100)  # SUCCESS (Menu)
next_button = Button(next_img, button_x, 250)  # SUCCESS (Next, renamed from success_next_button)
success_loss_quit_button = Button(quit_img, button_x, 400)  # SUCCESS (Quit)

def get_unused_word_index(difficulty):
    ranges = {"EASY": (0, 99), "MEDIUM": (100, 199), "HARD": (200, 299), "EXTREME": (300, 399)}
    min_idx, max_idx = ranges[difficulty]
    available_indices = [i for i in range(min_idx, max_idx + 1) if i not in used_word_indices]
    if not available_indices:  # If all words in this difficulty are used
        used_word_indices.clear()  # Reset used indices
        available_indices = list(range(min_idx, max_idx + 1))  # Repopulate with all indices
    return random.choice(available_indices)

# Function to reset button positions based on game state
def reset_button_positions():
    if GAME_STATE == "MENU":
        start_button.rect.topleft = (button_x, 150)  # 880, 150
        quit_button.rect.topleft = (button_x, 350)  # 880, 350
    elif GAME_STATE == "SUCCESS":
        success_loss_menu_button.rect.topleft = (button_x, 100)  # 880, 100 (Menu)
        next_button.rect.topleft = (button_x, 250)  # 880, 250 (Next)
        success_loss_quit_button.rect.topleft = (button_x, 400)  # 880, 400 (Quit)
    elif GAME_STATE == "LOSS":
        success_loss_menu_button.rect.topleft = (button_x, 100)  # 880, 100 (Menu)
        next_button.rect.topleft = (button_x, 250)  # 880, 250 (Next)
        success_loss_quit_button.rect.topleft = (button_x, 400)  # 880, 400 (Quit)
    elif GAME_STATE == "PROGRESSION":
        success_loss_menu_button.rect.topleft = (button_x, 100)  # 880, 100 (Menu)
        next_button.rect.topleft = (button_x, 250)  # 880, 250 (Next)
        success_loss_quit_button.rect.topleft = (button_x, 400)  # 880, 400 (Quit)
    elif GAME_STATE == "WIN_ALL":
        menu_button.rect.topleft = (button_x, 350)  # 880, 350
    elif GAME_STATE == "GAME":
        game_quit_button.rect.topleft = (10, WINDOW_HEIGHT - BUTTON_HEIGHT - 10)  # 10, 585
        game_menu_button.rect.topleft = (WINDOW_WIDTH - BUTTON_WIDTH - 10, WINDOW_HEIGHT - BUTTON_HEIGHT - 10)  # 1020, 585

GAME_STATE = "MENU"
current_difficulty = "EASY"  # Start at Easy
correct_in_row = 0  # Count consecutive correct guesses
correct_words = 0  # Number of correct words in current difficulty
resetter = 0 # This counts to 10 on easy and 20 on all other game modes
words_attempted = 0  # Total words tried in current difficulty
used_word_indices = set()  # Track used word indices in this playthrough
current_word = None  # Initialize current word
current_hint = None  # Initialize current hint
current_word_index = None  # Initialize word index

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    
    # Reset button positions based on current game state
    reset_button_positions()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if GAME_STATE == "MENU":
                if start_button.check_click(mouse_pos):
                    GAME_STATE = "GAME"
                    # Only reset if no game in progress (i.e., starting fresh)
                    if current_word is None:
                        current_difficulty = "EASY"
                        correct_in_row = 0
                        correct_words = 0
                        words_attempted = 0
                        used_word_indices.clear()
                        current_word_index = get_unused_word_index(current_difficulty)
                        used_word_indices.add(current_word_index)
                        current_word = words[current_word_index]
                        current_hint = hints[current_word_index]
                        guessed_letters.clear()
                        lives = min(8, len(current_word) - 1 if len(current_word) > 1 else 1)
                        current_image_index = 8
                elif quit_button.check_click(mouse_pos):
                    running = False

            elif GAME_STATE == "WIN_ALL":
                if menu_button.check_click(mouse_pos):
                    GAME_STATE = "MENU"
            elif GAME_STATE == "SUCCESS" or GAME_STATE == "LOSS" or GAME_STATE == "PROGRESSION":
                if next_button.check_click(mouse_pos) or success_loss_menu_button.check_click(mouse_pos):
                    current_word_index = get_unused_word_index(current_difficulty)
                    used_word_indices.add(current_word_index)
                    current_word = words[current_word_index]
                    current_hint = hints[current_word_index]
                    guessed_letters.clear()
                    lives = min(8, len(current_word) - 1 if len(current_word) > 1 else 1)
                    current_image_index = 8
                    if next_button.check_click(mouse_pos):  #progression check
                        if GAME_STATE == "PROGRESSION":
                            GAME_STATE = "GAME"
                        elif GAME_STATE == "SUCCESS" or GAME_STATE == "LOSS":
                            if words_attempted == 10:
                                GAME_STATE = "PROGRESSION"
                            else:
                                GAME_STATE = "GAME"
                    elif success_loss_menu_button.check_click(mouse_pos):
                        GAME_STATE = "MENU"
                elif success_loss_quit_button.check_click(mouse_pos):
                    running = False  # Exits game
            elif GAME_STATE == "GAME":
                if game_quit_button.check_click(mouse_pos):
                    running = False  # Exits game
                elif game_menu_button.check_click(mouse_pos):
                    GAME_STATE = "MENU"
        elif event.type == pygame.KEYDOWN and GAME_STATE == "GAME":
            if event.key >= pygame.K_a and event.key <= pygame.K_z:
                letter = chr(event.key)
                if letter not in guessed_letters:
                    guessed_letters.add(letter)
                    if letter not in current_word:
                        lives -= 1
                        current_image_index = max(0, int((lives / max(1, min(8, len(current_word) - 1))) * 8))
                        if lives <= 0:
                            correct_in_row = 0
                            words_attempted += 1
                            score = correct_words
                            GAME_STATE = "LOSS"
                            # Reset for next word
                    if all(l in guessed_letters for l in current_word):
                        correct_words += 1
                        correct_in_row += 1
                        words_attempted += 1
                        score = correct_words

                        # Debug messages for tracking progression
                        print(f"Current difficulty: {current_difficulty}")
                        print(f"Words attempted: {words_attempted}")
                        print(f"Correct in a row: {correct_in_row}")
                        print(f"Correct words: {correct_words}")
                        if words_attempted == 0 and current_difficulty == "EASY":
                            print(f"In the last 10 you got {correct_words}")
                        elif words_attempted == 0 and current_difficulty != "EASY":
                            print(f"In the last 20 you got {correct_words}")

                        GAME_STATE = "SUCCESS"

    if GAME_STATE == "MENU":
        screen.blit(background, (0, 0))
        start_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)
        start_button.draw(screen)
        quit_button.draw(screen)

        title_word = font2.render("WrdGuessr", True, (0, 0, 0))
        screen.blit(title_word, (150, 50))

    elif GAME_STATE == "GAME":
        screen.blit(game_background, (0, 0))
        dash_spacing = 60
        word_x = 120
        for i, letter in enumerate(current_word):
            screen.blit(dash_img, (word_x + i * dash_spacing, WINDOW_HEIGHT // 2))
            if letter in guessed_letters:
                letter_surface = font.render(letter, True, (0, 0, 0))
                letter_rect = letter_surface.get_rect(center=(word_x + i * dash_spacing + dash_img.get_width() // 2, WINDOW_HEIGHT // 2 - 30))
                screen.blit(letter_surface, letter_rect)
        lives_surface = font.render(f"Lives: {lives}", True, (0, 0, 0))
        screen.blit(lives_surface, (10, 10))
        hint_surface = font.render(f"Hint: {current_hint}", True, (0, 0, 0))
        screen.blit(hint_surface, (10, 60))

        current_difficulty_text = font.render(current_difficulty, True, (0, 0, 0))
        screen.blit(current_difficulty_text, (WINDOW_WIDTH - 250, 10))
        hint_surface = font.render(f"{correct_words}/{words_attempted}", True, (0, 0, 0))
        screen.blit(hint_surface, (WINDOW_WIDTH - 150, 60))
        screen.blit(hangman_images[current_image_index], (WINDOW_WIDTH - 750, WINDOW_HEIGHT // 2 - 412))
        
        # Draw the Quit and Menu buttons in GAME state
        game_quit_button.check_hover(mouse_pos)
        game_menu_button.check_hover(mouse_pos)
        game_quit_button.draw(screen)
        game_menu_button.draw(screen)
        
    elif GAME_STATE == "SUCCESS" or GAME_STATE == "LOSS" or GAME_STATE == "PROGRESSION":
        screen.blit(game_background, (0, 0))
        # Dim the background
        dim_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        dim_surface.fill((0, 0, 0))
        dim_surface.set_alpha(128)
        screen.blit(dim_surface, (0, 0))
        
        # Buttons: Next, menu and Quit
        success_loss_menu_button.check_hover(mouse_pos)
        next_button.check_hover(mouse_pos)
        success_loss_quit_button.check_hover(mouse_pos)
        success_loss_menu_button.draw(screen)
        next_button.draw(screen)
        success_loss_quit_button.draw(screen)

        if GAME_STATE == "SUCCESS" or GAME_STATE == "LOSS":
            # Correct word capitalization + load
            current_word_text = current_word.capitalize()
            current_word_text = font.render(current_word_text, True, (255, 255, 255))

            # Check difficulty progression
            if current_difficulty == "EASY" and words_attempted >= 10 and correct_words >= 7:
                print("PROGRESSING FROM EASY TO MEDIUM!")
                current_difficulty = "MEDIUM"
                GAME_STATE = "SUCCESS"
            elif current_difficulty == "MEDIUM" and words_attempted >= 20 and correct_words >= 14:
                print("PROGRESSING FROM MEDIUM TO HARD!")
                current_difficulty = "HARD"
                GAME_STATE = "SUCCESS"
            elif current_difficulty == "HARD" and words_attempted >= 20 and correct_words >= 14:
                print("PROGRESSING FROM HARD TO EXTREME!")
                current_difficulty = "EXTREME"
                GAME_STATE = "SUCCESS"
            elif current_difficulty == "EXTREME" and correct_in_row >= 20:
                print("YOU WIN THE GAME!")
                GAME_STATE = "WIN_ALL"

            if GAME_STATE == "SUCCESS":
                # Success message
                success_text = font.render("Correct!", True, (255, 255, 255))
                screen.blit(success_text, (WINDOW_WIDTH // 2 - 100, 50))

                # Word was message
                word_text = font.render("The word was:", True, (255, 255, 255))
                screen.blit(word_text, (100, 250))
                screen.blit(current_word_text, (450, 250))

            elif GAME_STATE == "LOSS":
                # Loss message
                loss_text = font.render("Incorrect", True, (255, 255, 255))
                screen.blit(loss_text, (WINDOW_WIDTH // 2 - 100, 50))

                # Correct word was message
                word_text = font.render("The correct word was:", True, (255, 255, 255))
                screen.blit(word_text, (70, 250))
                screen.blit(current_word_text, (600, 250))

        elif GAME_STATE == "PROGRESSION":
            # Difficulty message
            progression_text = font.render("You are on", True, (255, 255, 255))
            screen.blit(progression_text, (375, 50))
            progression_level = font.render(current_difficulty, True, (255, 255, 255))
            screen.blit(progression_level, (WINDOW_WIDTH // 2 + 25, 50))

            # Correct words message
            correct_words_text = font.render(f"You got {score} / 10", True, (255, 255, 255))
            screen.blit(correct_words_text, (200, 250))

            difficulty_text = font.render(f"Difficulty:", True, (0, 0, 0))
            screen.blit(difficulty_text, (WINDOW_WIDTH - 600, 10))

            if current_difficulty == "EASY":
                progression_limit_text = font.render(f"To progress you need 7", True, (255, 255, 255))
            elif current_difficulty == "MEDIUM" or current_difficulty == "HARD":
                progression_limit_text = font.render(f"To progress you need 14", True, (255, 255, 255))
            else:
                progression_limit_text = font.render(f"To progress you need exactly 20/20", True, (255, 255, 255))
            screen.blit(progression_limit_text, (100, 450))

            correct_words = 0
            words_attempted = 0
    
            
    elif GAME_STATE == "WIN_ALL":
        screen.blit(game_background, (0, 0))
        win_surface = font.render("Blimey, you're a Hangman champ!", True, (0, 0, 0))
        screen.blit(win_surface, (WINDOW_WIDTH // 2 - 250, WINDOW_HEIGHT // 2 - 50))
        menu_button.check_hover(mouse_pos)
        menu_button.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()