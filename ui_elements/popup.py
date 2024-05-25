import pygame
from icecream import ic
from constants import BLACK, BLUE
from utils import draw_rounded_rect
from helpers import render_text, center_text_in_rect
from ui_elements.buttons import Button

class Popup:
    """
    Popup class to create and manage popup windows.

    Attributes:
        - rect (pygame.Rect): The rectangle defining the popup window area.
        - color (tuple): The color of the popup window.
        - font (pygame.font.Font): The font used for the text.
        - item_text (str): The text of the item.
        - product_name (str): The name of the product.
        - game_state (GameState): The current game state.
        - alpha (int): The transparency level of the popup window.
        - buttons (list): List of buttons in the popup window.
    """
    def __init__(self, item_text, game_state):
        """
        Initialize a Popup object.

        Parameters:
            - item_text (str): The text of the item.
            - game_state (GameState): The current game state.
        """
        self.rect = pygame.Rect(100, 100, 200, 100)
        self.color = BLUE
        self.font = pygame.font.Font(None, 36)
        self.item_text = item_text
        self.product_name = self.extract_product_name(item_text)
        self.game_state = game_state
        self.alpha = 200
        self.buttons = [
            Button("Buy", self.rect.x + 10, self.rect.y + 50, 80, 40, self.buy_item, self.font),
            Button("Exit", self.rect.x + 110, self.rect.y + 50, 80, 40, self.close_popup, self.font)
        ]
        # ic(self.__dict__)  # Debugging

    def extract_product_name(self, item_text):
        """
        Extract the product name from the item text.

        Parameters:
            - item_text (str): The item text.

        Returns:
            str: The extracted product name.
        """
        if ',' in item_text:
            result = item_text.split(',')[1].strip()
        elif '  ' in item_text:
            result = item_text.split('  ')[1].strip()
        else:
            result = item_text
        # ic(result)  # Debugging
        return result

    def draw(self, screen):
        """
        Draw the popup window on the screen.

        Parameters:
            - screen (pygame.Surface): The screen to draw on.
        """
        draw_rounded_rect(screen, self.rect, self.color, 20, self.alpha)
        text_surf = render_text(self.font, self.product_name, BLACK)
        center_text_in_rect(screen, text_surf, self.rect)
        for button in self.buttons:
            button.draw(screen)
        # ic(screen)  # Debugging

    def handle_event(self, event):
        """
        Handle events related to the popup window.

        Parameters:
            - event (pygame.event.Event): The event to handle.
        """
        for button in self.buttons:
            button.handle_event(event)
            # ic(event)  # Debugging

    def buy_item(self):
        """
        Perform the buy item action.
        """
        result = self.game_state.shop.buy_stock_by_text(self.item_text)
        self.game_state.scrollable_text.add_text(result)
        self.game_state.money_display.update_text(f"Money: ${self.game_state.shop.cash:.2f}")
        self.close_popup()
        # ic(result)  # Debugging

    def close_popup(self):
        """
        Close the popup window.
        """
        self.game_state.popup = None
        # ic(self.game_state.popup)  # Debugging
