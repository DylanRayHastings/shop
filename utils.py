import pygame

def draw_rounded_rect(surface, rect, color, corner_radius, alpha):
    rect_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    rect_surface.set_alpha(alpha)
    
    pygame.draw.circle(rect_surface, color, (corner_radius, corner_radius), corner_radius)
    pygame.draw.circle(rect_surface, color, (rect.width - corner_radius - 1, corner_radius), corner_radius)
    pygame.draw.circle(rect_surface, color, (corner_radius, rect.height - corner_radius - 1), corner_radius)
    pygame.draw.circle(rect_surface, color, (rect.width - corner_radius - 1, rect.height - corner_radius - 1), corner_radius)
    
    pygame.draw.rect(rect_surface, color, (corner_radius, 0, rect.width - 2 * corner_radius, rect.height))
    pygame.draw.rect(rect_surface, color, (0, corner_radius, rect.width, rect.height - 2 * corner_radius))
    
    surface.blit(rect_surface, rect.topleft)
