import pygame
import sys
import os
import random  # random word selection

os.chdir("c:/Users/theje/Desktop/word game project")  # specify working directory!!
pygame.init()

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Hangman - Main Menu")

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
next_button = Button(next_img, button_x, 250)  # SUCCESS (Next, renamed from success_next_button)
success_quit_button = Button(quit_img, button_x, 400)  # SUCCESS (Quit)

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
        next_button.rect.topleft = (button_x, 250)  # 880, 250 (Next)
        success_quit_button.rect.topleft = (button_x, 400)  # 880, 400 (Quit)
    elif GAME_STATE == "WIN_ALL":
        menu_button.rect.topleft = (button_x, 350)  # 880, 350
    elif GAME_STATE == "GAME":
        game_quit_button.rect.topleft = (10, WINDOW_HEIGHT - BUTTON_HEIGHT - 10)  # 10, 585

GAME_STATE = "MENU"
current_difficulty = "EASY"  # Start at Easy
correct_in_row = 0  # Count consecutive correct guesses
attempt_history = []  # List of wins and losses
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
                        attempt_history.clear()
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
            elif GAME_STATE == "SUCCESS":
                if next_button.check_click(mouse_pos):
                    GAME_STATE = "GAME"
                    current_word_index = get_unused_word_index(current_difficulty)
                    used_word_indices.add(current_word_index)
                    current_word = words[current_word_index]
                    current_hint = hints[current_word_index]
                    guessed_letters.clear()
                    lives = min(8, len(current_word) - 1 if len(current_word) > 1 else 1)
                    current_image_index = 8
                elif success_quit_button.check_click(mouse_pos):
                    running = False  # Exits game
            elif GAME_STATE == "GAME":
                if game_quit_button.check_click(mouse_pos):
                    running = False  # Exits game
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
                            attempt_history.append(False)
                            words_attempted += 1
                            # Reset for next word
                            current_word_index = get_unused_word_index(current_difficulty)
                            used_word_indices.add(current_word_index)
                            current_word = words[current_word_index]
                            current_hint = hints[current_word_index]
                            guessed_letters.clear()
                            lives = min(8, len(current_word) - 1 if len(current_word) > 1 else 1)
                            current_image_index = 8
                    if all(l in guessed_letters for l in current_word):
                        correct_in_row += 1
                        attempt_history.append(True)
                        words_attempted += 1
                        
                        # Debug messages for tracking progression
                        print(f"Current difficulty: {current_difficulty}")
                        print(f"Words attempted: {words_attempted}")
                        print(f"Correct in a row: {correct_in_row}")
                        print(f"Attempt history length: {len(attempt_history)}")
                        if len(attempt_history) >= 10:
                            print(f"Last 10 attempts success rate: {sum(attempt_history[-10:])}")
                        if len(attempt_history) >= 20:
                            print(f"Last 20 attempts success rate: {sum(attempt_history[-20:])}")
                            
                        # Check difficulty progression
                        if current_difficulty == "EASY" and len(attempt_history) >= 10 and sum(attempt_history[-10:]) >= 7:
                            print("PROGRESSING FROM EASY TO MEDIUM!")
                            current_difficulty = "MEDIUM"
                            attempt_history.clear()
                            words_attempted = 0
                            GAME_STATE = "SUCCESS"
                        elif current_difficulty == "MEDIUM" and len(attempt_history) >= 20 and sum(attempt_history[-20:]) >= 14:
                            print("PROGRESSING FROM MEDIUM TO HARD!")
                            current_difficulty = "HARD"
                            attempt_history.clear()
                            words_attempted = 0
                            GAME_STATE = "SUCCESS"
                        elif current_difficulty == "HARD" and len(attempt_history) >= 20 and sum(attempt_history[-20:]) >= 14:
                            print("PROGRESSING FROM HARD TO EXTREME!")
                            current_difficulty = "EXTREME"
                            attempt_history.clear()
                            words_attempted = 0
                            GAME_STATE = "SUCCESS"
                        elif current_difficulty == "EXTREME" and correct_in_row >= 20:
                            print("YOU WIN THE GAME!")
                            GAME_STATE = "WIN_ALL"
                        else:
                            # If no progression, just go to success screen
                            GAME_STATE = "SUCCESS"
                        
                        # Reset counters if threshold not met
                        if current_difficulty == "EASY" and len(attempt_history) >= 10 and sum(attempt_history[-10:]) < 7:
                            attempt_history.clear()
                            words_attempted = 0
                        elif current_difficulty in ["MEDIUM", "HARD"] and len(attempt_history) >= 20 and sum(attempt_history[-20:]) < 14:
                            attempt_history.clear()
                            words_attempted = 0

    if GAME_STATE == "MENU":
        screen.blit(background, (0, 0))
        start_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)
        start_button.draw(screen)
        quit_button.draw(screen)
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
        
        # Show current progress toward next difficulty
        if current_difficulty == "EASY":
            progress = f"{current_difficulty.capitalize()}: {sum(attempt_history[-10:] if len(attempt_history) >= 10 else attempt_history)}/{10}"
        else:
            progress = f"{current_difficulty.capitalize()}: {sum(attempt_history[-20:] if len(attempt_history) >= 20 else attempt_history)}/{20}"
        
        progress_surface = font.render(progress, True, (0, 0, 0))
        screen.blit(progress_surface, (WINDOW_WIDTH - 300, 10))
        screen.blit(hangman_images[current_image_index], (WINDOW_WIDTH - 750, WINDOW_HEIGHT // 2 - 412))
        
        # Draw the Quit button in GAME state
        game_quit_button.check_hover(mouse_pos)
        game_quit_button.draw(screen)
        
    elif GAME_STATE == "SUCCESS":
        screen.blit(game_background, (0, 0))
        # Dim the background
        dim_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        dim_surface.fill((0, 0, 0))
        dim_surface.set_alpha(128)
        screen.blit(dim_surface, (0, 0))
        
        # Success message
        success_surface = font.render("Correct!", True, (255, 255, 255))
        screen.blit(success_surface, (WINDOW_WIDTH // 2 - 100, 50))
        
        # Buttons: Next and Quit
        next_button.check_hover(mouse_pos)
        success_quit_button.check_hover(mouse_pos)
        next_button.draw(screen)
        success_quit_button.draw(screen)
        
    elif GAME_STATE == "WIN_ALL":
        screen.blit(game_background, (0, 0))
        win_surface = font.render("Blimey, you're a Hangman champ!", True, (0, 0, 0))
        screen.blit(win_surface, (WINDOW_WIDTH // 2 - 250, WINDOW_HEIGHT // 2 - 50))
        menu_button.check_hover(mouse_pos)
        menu_button.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()