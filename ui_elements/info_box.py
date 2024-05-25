import pygame
from icecream import ic
from constants import BLACK, GRAY
from helpers import render_text, center_text_in_rect

class InfoBox:
    """
    InfoBox class to create and manage information boxes.

    Attributes:
        - rect (pygame.Rect): The rectangle defining the info box area.
        - font (pygame.font.Font): The font used for the text.
        - text (str): The text displayed in the info box.
        - txt_surface (pygame.Surface): The surface containing the rendered text.
    """
    def __init__(self, x, y, width, height, font, text=''):
        """
        Initialize an InfoBox object.

        Parameters:
            - x (int): X-coordinate of the info box.
            - y (int): Y-coordinate of the info box.
            - width (int): Width of the info box.
            - height (int): Height of the info box.
            - font (pygame.font.Font): The font used for the text.
            - text (str): The text displayed in the info box.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = text
        self.txt_surface = render_text(self.font, text, BLACK)
        # ic(self.__dict__)  # Debugging

    def draw(self, screen):
        """
        Draw the info box on the screen.

        Parameters:
            - screen (pygame.Surface): The screen to draw on.
        """
        pygame.draw.rect(screen, GRAY, self.rect, 2)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        center_text_in_rect(screen, self.txt_surface, self.rect)
        # ic(screen)  # Debugging

    def update_text(self, new_text):
        """
        Update the text in the info box.

        Parameters:
            - new_text (str): The new text to display.
        """
        self.text = new_text
        self.txt_surface = render_text(self.font, new_text, BLACK)
        # ic(new_text)  # Debugging
