import pygame
import abc
from colors import *
from random import randrange


class Object(abc.ABC):
    def __init__(self, screen, x, y, width=0, height=0):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @abc.abstractmethod
    def draw(self):
        pass

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def check_collision(self, other_object):
        return self.get_rect().colliderect(other_object.get_rect())


class Player(Object):
    def __init__(self, screen, x, y, width=0, height=0):
        super().__init__(screen, x, y, width, height)
        self.color = YELLOW
        self.jump_color = WHITE
        self.jump = 0
        self.JUMP_POWER = 50
        self.JUMP_DELAY = 10

    def draw(self):
        self.jump = -self.JUMP_DELAY if self.jump <= -self.JUMP_DELAY else self.jump - 1
        pygame.draw.rect(
            self.screen,
            self.jump_color if self.jump > 0 else self.color,
            self.get_rect(),
        )

    def handle_movement(self, event, line_width, line_spacing):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.x > line_width + line_spacing:
                self.x -= line_spacing + line_width
            elif (
                event.key == pygame.K_RIGHT
                and self.x < self.screen.get_width() - line_width - line_spacing
            ):
                self.x += line_spacing + line_width
            elif event.key == pygame.K_UP and self.jump <= -self.JUMP_DELAY:
                self.jump = self.JUMP_POWER

    def is_jumping(self):
        return self.jump > 0


class Obstacle(Object):
    def __init__(self, screen, lines, line_spacing, line_width):
        line = randrange(lines)
        height = randrange(20, 200)
        super().__init__(
            screen, 10 + line * (line_spacing + line_width), -200, 100, height
        )
        self.color = RED
        self.speed = 6

    def draw(self):
        self.move(0, self.speed)
        pygame.draw.rect(
            self.screen,
            self.color,
            self.get_rect(),
        )

        return self.y > self.screen.get_height() + self.height

    def handle_movement(self):
        pass
