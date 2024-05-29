import pygame
from ui_elements import initialize_ui_elements, handle_events, draw_ui_elements
from data_handler import parse_data
from data import data
from game_logic import Shop
from customers import CustomerManager, generate_customers
from constants import BUTTON_WIDTH, BUTTON_HEIGHT, WHITE
from icecream import ic
from ui_elements.buttons import Button
from ui_elements.scrollable_text import ScrollableText
from ui_elements.info_box import InfoBox
from ui_elements.dropdown_menu import DropdownMenu
from ui_elements.popup import Popup
from ui_elements.ui_helpers import display_message
from utils import draw_rounded_rect
from helpers import render_text, center_text_in_rect, handle_mouse_click
from employees import EmployeeManager, Skill

pygame.init()

# Set up the screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('JM 15172')
icon = pygame.image.load('jm_logo.png')
pygame.display.set_icon(icon)
background_image = pygame.image.load('jm_background.png')
background_image = pygame.transform.scale(background_image, screen.get_size())

# Set up the font and screen dimensions
FONT = pygame.font.Font('Montserrat-Regular.ttf', 36)
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Parse data
items = parse_data(data)

class GameState:
    def __init__(self, items):
        self.shop = Shop()
        for item in items:
            self.shop.add_item(item)
        self.current_input_step = 0
        self.product_number = ""
        self.quantity = ""
        self.return_to_menu = False
        self.quit_game = False
        self.popup = None
        self.customer_manager = CustomerManager()
        self.customer_manager.customers = generate_customers()
        self.day_started = False
        self.employee_manager = EmployeeManager()
        self.clickable_inventory_items = []

game_state = GameState(items)

def start_new_game():
    global game_state
    game_state = GameState(items)
    initialize_ui_elements(SCREEN_WIDTH, SCREEN_HEIGHT, FONT, game_state, exit_to_menu, start_day)
    game_loop()

def load_saved_game():
    if not game_state.shop.load_game():
        display_message(screen, "Save file not found.", FONT, SCREEN_WIDTH, SCREEN_HEIGHT)
    else:
        initialize_ui_elements(SCREEN_WIDTH, SCREEN_HEIGHT, FONT, game_state, exit_to_menu, start_day)
        game_loop()

def exit_to_menu():
    game_state.return_to_menu = True

def quit_game():
    game_state.quit_game = True

def start_day():
    game_state.day_started = True

button_x = SCREEN_WIDTH // 4 - BUTTON_WIDTH // 2

buttons = [
    Button("Start", button_x, SCREEN_HEIGHT // 2 - 150, BUTTON_WIDTH, BUTTON_HEIGHT, start_new_game, FONT),
    Button("Continue", button_x, SCREEN_HEIGHT // 2 - 50, BUTTON_WIDTH, BUTTON_HEIGHT, load_saved_game, FONT),
    Button("Exit", button_x, SCREEN_HEIGHT // 2 + 50, BUTTON_WIDTH, BUTTON_HEIGHT, quit_game, FONT)
]

initialize_ui_elements(SCREEN_WIDTH, SCREEN_HEIGHT, FONT, game_state, exit_to_menu, start_day)

def startup_scene():
    running = True
    while running:
        screen.blit(background_image, (0, 0))  # Draw the background image
        events = pygame.event.get()
        running = handle_events(buttons, events, game_state)
        if game_state.quit_game:
            return False
        for button in buttons:
            button.draw(screen)
        pygame.display.flip()
    return True

def game_loop():
    running = True
    while running:
        screen.blit(background_image, (0, 0))  # Draw the background image
        events = pygame.event.get()
        running = handle_events([], events, game_state)
        if not running or game_state.return_to_menu:
            break
        if game_state.day_started:
            game_state.customer_manager.simulate_customers(game_state.shop)
        current_inventory = game_state.shop.show_inventory()
        if current_inventory != '\n'.join(game_state.inventory_display.texts):
            game_state.inventory_display.add_text(current_inventory)
        reviews = game_state.customer_manager.show_reviews()
        if reviews != '\n'.join(game_state.scrollable_text.texts):
            game_state.scrollable_text.add_text(reviews)
        draw_ui_elements(screen, game_state)
        if game_state.popup:
            game_state.popup.draw(screen)
        pygame.display.flip()

    if game_state.return_to_menu:
        if not startup_scene():
            return
    elif game_state.quit_game:
        return

if startup_scene():
    pygame.quit()
