import pygame
import os

#To-Do:
#Wrap code inside of functions for modularity

pygame.init()

#Screen initialization...
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

text_font = pygame.font.SysFont('Short Baby', 72)


game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Word Game")

#Load background image from local path/rescale
game_background_image = pygame.transform.scale(pygame.image.load(os.path.join('Background.png')), 
                                                             (SCREEN_WIDTH, SCREEN_HEIGHT))
title_image = pygame.transform.scale(pygame.image.load(os.path.join('Title.png')), 
                                                                       (473, 70))
TITLE_ORIGIN  = 640 - (473 / 2) #Position Title based on centrepoint, not leftmost point

main_menu_background = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

#Menu Buttons
menu_play_button = text_font.render('Play', False, (0, 0, 0))
menu_exit_button =  text_font.render ('Exit', False, (0, 0, 0))


#Defining the range in which the mouse position must be to click a menu button.
MENU_BUTTON_X_BEG = 580
MENU_BUTTON_X_END = 720

PLAY_BUTTON_Y_BEG = 200
PLAY_BUTTON_Y_END = 260

EXIT_BUTTON_Y_BEG = 300
EXIT_BUTTON_Y_END = 360

#Fill dictionary with words from the data set.
dictionary = []
with open('Word Set.txt', 'r') as word_set:
 for word in word_set:
    dictionary.append(word.strip())

#Use to transition between main menu and game screen
in_menu = True

pygame.draw.rect(game_screen, (255, 255, 255), main_menu_background)
pygame.Surface.blit(game_screen, title_image, (TITLE_ORIGIN, 0))
         
game_screen.blit(menu_play_button, (MENU_BUTTON_X_BEG, PLAY_BUTTON_Y_BEG))
game_screen.blit(menu_exit_button, (MENU_BUTTON_X_BEG, EXIT_BUTTON_Y_BEG))


#Game loop

game_running = True
while game_running:

    #Main Menu

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            game_running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if x >= MENU_BUTTON_X_BEG and x <= MENU_BUTTON_X_END and y >= PLAY_BUTTON_Y_BEG and y <= PLAY_BUTTON_Y_END and in_menu: #Janky button press detection for Play button, use Rect.collidepoint instead

             pygame.Surface.blit(game_screen, game_background_image, (0, 0))

             pygame.Surface.blit(game_screen, title_image, (TITLE_ORIGIN, 0))

             in_menu = False

            if x >= MENU_BUTTON_X_BEG and x <= MENU_BUTTON_X_END and y >= EXIT_BUTTON_Y_BEG and y <= EXIT_BUTTON_Y_END and in_menu: 
             game_running = False

    pygame.display.update()

pygame.quit()