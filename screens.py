import pygame
from button import Button
from colors import *
import abc
import sys
from objects import *
from random import randrange


class Screen(abc.ABC):
    def __init__(self, screen_width, screen_height, font):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = font

    @abc.abstractmethod
    def draw(self):
        pass

    @abc.abstractmethod
    def handle_events(self):
        pass

    def exit(self):
        pygame.quit()
        sys.exit()


class MenuScreen(Screen):
    def __init__(self, screen_width, screen_height, font):
        super().__init__(screen_width, screen_height, font)
        self.buttons = [
            Button("Play", screen_width / 2 - 100, 100, 200, 80, GREY, ACTIVE, font),
            Button("Quit", screen_width / 2 - 100, 200, 200, 80, GREY, ACTIVE, font),
        ]

    def draw(self):
        self.screen.fill(BLACK)
        for button in self.buttons:
            button.draw(self.screen, button.is_clicked(pygame.mouse.get_pos()))
        return "menu"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.is_clicked(pos):
                        if button.text == "Play":
                            return "game"
                        elif button.text == "Quit":
                            self.exit()
        return "menu"


class GameScreen(Screen):
    def __init__(self, screen_width, screen_height, font):
        super().__init__(screen_width, screen_height, font)
        self.line_width = 1
        self.line_color = WHITE
        self.num_lines = 6
        self.line_spacing = (screen_width - (self.line_width * self.num_lines)) / (
            self.num_lines - 1
        )

        self.button = Button(
            "||",
            screen_width - 80,
            20,
            50,
            50,
            GREY,
            ACTIVE,
            font,
        )

        self.generate_obstacle = 20
        self.reset()

    def reset(self):
        self.obstacles = []
        self.player = Player(
            self.screen,
            10,
            self.screen_height - 150,
            100,
            50,
        )

    def draw(self):
        ret_val = "game"
        self.generate_obstacle -= 1
        if self.generate_obstacle <= 0:
            self.obstacles.append(
                Obstacle(
                    self.screen, self.num_lines, self.line_spacing, self.line_width
                )
            )
            self.generate_obstacle = randrange(50, 100)

        self.screen.fill(BLACK)

        # Draw vertical lines
        for i in range(self.num_lines):
            x_pos = self.line_width * i + self.line_spacing * i
            pygame.draw.line(
                self.screen, self.line_color, (x_pos, 0), (x_pos, self.screen_height)
            )

        for o in self.obstacles:
            if not self.player.is_jumping() and o.check_collision(self.player):
                ret_val = "game_over"
                self.reset()
                break

            remove = o.draw()
            if remove:
                self.obstacles.remove(o)

        self.player.draw()

        self.button.draw(self.screen, self.button.is_clicked(pygame.mouse.get_pos()))

        return ret_val

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            elif event.type == pygame.KEYDOWN:
                self.player.handle_movement(event, self.line_width, self.line_spacing)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.button.is_clicked(pygame.mouse.get_pos()):
                    return "pause"

        return "game"


class PauseMenuScreen(Screen):
    def __init__(self, screen_width, screen_height, font):
        super().__init__(screen_width, screen_height, font)
        self.buttons = [
            Button("Resume", screen_width / 2 - 100, 100, 200, 80, GREY, ACTIVE, font),
            Button(
                "Back to Menu", screen_width / 2 - 100, 200, 200, 80, GREY, ACTIVE, font
            ),
        ]

    def draw(self):
        self.screen.fill(BLACK)
        for button in self.buttons:
            button.draw(self.screen, button.is_clicked(pygame.mouse.get_pos()))
        return "pause"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.is_clicked(pos):
                        if button.text == "Resume":
                            return "game"
                        elif button.text == "Back to Menu":
                            return "menu"
        return "pause"


class GameOverScreen(Screen):
    def __init__(self, screen_width, screen_height, font):
        super().__init__(screen_width, screen_height, font)
        self.buttons = [
            Button("Restart", screen_width / 2 - 100, 100, 200, 80, GREY, ACTIVE, font),
            Button(
                "Back to Menu", screen_width / 2 - 100, 200, 200, 80, GREY, ACTIVE, font
            ),
        ]

    def draw(self):
        self.screen.fill(BLACK)
        for button in self.buttons:
            button.draw(self.screen, button.is_clicked(pygame.mouse.get_pos()))
        return "game_over"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.is_clicked(pos):
                        if button.text == "Restart":
                            return "game"
                        elif button.text == "Back to Menu":
                            return "menu"
        return "game_over"
