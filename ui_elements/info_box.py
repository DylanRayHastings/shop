import pygame
from icecream import ic
from constants import BLACK, GRAY
from helpers import render_text, center_text_in_rect

class InfoBox:
    def __init__(self, x, y, width, height, font, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = text
        self.txt_surface = render_text(self.font, text, BLACK)

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect, 2)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        center_text_in_rect(screen, self.txt_surface, self.rect)

    def update_text(self, new_text):
        self.text = new_text
        self.txt_surface = render_text(self.font, new_text, BLACK)
