import os
import random  # Import random module for generating random values
from decimal import Decimal  # Import Decimal for precise decimal arithmetic
from constants import SUBS, SIZES, EXTRAS, TOPPINGS  # Import constants for subs, sizes, extras, and toppings

class Customer:
    """
    Customer class to manage customer information and behaviors.

    Attributes:
        - name (str): Name of the customer.
        - mood (int): Mood of the customer.
        - cleanliness (int): Customer's cleanliness preference.
        - customer_service (int): Customer's customer service preference.
        - order_history (list): List of previous orders made by the customer.
    """
    def __init__(self, name, mood, cleanliness, customer_service):
        """
        Initialize a Customer object.

        Parameters:
            - name (str): Name of the customer.
            - mood (int): Mood of the customer.
            - cleanliness (int): Customer's cleanliness preference.
            - customer_service (int): Customer's customer service preference.
        """
        self.name = name  # Assign the name
        self.mood = mood  # Assign the mood
        self.cleanliness = cleanliness  # Assign cleanliness preference
        self.customer_service = customer_service  # Assign customer service preference
        self.order_history = []  # Initialize an empty order history

    def generate_order(self):
        """
        Generate a random order for the customer.

        Returns:
            dict: A dictionary containing order details.
        """
        sub_id = random.choice(list(SUBS.keys()))  # Randomly select a sub ID
        size = random.choice(list(SIZES.keys()))  # Randomly select a size
        bread_type = random.choice(['WHITE', 'WHEAT', 'RP'])  # Randomly select a bread type
        extras = self.choose_extras()  # Choose extras for the order
        return {
            'sub_id': sub_id,
            'size': size,
            'bread_type': bread_type,
            'extras': extras
        }

    def choose_extras(self):
        """
        Choose extras for the order.

        Returns:
            list: A list of selected extras.
        """
        base_extras = ['LETTUCE', 'ONIONS', 'TOMATO', 'OIL', 'VINEGAR', 'OREGANO', 'SALT']  # Base extras
        additional_extras = [extra for extra in TOPPINGS if extra not in base_extras]  # Additional extras not in base
        selected_extras = base_extras[:]  # Start with base extras
        for extra in additional_extras:  # Iterate through additional extras
            if random.random() < 0.5:  # 50% chance to add each extra
                selected_extras.append(extra)
        return selected_extras

    def review_experience(self, order_successful, shop_cleanliness, customer_service):
        """
        Review the customer's experience.

        Parameters:
            - order_successful (bool): Whether the order was successful.
            - shop_cleanliness (int): Cleanliness score of the shop.
            - customer_service (int): Customer service score of the shop.

        Returns:
            int: The review score.
        """
        review_score = self.mood  # Start with the customer's mood
        if order_successful:  # Adjust score based on order success
            review_score += 10
        else:
            review_score -= 20

        review_score += shop_cleanliness + customer_service  # Add shop cleanliness and customer service scores
        review_score = max(0, min(100, review_score))  # Ensure the score is between 0 and 100
        return review_score

    def decide_to_return(self, review_score):
        """
        Decide whether the customer will return based on the review score.

        Parameters:
            - review_score (int): The review score.

        Returns:
            bool: True if the customer will return, False otherwise.
        """
        return review_score >= 50  # Return True if review score is 50 or higher, otherwise False

def load_customer_names(filename='customer_names.txt'):
    """
    Load customer names from a file.

    Parameters:
        - filename (str): The filename containing customer names.

    Returns:
        list: A list of customer names.
    """
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'r') as file:  # Open the file in read mode
        names = file.read().splitlines()  # Read lines and split into a list
    return names

def generate_customers():
    """
    Generate random customers.

    Returns:
        list: A list of Customer objects.
    """
    customer_names = load_customer_names()  # Load customer names from file
    random.shuffle(customer_names)  # Shuffle the names to ensure randomness
    customers = []  # Initialize an empty list of customers
    name_set = set()  # Initialize an empty set to track used names
    while len(customers) < len(customer_names):  # Ensure the number of customers matches the number of names
        name = customer_names.pop()  # Get a name from the list
        if name not in name_set:  # Ensure the name is not already used
            name_set.add(name)  # Add the name to the set
            mood = random.randint(40, 60)  # Generate a random mood
            cleanliness = random.randint(0, 20)  # Generate a random cleanliness score
            customer_service = random.randint(0, 20)  # Generate a random customer service score
            customers.append(Customer(name, mood, cleanliness, customer_service))  # Create a Customer object and add to the list
    return customers
