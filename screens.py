import pygame
from button import Button
from colors import *
import abc
import sys


class Screen:
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
        self.radius = 0

    def draw(self):
        self.screen.fill(BLACK)
        pygame.draw.circle(
            self.screen,
            WHITE,
            (self.screen_width // 2, self.screen_height // 2),
            self.radius,
        )
        self.button.draw(self.screen, self.button.is_clicked(pygame.mouse.get_pos()))
        self.radius += 1

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
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
