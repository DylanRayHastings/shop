import pygame  # Import Pygame module for game development
import pygame.gfxdraw  # Import Pygame GFX draw for additional drawing functions
from data_handler import parse_data  # Import parse_data function from data_handler module
from data import data  # Import data from data module
from game_logic import Shop, begin_day  # Import Shop class from game_logic module
from ui_elements import initialize_ui_elements, handle_events, draw_ui_elements, display_message  # Import UI related functions from ui_elements module
from customers import CustomerManager, generate_customers  # Import CustomerManager and generate_customers from customers module
from constants import BUTTON_WIDTH, BUTTON_HEIGHT, WHITE  # Import constants for button dimensions and color
from icecream import ic  # Debugging
from ui_elements.buttons import Button
from ui_elements.scrollable_text import ScrollableText
from ui_elements.info_box import InfoBox
from ui_elements.dropdown_menu import DropdownMenu
from ui_elements.popup import Popup
from utils import draw_rounded_rect
from helpers import render_text, center_text_in_rect, handle_mouse_click

# Initialize Pygame
pygame.init()  # Initialize all imported Pygame modules
# ic()  # Debugging

# Set up the display
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Set the display mode to fullscreen
# ic(screen)  # Debugging
pygame.display.set_caption('JM 15172')  # Set the window caption to 'JM 15172'
icon = pygame.image.load('jm_logo.png')  # Load the game icon image
pygame.display.set_icon(icon)  # Set the window icon

# Load the background image
background_image = pygame.image.load('jm_background.png')  # Load the background image for the game

# Load the Montserrat font
FONT = pygame.font.Font('Montserrat-Regular.ttf', 36)  # Load the Montserrat font with size 36

# Get the screen dimensions
info = pygame.display.Info()  # Get display information
SCREEN_WIDTH = info.current_w  # Get the current screen width
SCREEN_HEIGHT = info.current_h  # Get the current screen height
# ic(SCREEN_WIDTH, SCREEN_HEIGHT)  # Debugging

# Parse the data and create a Shop instance
items = parse_data(data)  # Parse the data and store the items
# ic(items)  # Debugging

class GameState:
    """
    Represents the shared state of the game.

    Attributes:
        shop (Shop): The shop instance managing inventory and sales.
        current_input_step (int): The current step in the user input process.
        product_number (str): The product number input by the user.
        quantity (str): The quantity input by the user.
        return_to_menu (bool): Flag to indicate if the game should return to the menu.
        quit_game (bool): Flag to indicate if the game should quit.
        popup (Popup or None): The current popup message, if any.
        customer_manager (CustomerManager): The manager handling customer generation and simulation.
        day_started (bool): Flag to indicate if the day has started.
    """
    def __init__(self, items):
        """
        Initializes the GameState with provided items.

        Args:
            items (list): A list of items to be added to the shop inventory.
        """
        self.shop = Shop()  # Initialize a Shop instance
        for item in items:  # Add each item to the shop
            self.shop.add_item(item)
        self.current_input_step = 0  # Initialize current input step to 0
        self.product_number = ""  # Initialize product number as an empty string
        self.quantity = ""  # Initialize quantity as an empty string
        self.return_to_menu = False  # Initialize return_to_menu flag as False
        self.quit_game = False  # Initialize quit_game flag as False
        self.popup = None  # Initialize popup as None
        self.customer_manager = CustomerManager()  # Initialize CustomerManager instance
        self.customer_manager.customers = generate_customers()  # Generate and assign customers
        self.day_started = False  # Initialize day_started flag as False
        # ic(self.__dict__)  # Debugging

game_state = GameState(items)  # Create an instance of GameState with the parsed items
# ic(game_state)  # Debugging

def start_new_game():
    """
    Starts a new game by resetting the GameState and initializing UI elements.
    """
    global game_state  # Use the global game_state variable
    game_state = GameState(items)  # Reset game_state with a new instance
    initialize_ui_elements(SCREEN_WIDTH, SCREEN_HEIGHT, FONT, game_state, exit_to_menu, start_day)  # Initialize UI elements
    game_loop()  # Start the game loop
    # ic()  # Debugging

def load_saved_game():
    """
    Loads a saved game by attempting to load game data into the GameState.
    """
    if not game_state.shop.load_game():  # Attempt to load saved game data
        display_message(screen, "Save file not found.", FONT, SCREEN_WIDTH, SCREEN_HEIGHT)  # Display message if save file not found
    else:
        initialize_ui_elements(SCREEN_WIDTH, SCREEN_HEIGHT, FONT, game_state, exit_to_menu, start_day)  # Initialize UI elements if save file found
        game_loop()  # Start the game loop
    # ic()  # Debugging

