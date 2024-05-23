import pygame
from screens import *

pygame.init()

font = pygame.font.Font(None, 32)
W = 600
H = 800

pygame.display.set_caption("Game")
CLOCK = pygame.time.Clock()

screens = {
    "game": GameScreen(W, H, font),
    "menu": MenuScreen(W, H, font),
    "pause": PauseMenuScreen(W, H, font),
    "game_over": GameOverScreen(W, H, font),
}

current_screen = screens["menu"]
running = True
while running:
    CLOCK.tick(30)
    current_screen = screens[current_screen.draw()]
    current_screen = screens[current_screen.handle_events()]

    pygame.display.flip()

pygame.quit()
