import pygame
from constants import BLACK
from helpers import render_text, handle_mouse_click
from icecream import ic
from ui_elements.popup import Popup

class ScrollableText:
    def __init__(self, x, y, width, height, font, text_font, game_state):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text_font = text_font
        self.texts = []
        self.rendered_texts = []
        self.scroll_offset = 0
        self.color = BLACK
        self.game_state = game_state
        self.scroll_active = False

    def add_text(self, text):
        if text is None:
            text = "No message provided."
        self.texts.extend(text.split('\n'))
        self.scroll_offset = 0
        self.cache_rendered_texts()

    def cache_rendered_texts(self):
        self.rendered_texts = [render_text(self.text_font, text, self.color) for text in self.texts]

    def draw(self, screen):
        clear_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        clear_surface.fill((255, 255, 255, 0))
        screen.blit(clear_surface, self.rect.topleft)

        overlay = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 128))

        screen.blit(overlay, self.rect.topleft)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        y = 10
        max_visible_lines = (self.rect.height - 20) // (self.text_font.get_height() + 5)
        visible_texts = self.rendered_texts[self.scroll_offset:self.scroll_offset + max_visible_lines]

        for text_surf in visible_texts:
            screen.blit(text_surf, (self.rect.x + 10, self.rect.y + y))
            y += text_surf.get_height() + 5

    def handle_event(self, event):
        ic(event)
        if self.game_state.popup is None:
            if handle_mouse_click(self.rect, event):
                ic("Click is within rect")
                self.scroll_active = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.scroll_active = False
                if handle_mouse_click(self.rect, event):
                    item_height = self.text_font.get_height() + 5
                    relative_y = event.pos[1] - self.rect.y
                    item_index = self.scroll_offset + relative_y // item_height
                    ic("Click detected within scrollable area")
                    ic(f"Item index: {item_index}, scroll_offset: {self.scroll_offset}, relative_y: {relative_y}")
                    if 0 <= item_index < len(self.texts):
                        ic("Creating Popup for item:", self.texts[item_index])
                        self.game_state.popup = Popup(self.texts[item_index], self.game_state)
                        ic(f"Clicked on item: {self.texts[item_index]}")
                        ic(f"Popup created with item text: {self.texts[item_index]}")
            if self.scroll_active and hasattr(event, 'button'):
                if event.button == 4:
                    self.scroll_offset = max(0, self.scroll_offset - 1)
                    ic(f"Scrolled up, new scroll_offset: {self.scroll_offset}")
                if event.button == 5:
                    max_visible_lines = (self.rect.height - 20) // (self.text_font.get_height() + 5)
                    self.scroll_offset = min(len(self.texts) - max_visible_lines, self.scroll_offset + 1)
                    ic(f"Scrolled down, new scroll_offset: {self.scroll_offset}")

            max_visible_lines = (self.rect.height - 20) // (self.text_font.get_height() + 5)
            self.scroll_offset = max(0, min(self.scroll_offset, len(self.texts) - max_visible_lines))
            ic(f"Final scroll_offset: {self.scroll_offset}")
        elif self.game_state.popup:
            self.game_state.popup.handle_event(event)
