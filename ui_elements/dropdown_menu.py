import pygame
from icecream import ic
from constants import BLACK, GRAY, BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_CLICK_COLOR, BUTTON_EXPANDED_COLOR
from helpers import render_text, center_text_in_rect

class DropdownMenu:
    def __init__(self, x, y, width, options, actions, font):
        self.rect = pygame.Rect(x, y, width, 40)
        self.options = options
        self.actions = actions
        self.font = font
        self.expanded = False
        self.option_height = 40

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.expanded = not self.expanded
                ic(self.expanded)
            elif self.expanded:
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.option_height, self.rect.width, self.option_height)
                    if option_rect.collidepoint(event.pos):
                        self.actions[i]()
                        self.expanded = False
                        ic(option, self.actions[i])
                        return
                self.expanded = False

    def draw(self, screen):
        color = BUTTON_EXPANDED_COLOR if self.expanded else BUTTON_COLOR
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            color = BUTTON_HOVER_COLOR
            if pygame.mouse.get_pressed()[0]:
                color = BUTTON_CLICK_COLOR

        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text_surf = render_text(self.font, "Menu", BLACK)
        center_text_in_rect(screen, text_surf, self.rect)

        # Draw arrow icon
        arrow_direction = "▲" if self.expanded else "▼"
        arrow_surf = render_text(self.font, arrow_direction, BLACK)
        arrow_rect = arrow_surf.get_rect()
        arrow_rect.topleft = (self.rect.right - 30, self.rect.centery - arrow_rect.height // 2)
        screen.blit(arrow_surf, arrow_rect)

        if self.expanded:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.option_height, self.rect.width, self.option_height)
                color = BUTTON_COLOR
                if option_rect.collidepoint(pygame.mouse.get_pos()):
                    color = BUTTON_HOVER_COLOR
                    if pygame.mouse.get_pressed()[0]:
                        color = BUTTON_CLICK_COLOR

                pygame.draw.rect(screen, color, option_rect, border_radius=5)
                pygame.draw.rect(screen, BLACK, option_rect, 2)
                option_text_surf = render_text(self.font, option, BLACK)
                center_text_in_rect(screen, option_text_surf, option_rect)
