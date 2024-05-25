from decimal import Decimal, InvalidOperation  # Import Decimal for precise decimal arithmetic and InvalidOperation for exception handling
import json  # Import json module for handling JSON data
import os  # Import os module for interacting with the operating system
import random  # Import random module for generating random values

import pygame  # Import Pygame module for game development

from constants import EXTRAS, SIZES, SUBS  # Import constants for extras, sizes, and subs
from data_handler import Item  # Import Item class from data_handler module

class Shop:
    """
    Shop class to manage the shop's inventory, cash, and operations.

    Attributes:
        - inventory (dict): Dictionary storing items in the inventory.
        - cash (Decimal): The shop's cash balance.
        - product_map (dict): Dictionary mapping product numbers to names.
        - cleanliness (int): Cleanliness level of the shop (0-20).
        - customer_service (int): Customer service level of the shop (0-20).
    """
    def __init__(self):
        """
        Initialize a Shop object.
        """
        self.inventory = {}  # Initialize an empty inventory dictionary
        self.cash = Decimal(1000.0)  # Set initial cash balance to $1000.00
        self.product_map = {}  # Initialize an empty product map
        self.cleanliness = 20  # Set initial cleanliness level
        self.customer_service = 20  # Set initial customer service level

    def add_item(self, item):
        """
        Add an item to the shop's inventory.

        Parameters:
            - item (Item): The item to add.
        """
        self.inventory[item.product_number] = item  # Add the item to inventory
        self.product_map[item.product_number] = item.name  # Map the product number to the item name

    def buy_stock_by_text(self, item_text):
        """
        Buy stock using item text description.

        Parameters:
            - item_text (str): The item text description.

        Returns:
            str: Result message of the stock purchase.
        """
        product_number = item_text.split(',')[0].split(':')[-1].strip()  # Extract product number from text
        quantity = 1  # Default quantity
        return self.buy_stock(product_number, quantity)  # Buy stock

    def buy_stock(self, product_number, quantity):
        """
        Buy stock for a given product number and quantity.

        Parameters:
            - product_number (str): The product number.
            - quantity (int or str): The quantity to buy.

        Returns:
            str: Result message of the stock purchase.
        """
        if product_number not in self.inventory:  # Check if product is in inventory
            return "Item not found in inventory."

        try:
            quantity = Decimal(quantity)  # Convert quantity to Decimal
        except InvalidOperation:  # Handle invalid quantity
            return "Invalid quantity."

        item = self.inventory[product_number]  # Get the item from inventory
        cost = item.unit_price * quantity  # Calculate the total cost
        if self.cash < cost:  # Check if enough cash is available
            return "Not enough cash to buy this stock."

        self.cash -= cost  # Deduct the cost from cash
        item.stock += quantity  # Add the quantity to the item's stock
        return f"Bought {quantity:.2f} {item.vendor_unit} of {item.name} for ${cost:.2f}"

    def sell_sub(self, sub_id, size='REGULAR', bread_type='WHITE', extras=[]):
        """
        Sell a sub to a customer.

        Parameters:
            - sub_id (str): The ID of the sub.
            - size (str): The size of the sub (default is 'REGULAR').
            - bread_type (str): The type of bread (default is 'WHITE').
            - extras (list): List of extras to add to the sub.

        Returns:
            str: Result message of the sub sale.
        """
        if sub_id not in SUBS:  # Check if sub ID exists
            return "Sub ID not found."

        required_ingredients = SUBS[sub_id]  # Get the required ingredients for the sub
        size_multiplier = SIZES[size.upper()]  # Get the size multiplier
        total_price = 0  # Initialize total price

        for ingredient in required_ingredients:  # Check if required ingredients are in stock
            required_amount = Decimal(size_multiplier)
            if ingredient not in self.inventory or self.inventory[ingredient].stock < required_amount:
                ingredient_name = self.product_map.get(ingredient, "Unknown Product")
                return f"Not enough stock of {ingredient_name} to make {size} {bread_type} {sub_id}."

        for ingredient in required_ingredients:  # Deduct ingredients from stock and calculate total price
            required_amount = Decimal(size_multiplier)
            self.inventory[ingredient].stock -= required_amount
            total_price += self.inventory[ingredient].price_per_unit * required_amount

        for extra in extras:  # Add extras if available
            if extra in EXTRAS and random.random() < EXTRAS[extra]:
                extra_item = self.product_map.get(extra, "Unknown Product")
                if extra in self.inventory and self.inventory[extra].stock >= 1:
                    self.inventory[extra].stock -= 1
                    total_price += self.inventory[extra].price_per_unit
                else:
                    return f"Not enough stock of {extra_item} to add to {size} {bread_type} {sub_id}."

        revenue = total_price * Decimal(1.5)  # Calculate revenue
        self.cash += revenue  # Add revenue to cash

        return f"Sold a {size} {bread_type} {sub_id} with extras for ${revenue:.2f}"

    def show_inventory(self):
        """
        Show the current inventory.

        Returns:
            str: String representation of the inventory.
        """
        inventory_list = [str(item) for item in self.inventory.values()]  # Get string representation of each item
        return "\n".join(inventory_list)  # Join the item strings with newline

    def save_game(self, filename='savegame.json'):
        """
        Save the game state to a file.

        Parameters:
            - filename (str): The filename to save the game state.
        """
        data = {
            'cash': str(self.cash),
            'inventory': {k: {'name': v.name, 'unit_price': str(v.unit_price), 'vendor_unit': v.vendor_unit, 'stock': str(v.stock)} for k, v in self.inventory.items()}
        }
        with open(filename, 'w') as f:  # Open the file for writing
            json.dump(data, f)  # Dump the data to the file

    def load_game(self, filename='savegame.json'):
        """
        Load the game state from a file.

        Parameters:
            - filename (str): The filename to load the game state from.

        Returns:
            bool: True if the game state is loaded successfully, False otherwise.
        """
        if not os.path.exists(filename):  # Check if the file exists
            return False

        with open(filename, 'r') as f:  # Open the file for reading
            data = json.load(f)  # Load the data from the file
        self.cash = Decimal(data['cash'])  # Load cash value
        self.inventory = {k: Item(k, v['name'], v['unit_price'], v['vendor_unit']) for k, v in data['inventory'].items()}  # Load inventory
        for k, v in data['inventory'].items():  # Set stock for each item
            self.inventory[k].stock = Decimal(v['stock'])
            self.product_map[k] = v['name']
        return True

    def adjust_cleanliness(self, amount):
        """
        Adjust the cleanliness level.

        Parameters:
            - amount (int): The amount to adjust cleanliness by.
        """
        self.cleanliness = max(0, min(20, self.cleanliness + amount))  # Ensure cleanliness is within bounds

    def adjust_customer_service(self, amount):
        """
        Adjust the customer service level.

        Parameters:
            - amount (int): The amount to adjust customer service by.
        """
        self.customer_service = max(0, min(20, self.customer_service + amount))  # Ensure customer service is within bounds

