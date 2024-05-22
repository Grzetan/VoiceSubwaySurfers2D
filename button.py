import pygame
from colors import *


class Button:
    def __init__(self, text, x, y, width, height, inactive_color, active_color, font):
        self.font = font
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, active):
        color = self.inactive_color if not active else self.active_color
        pygame.draw.rect(screen, color, self.rect)
        text = self.font.render(self.text, True, WHITE)
        text_rect = text.get_rect(
            center=(self.x + (self.width // 2), self.y + (self.height // 2))
        )
        screen.blit(text, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
