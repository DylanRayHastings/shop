import pygame
from constants import BLACK, WHITE
from helpers import render_text, handle_mouse_click
from icecream import ic

class ScrollableText:
    def __init__(self, x, y, width, height, font, text_font, game_state):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text_font = text_font
        self.texts = []
        self.scroll_offset = 0
        self.color = BLACK
        self.game_state = game_state
        self.scroll_active = False
        # ic(self.__dict__)  # Debugging

    def add_text(self, text):
        if text is None:
            text = "No message provided."
        self.texts.extend(text.split('\n'))
        self.scroll_offset = 0
        # ic(f"Added text: {text}, updated scroll_offset: {self.scroll_offset}")  # Debugging

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        y = self.rect.y + 10
        max_visible_lines = (self.rect.height - 20) // (self.text_font.get_height() + 5)
        visible_texts = self.texts[self.scroll_offset:self.scroll_offset + max_visible_lines]
        # ic(f"Drawing texts from index {self.scroll_offset} to {self.scroll_offset + max_visible_lines}")  # Debugging
        
        surface = screen.subsurface(self.rect).copy()
        surface.fill(WHITE)
        for text in visible_texts:
            text_surf = render_text(self.text_font, text, self.color)
            surface.blit(text_surf, (10, y - self.rect.y - 10))
            y += text_surf.get_height() + 5
        screen.blit(surface, self.rect.topleft)
        # ic(visible_texts)  # Debugging

    def handle_event(self, event):
        if self.game_state.popup is None:
            if handle_mouse_click(self.rect, event):
                self.scroll_active = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.scroll_active = False
            if self.scroll_active and hasattr(event, 'button'):
                if event.button == 4:
                    self.scroll_offset = max(0, self.scroll_offset - 1)
                    # ic(f"Scrolled up, new scroll_offset: {self.scroll_offset}")  # Debugging
                elif event.button == 5:
                    max_visible_lines = (self.rect.height - 20) // (self.text_font.get_height() + 5)
                    self.scroll_offset = min(len(self.texts) - max_visible_lines, self.scroll_offset + 1)
                    # ic(f"Scrolled down, new scroll_offset: {self.scroll_offset}")  # Debugging

            if handle_mouse_click(self.rect, event) and not self.scroll_active:
                item_height = self.text_font.get_height() + 5
                relative_y = event.pos[1] - self.rect.y
                item_index = self.scroll_offset + relative_y // item_height
                if 0 <= item_index < len(self.texts):
                    from ui_elements.popup import Popup  # Import Popup here to avoid circular import
                    self.game_state.popup = Popup(self.texts[item_index], self.game_state)
                    # ic(f"Clicked on item: {self.texts[item_index]}")  # Debugging

            max_visible_lines = (self.rect.height - 20) // (self.text_font.get_height() + 5)
            self.scroll_offset = max(0, min(self.scroll_offset, len(self.texts) - max_visible_lines))
            # ic(f"Final scroll_offset: {self.scroll_offset}")  # Debugging

