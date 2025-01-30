import pygame
import os

pygame.init()

#Screen initialization...
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Word Game")

#Load background image from local path/rescale
background_image = pygame.transform.scale(pygame.image.load(os.path.join('Background.png')), 
                                                             (SCREEN_WIDTH, SCREEN_HEIGHT))
#Load title image from local path/rescale
title_image = pygame.transform.scale(pygame.image.load(os.path.join('Title.png')), 
                                                                       (473, 70))

#Game loop.
game_running = True
while game_running:

    pygame.Surface.blit(game_screen, background_image, (0, 0))
    pygame.Surface.blit(game_screen, title_image, (640 - (473 / 2), 0))

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            game_running = False

    pygame.display.update()

pygame.quit()