def begin_day(shop):
    """
    Simulate the start of a business day.

    Parameters:
        - shop (Shop): The shop instance.
    
    Returns:
        str: Message indicating the store is closed for the day.
    """
    store_open = True  # Initialize store_open flag
    start_time = 10 * 60  # Set store opening time (10 AM in minutes)
    end_time = 21 * 60  # Set store closing time (9 PM in minutes)
    current_time = start_time  # Initialize current time

    popularity = 50  # Set initial popularity

    while store_open:
        pygame.time.wait(1000)  # Simulate each minute
        current_time += 1  # Increment the current time

        if current_time >= end_time:  # Check if the store should close
            store_open = False
            return "Store is closed for the day."

        if random.randint(0, 100) < popularity:  # Generate customer orders based on popularity
            generate_customer_order(shop)

        popularity = adjust_popularity(popularity)  # Adjust popularity

    return "Day ended."

def generate_customer_order(shop):
    """
    Generate a random customer order.

    Parameters:
        - shop (Shop): The shop instance.
    """
    sub_id = random.choice(list(SUBS.keys()))  # Choose a random sub ID
    quantity = random.randint(1, 5)  # Random quantity
    shop.sell_sub(sub_id)  # Sell the sub

def adjust_popularity(popularity):
    """
    Adjust the shop's popularity.

    Parameters:
        - popularity (int): The current popularity.
    
    Returns:
        int: The adjusted popularity.
    """
    return min(100, max(0, popularity + random.randint(-5, 5)))  # Adjust popularity within bounds
