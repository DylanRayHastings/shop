import pygame

from constants import RED, WHITE
from game_logic import begin_day
from .buttons import Button
from .scrollable_text import ScrollableText
from .info_box import InfoBox
from .dropdown_menu import DropdownMenu
from .popup import Popup
from utils import draw_rounded_rect
from helpers import render_text, center_text_in_rect, handle_mouse_click
from icecream import ic

def initialize_ui_elements(screen_width, screen_height, font, game_state, exit_to_menu, start_day):
    left_x = 10
    left_y = 10
    box_width = 200
    box_height = 40
    spacing = 10

    game_state.dropdown_menu = DropdownMenu(
        left_x, left_y, box_width, 
        ["Save", "Exit"], 
        [lambda: game_state.shop.save_game(), exit_to_menu], 
        font
    )

    game_state.money_display = InfoBox(left_x + box_width + spacing, left_y, box_width, box_height, font, "$1000.00")
    game_state.time_display = InfoBox(left_x + 2 * (box_width + spacing), left_y, box_width, box_height, font, "10:00 AM")
    game_state.popularity_display = InfoBox(left_x + 3 * (box_width + spacing), left_y, box_width, box_height, font, "0 POP")

    content_y = left_y + box_height + spacing
    content_height = screen_height - content_y - 50 - 20
    half_width = (screen_width - 40) // 2

    small_font = pygame.font.Font('Montserrat-Regular.ttf', 24)

    game_state.scrollable_text = ScrollableText(left_x, content_y, half_width - 10, content_height, font, small_font, game_state)
    game_state.inventory_display = ScrollableText(left_x + half_width + 20, content_y, half_width - 10, content_height, font, small_font, game_state)
    game_state.inventory_display.add_text(game_state.shop.show_inventory())
    # ic(game_state.__dict__)  # Debugging

def handle_events(buttons, events, game_state):
    running = True
    for event in events:
        if event.type == pygame.QUIT:
            game_state.quit_game = True
            running = False
            break
        for button in buttons:
            button.handle_event(event)
            # ic(event)  # Debugging
        if not running:
            break
        game_state.scrollable_text.handle_event(event)
        game_state.inventory_display.handle_event(event)
        game_state.dropdown_menu.handle_event(event)
        if game_state.popup:
            game_state.popup.handle_event(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            ic(mouse_pos)  # Debugging: Check mouse position on click
            for rect, item_text in game_state.clickable_inventory_items:
                if rect.collidepoint(mouse_pos):
                    ic("Item clicked:", item_text)  # Debugging: Verify item click
                    game_state.popup = Popup(item_text, game_state)
                    ic("Popup created")  # Debugging: Verify popup creation
                    break
    return running
    # ic(running)  # Debugging

def draw_ui_elements(screen, game_state):
    game_state.scrollable_text.draw(screen)
    game_state.inventory_display.draw(screen)
    game_state.dropdown_menu.draw(screen)
    game_state.money_display.draw(screen)
    game_state.time_display.draw(screen)
    game_state.popularity_display.draw(screen)
    if game_state.popup:
        ic("Drawing popup")  # Debugging: Confirm popup drawing
        game_state.popup.draw(screen)
    # ic(screen)  # Debugging

def display_message(screen, message, font, screen_width, screen_height):
    running = True
    while running:
        screen.fill(WHITE)
        text_surf = font.render(message, True, RED)
        text_rect = text_surf.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text_surf, text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                running = False
                # ic(event)  # Debugging

def start_buy_stock(game_state):
    game_state.current_input_step = 1
    game_state.scrollable_text.add_text("Click an item to buy.")
    # ic(game_state.current_input_step)  # Debugging
