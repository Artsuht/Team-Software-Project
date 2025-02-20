import pygame
import sys
import os
import random  # random word selection

os.chdir("c:/Users/jm24adk/Desktop/game project/") #specify working directory!!
pygame.init()

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Hangman - Main Menu")

# Colour for that highlight
YELLOW = (255, 255, 0)

# menu images
background = pygame.image.load("main.png").convert()
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

BUTTON_WIDTH = 250
BUTTON_HEIGHT = 125
start_img = pygame.image.load("start.png").convert_alpha()
start_img = pygame.transform.scale(start_img, (BUTTON_WIDTH, BUTTON_HEIGHT))
print("Scaled Start button size:", start_img.get_size())

quit_img = pygame.image.load("quit.png").convert_alpha()
quit_img = pygame.transform.scale(quit_img, (BUTTON_WIDTH, BUTTON_HEIGHT))
print("Scaled Quit button size:", quit_img.get_size())

menu_img = pygame.image.load("menu.png").convert_alpha()
menu_img = pygame.transform.scale(menu_img, (BUTTON_WIDTH, BUTTON_HEIGHT)) #bruh why is there a menu button in the main menu?
print("Scaled Menu button size:", menu_img.get_size())

# in game assets
game_background = pygame.image.load("game-screen 1.png").convert()
game_background = pygame.transform.scale(game_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
dash_img = pygame.image.load("dash.png").convert_alpha()
dash_img = pygame.transform.scale(dash_img, (50, 20)) 
with open("word set.txt", "r") as file:
    words = file.read().splitlines()
current_word = random.choice(words).lower()
guessed_letters = set()
lives=5 #track player errorsy
hangman_images=[pygame.transform.scale(pygame.image.load(f"{i}.png").convert_alpha(), (800, 700)) for i in range(9)] #define hangman image and its size

current_image_index=8 # keep track of current hangman image

font = pygame.font.SysFont("arial", 46, bold=True)


class Button:
    def __init__(self, image, x, y):
        self.original_image = image
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.scale_factor = 0.9

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
    
    #detect clicks
    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Position buttons
button_x = WINDOW_WIDTH - 400
start_button = Button(start_img, button_x, 150)
menu_button = Button(menu_img, button_x, 250)
quit_button = Button(quit_img, button_x, 350)


GAME_STATE = "MENU"  

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if GAME_STATE == "MENU":
                if start_button.check_click(mouse_pos):
                    GAME_STATE = "GAME"
                    guessed_letters.clear()
                    current_word = random.choice(words).lower()
                    lives=min(8, len(current_word)-1 if len(current_word)>1 else 1)
                    current_image_index = 8 #starts with png 8(first image)
                elif quit_button.check_click(mouse_pos):
                    running = False
        elif event.type == pygame.KEYDOWN and GAME_STATE == "GAME":
            if event.key >= pygame.K_a and event.key <= pygame.K_z:
                letter = chr(event.key)
                if letter not in guessed_letters and letter not in current_word:
                    lives -= 1
                    current_image_index = max(0, int((lives/max(1, min(8, len(current_word)-1)))*8))
                    if lives<=0:
                        GAME_STATE = "GAME_OVER"
                guessed_letters.add(letter)
                
    if GAME_STATE == "MENU":
        screen.blit(background, (0, 0))
        start_button.check_hover(mouse_pos)
        menu_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)
        start_button.draw(screen)
        menu_button.draw(screen)
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
        screen.blit(hangman_images[current_image_index], (WINDOW_WIDTH - 750, WINDOW_HEIGHT // 2 - 412))#positioning of the hangman image
    elif GAME_STATE == "GAME_OVER":
        screen.blit(game_background, (0, 0))
        game_over_surface = font.render("Pack it up buddy, you're cooked", True, (0, 0, 0))
        screen.blit(game_over_surface, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2))
    
    pygame.display.flip()
pygame.quit()
sys.exit()