import pygame

def render_text(font, text, color):
    return font.render(text, True, color)

def center_text_in_rect(surface, text_surf, rect):
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

def handle_mouse_click(rect, event):
    if event.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(event.pos):
        return True
    return False

