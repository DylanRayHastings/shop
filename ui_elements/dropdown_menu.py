import pygame
from icecream import ic
from constants import BLACK, GRAY
from helpers import render_text, center_text_in_rect, handle_mouse_click

class DropdownMenu:
    """
    DropdownMenu class to create and manage dropdown menus.

    Attributes:
        - rect (pygame.Rect): The rectangle defining the dropdown menu area.
        - options (list): List of options in the dropdown menu.
        - actions (list): List of actions corresponding to the options.
        - font (pygame.font.Font): The font used for the text.
        - expanded (bool): Flag to track if the menu is expanded.
        - option_height (int): Height of each option.
    """
    def __init__(self, x, y, width, options, actions, font):
        """
        Initialize a DropdownMenu object.

        Parameters:
            - x (int): X-coordinate of the dropdown menu.
            - y (int): Y-coordinate of the dropdown menu.
            - width (int): Width of the dropdown menu.
            - options (list): List of options in the dropdown menu.
            - actions (list): List of actions corresponding to the options.
            - font (pygame.font.Font): The font used for the text.
        """
        self.rect = pygame.Rect(x, y, width, 40)
        self.options = options
        self.actions = actions
        self.font = font
        self.expanded = False
        self.option_height = 40
        # ic(self.__dict__)  # Debugging

    def handle_event(self, event):
        """
        Handle events related to the dropdown menu.

        Parameters:
            - event (pygame.event.Event): The event to handle.
        """
        if handle_mouse_click(self.rect, event):
            self.expanded = not self.expanded
            # ic(self.expanded)  # Debugging
        elif self.expanded:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.option_height, self.rect.width, self.option_height)
                if option_rect.collidepoint(event.pos):
                    self.actions[i]()
                    self.expanded = False
                    # ic(option, self.actions[i])  # Debugging
                    return
            self.expanded = False
            # ic(self.expanded)  # Debugging

    def draw(self, screen):
        """
        Draw the dropdown menu on the screen.

        Parameters:
            - screen (pygame.Surface): The screen to draw on.
        """
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text_surf = render_text(self.font, "Menu", BLACK)
        center_text_in_rect(screen, text_surf, self.rect)

        if self.expanded:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.option_height, self.rect.width, self.option_height)
                pygame.draw.rect(screen, GRAY, option_rect)
                pygame.draw.rect(screen, BLACK, option_rect, 2)
                option_text_surf = render_text(self.font, option, BLACK)
                center_text_in_rect(screen, option_text_surf, option_rect)
        # ic(screen)  # Debugging

