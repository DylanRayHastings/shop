import pygame
from helpers import render_text

class Button:
    def __init__(self, text, x, y, width, height, action=None, font=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (70, 130, 180)  # Steel blue
        self.hover_color = (100, 149, 237)  # Cornflower blue
        self.click_color = (65, 105, 225)  # Royal blue
        self.text = text
        self.action = action
        self.font = font
        self.clicked = False

    def draw(self, screen):
        color = self.color
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            color = self.hover_color
            if pygame.mouse.get_pressed()[0]:
                color = self.click_color

        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        text_surf = render_text(self.font, self.text, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                if self.action:
                    self.action()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = False
