import pygame
from icecream import ic
from constants import BLACK, BLUE
from utils import draw_rounded_rect
from helpers import render_text, center_text_in_rect
from ui_elements.buttons import Button

class Popup:
    def __init__(self, item_text, game_state):
        self.rect = pygame.Rect(100, 100, 400, 200)
        self.color = BLUE
        self.font = pygame.font.Font(None, 36)
        self.item_text = item_text
        self.product_name = self.extract_product_name(item_text)
        self.game_state = game_state
        self.alpha = 200
        self.buttons = [
            Button("Buy", self.rect.x + 50, self.rect.y + 150, 100, 40, self.buy_item, self.font),
            Button("Exit", self.rect.x + 250, self.rect.y + 150, 100, 40, self.close_popup, self.font)
        ]
        ic("Popup initialized:", self.__dict__)

    def extract_product_name(self, item_text):
        return item_text.split(':')[1].split('-')[0].strip()

    def draw(self, screen):
        draw_rounded_rect(screen, self.rect, self.color, 20, self.alpha)
        text_surf = render_text(self.font, self.product_name, BLACK)
        center_text_in_rect(screen, text_surf, self.rect)
        for button in self.buttons:
            button.draw(screen)
        ic("Popup drawn")

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)
        ic("Popup event handled:", event)

    def buy_item(self):
        product_number = self.item_text.split(':')[0].strip()
        result = self.game_state.shop.buy_stock(product_number, 1)
        self.game_state.scrollable_text.add_text(result)
        self.game_state.money_display.update_text(f"Money: ${self.game_state.shop.cash:.2f}")
        self.close_popup()
        ic("Item bought:", result)

    def close_popup(self):
        self.game_state.popup = None
        ic("Popup closed")
