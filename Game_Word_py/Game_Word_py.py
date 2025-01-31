import pygame
import os

pygame.init()

#Screen initialization...
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

text_font = pygame.font.SysFont('Short Baby', 76)


game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Word Game")

#Load background image from local path/rescale
game_background_image = pygame.transform.scale(pygame.image.load(os.path.join('Background.png')), 
                                                             (SCREEN_WIDTH, SCREEN_HEIGHT))
title_image = pygame.transform.scale(pygame.image.load(os.path.join('Title.png')), 
                                                                       (473, 70))
TITLE_ORIGIN  = 640 - (473 / 2) #Position Title based on centrepoint, not leftmost point

main_menu_background = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

#Buttons
play_button = text_font.render('Play', False, (0, 0, 0))
exit_button =  text_font.render ('Exit', False, (0, 0, 0))

#Fill dictionary with words from the data set.
dictionary = []
with open('Word Set.txt', 'r') as word_set:
 for word in word_set:
    dictionary.append(word.strip())

#Use to transition between main menu and game screen
in_menu = True

#Game loop
game_running = True
while game_running:

    #Main Menu
    if in_menu:
         pygame.draw.rect(game_screen, (255, 255, 255), main_menu_background)
         pygame.Surface.blit(game_screen, title_image, (TITLE_ORIGIN, 0))
         
         game_screen.blit(play_button, (580, 200))
         game_screen.blit(exit_button, (580, 300))
    else:
        pygame.Surface.blit(game_screen, game_background_image, (0, 0))
        pygame.Surface.blit(game_screen, title_image, (TITLE_ORIGIN, 0))

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            game_running = False

    pygame.display.update()

pygame.quit()