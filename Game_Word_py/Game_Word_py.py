import pygame

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

background = pygame.Rect((0, 0, 1280, 720))

#Game loop.
game_running = True
while game_running:

    pygame.draw.rect(game_screen, (255,255, 255), background) #Draw a white background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    pygame.display.update()

pygame.quit()