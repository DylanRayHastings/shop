import pygame
from constants import BLACK, BLUE
from utils import draw_rounded_rect
from helpers import render_text, center_text_in_rect, handle_mouse_click
from icecream import ic

class Button:
    def __init__(self, text, x, y, width, height, action, font):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BLUE
        self.action = action
        self.font = font
        self.alpha = 200
        # ic(self.__dict__)  # Debugging

    def draw(self, screen):
        draw_rounded_rect(screen, self.rect, self.color, 20, self.alpha)
        text_surf = render_text(self.font, self.text, BLACK)
        center_text_in_rect(screen, text_surf, self.rect)
        # ic(screen)  # Debugging

    def handle_event(self, event):
        if handle_mouse_click(self.rect, event):
            self.action()
            # ic(event)  # Debugging

