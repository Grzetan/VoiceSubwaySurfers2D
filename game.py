import pygame
import sys  # for system exit

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

# Initialize Pygame
pygame.init()

# Define font
font = pygame.font.Font(None, 32)


class Button:
    def __init__(self, text, x, y, width, height, inactive_color, active_color):
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
        text = font.render(self.text, True, WHITE)
        text_rect = text.get_rect(
            center=(self.x + (self.width // 2), self.y + (self.height // 2))
        )
        screen.blit(text, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class MenuScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.buttons = [
            Button("Play", 100, 200, 100, 50, GREY, WHITE),
            Button("Quit", 300, 200, 100, 50, GREY, WHITE),
        ]
        self.font = font

    def draw(self):
        self.screen.fill(BLACK)
        for button in self.buttons:
            button.draw(self.screen, button.is_clicked(pygame.mouse.get_pos()))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Check mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.is_clicked(pos):
                        if button.text == "Play":
                            return "play"  # Return "play" to switch screens
                        elif button.text == "Quit":
                            pygame.quit()
                            sys.exit()  # Exit program properly
        return None  # Return None to stay on the menu


class EmptyScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, screen_height))
        self.button = Button(
            "STOP",
            self.screen_width // 2 - 50,
            self.screen_height // 2,
            100,
            50,
            GREY,
            WHITE,
        )
        self.radius = 0  # Initialize radius for the circle

    def draw(self):
        self.screen.fill(BLACK)
        # Draw the growing circle
        pygame.draw.circle(
            self.screen,
            WHITE,
            (self.screen_width // 2, self.screen_height // 2),
            self.radius,
        )
        self.button.draw(self.screen, self.button.is_clicked(pygame.mouse.get_pos()))
        # Update the radius (adjust growth rate as needed)
        self.radius += 1

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Exit program properly
            # Check mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button.is_clicked(pygame.mouse.get_pos()):
                    return "pause"  # Return "pause" to open pause menu
        return None  # Return None to stay on empty screen


class PauseMenuScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.buttons = [
            Button("Resume", 100, 200, 100, 50, GREY, WHITE),
            Button("Back to Menu", 300, 200, 150, 50, GREY, WHITE),
        ]
        self.font = font

    def draw(self):
        self.screen.fill(BLACK)
        for button in self.buttons:
            button.draw(self.screen, button.is_clicked(pygame.mouse.get_pos()))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Exit program properly
            # Check mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.is_clicked(pos):
                        if button.text == "Resume":
                            return (
                                "resume"  # Return "resume" to go back to empty screen
                            )
                        elif button.text == "Back to Menu":
                            return "menu"  # Return "menu" to go back to main menu
        return None  # Return None to stay on pause menu


# Set window title
pygame.display.set_caption("Menu")
CLOCK = pygame.time.Clock()

# Create screens
menu_screen = MenuScreen(800, 600)
empty_screen = EmptyScreen(800, 600)
pause_menu_screen = PauseMenuScreen(800, 600)

# Game loop
current_screen = menu_screen
running = True
while running:
    CLOCK.tick(5)
    current_screen.draw()
    next_screen = current_screen.handle_events()
    if next_screen:
        if next_screen == "play":
            current_screen = empty_screen
        elif next_screen == "pause":
            current_screen = pause_menu_screen
        elif next_screen == "resume":
            current_screen = empty_screen
        elif next_screen == "menu":
            current_screen = menu_screen
            # Exit if "Quit" is clicked from pause menu
        elif next_screen == "quit":
            running = False
    pygame.display.flip()

# Quit Pygame
pygame.quit()