def exit_to_menu():
    """
    Sets the return_to_menu flag in GameState to True.
    """
    game_state.return_to_menu = True  # Set return_to_menu flag to True
    # ic(game_state.return_to_menu)  # Debugging

def quit_game():
    """
    Sets the quit_game flag in GameState to True.
    """
    game_state.quit_game = True  # Set quit_game flag to True
    # ic(game_state.quit_game)  # Debugging

def start_day():
    """
    Sets the day_started flag in GameState to True.
    """
    game_state.day_started = True  # Set day_started flag to True
    # ic(game_state.day_started)  # Debugging

# Set buttons to be at approximately 1/4 of the screen width
button_x = SCREEN_WIDTH // 4 - BUTTON_WIDTH // 2  # Calculate the x position for the buttons
# ic(button_x)  # Debugging

buttons = [
    Button("Start", button_x, SCREEN_HEIGHT // 2 - 150, BUTTON_WIDTH, BUTTON_HEIGHT, start_new_game, FONT),  # Create Start button
    Button("Load", button_x, SCREEN_HEIGHT // 2 - 50, BUTTON_WIDTH, BUTTON_HEIGHT, load_saved_game, FONT),  # Create Load button
    Button("Exit", button_x, SCREEN_HEIGHT // 2 + 50, BUTTON_WIDTH, BUTTON_HEIGHT, quit_game, FONT)  # Create Exit button
]
# ic(buttons)  # Debugging

# Initialize UI elements before the startup scene
initialize_ui_elements(SCREEN_WIDTH, SCREEN_HEIGHT, FONT, game_state, exit_to_menu, start_day)  # Initialize UI elements
# ic()  # Debugging

def startup_scene():
    """
    Displays the startup scene where the user can choose to start a new game, load a saved game, or exit.

    Returns:
        bool: True if the game should continue running, False if it should quit.
    """
    running = True  # Initialize running flag as True
    # ic(running)  # Debugging
    while running:  # Loop while running is True
        screen.blit(pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))  # Draw the background image
        
        events = pygame.event.get()  # Get the list of events
        running = handle_events(buttons, events, game_state)  # Handle events and update running flag
        # ic(running, events)  # Debugging
        if game_state.quit_game:  # Check if quit_game flag is True
            return False  # Return False to quit the game
        for button in buttons:  # Loop through each button
            button.draw(screen)  # Draw the button on the screen
        pygame.display.flip()  # Update the full display surface to the screen
    # ic()  # Debugging
    return True  # Return True to continue the game

def game_loop():
    """
    Main game loop where the game's primary functionality runs.
    """
    running = True  # Initialize running flag as True
    # ic(running)  # Debugging
    while running:  # Loop while running is True
        screen.fill(WHITE)  # Fill the screen with white color
        events = pygame.event.get()  # Get the list of events
        running = handle_events([], events, game_state)  # Handle events and update running flag
        # ic(running, events)  # Debugging
        
        if not running or game_state.return_to_menu:  # Check if not running or return_to_menu flag is True
            break  # Exit the loop

        if game_state.day_started:  # Check if day_started flag is True
            game_state.customer_manager.simulate_customers(game_state.shop)  # Simulate customer interactions with the shop
            # ic()  # Debugging

        current_inventory = game_state.shop.show_inventory()  # Get the current inventory display
        if current_inventory != '\n'.join(game_state.inventory_display.texts):  # Check if the inventory display has changed
            game_state.inventory_display.add_text(current_inventory)  # Update the inventory display
            # ic(current_inventory)  # Debugging
                
        reviews = game_state.customer_manager.show_reviews()  # Get the current reviews display
        if reviews != '\n'.join(game_state.scrollable_text.texts):  # Check if the reviews display has changed
            game_state.scrollable_text.add_text(reviews)  # Update the reviews display
            # ic(reviews)  # Debugging

        draw_ui_elements(screen, game_state)  # Draw UI elements on the screen
        pygame.display.flip()  # Update the full display surface to the screen
    # ic()  # Debugging

    if game_state.return_to_menu:  # Check if return_to_menu flag is True
        if not startup_scene():  # If the startup scene returns False
            return  # Exit the function
    elif game_state.quit_game:  # Check if quit_game flag is True
        return  # Exit the function

if startup_scene():  # If the startup scene returns True
    pygame.quit()  # Quit Pygame
