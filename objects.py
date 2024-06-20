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
    def __init__(self, screen, x, y, width, height, line_width, line_spacing):
        super().__init__(screen, x, y, width, height)
        self.color = YELLOW
        self.jump_color = WHITE
        self.jump = 0
        self.JUMP_POWER = 50
        self.JUMP_DELAY = 10
        self.line_width = line_width
        self.line_spacing = line_spacing
        self.background = pygame.image.load("assets/player.png")
        self.jumping_background = pygame.image.load("assets/player-jumping.png")

    def draw(self):
        self.jump = -self.JUMP_DELAY if self.jump <= -self.JUMP_DELAY else self.jump - 1
        if self.is_jumping():
            self.screen.blit(self.jumping_background, self.get_rect()[:2])
        else:
            self.screen.blit(self.background, self.get_rect()[:2])

    def move_left(self):
        self.x -= self.line_spacing + self.line_width

    def move_right(self):
        self.x += self.line_spacing + self.line_width

    def jump_(self):
        self.jump = self.JUMP_POWER

    def handle_movement(self, event):
        if event.type == pygame.KEYDOWN:
            if (
                event.key == pygame.K_LEFT
                and self.x > self.line_width + self.line_spacing
            ):
                self.move_left()
            elif (
                event.key == pygame.K_RIGHT
                and self.x
                < self.screen.get_width() - self.line_width - self.line_spacing
            ):
                self.move_right()
            elif event.key == pygame.K_UP and self.jump <= -self.JUMP_DELAY:
                self.jump_()

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
        self.background = pygame.image.load("assets/obstacle.png")

    def draw(self):
        self.move(0, self.speed)
        self.screen.blit(
            pygame.transform.scale(self.background, (self.width, self.height)),
            self.get_rect()[:2],
        )

        return self.y > self.screen.get_height() + self.height

    def handle_movement(self):
        pass
