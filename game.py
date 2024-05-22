import pygame
from screens import *


pygame.init()

font = pygame.font.Font(None, 32)

pygame.display.set_caption("Game")
CLOCK = pygame.time.Clock()

screens = {
    "game": GameScreen(800, 600, font),
    "menu": MenuScreen(800, 600, font),
    "pause": PauseMenuScreen(800, 600, font),
}

current_screen = screens["menu"]
running = True
while running:
    CLOCK.tick(30)
    current_screen.draw()
    current_screen = screens[current_screen.handle_events()]

    pygame.display.flip()

pygame.quit()
