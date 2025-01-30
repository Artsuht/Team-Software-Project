from asyncio.windows_events import NULL
import pygame
import os

pygame.init()

#Screen initialization...
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Word Game")

#Load background image from local path/rescale
game_background_image = pygame.transform.scale(pygame.image.load(os.path.join('Background.png')), 
                                                             (SCREEN_WIDTH, SCREEN_HEIGHT))
title_image = pygame.transform.scale(pygame.image.load(os.path.join('Title.png')), 
                                                                       (473, 70))
main_menu_background = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)


#Fill dictionary with words from the data set.
dictionary = []
with open('Word Set.txt', 'r') as word_set:
 for word in word_set:
    dictionary.append(word.strip())

#Menu
in_menu = True

#Game loop
game_running = True
while game_running:

    #Main Menu
    if in_menu:
         pygame.draw.rect(game_screen, (255, 255, 255), main_menu_background)
         pygame.Surface.blit(game_screen, title_image, (640 - (473 / 2), 0))
    else:
        pygame.Surface.blit(game_screen, game_background_image, (0, 0))
        pygame.Surface.blit(game_screen, title_image, (640 - (473 / 2), 0))

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            game_running = False

    pygame.display.update()

pygame.quit()