import random
from .customers import Customer

class CustomerManager:
    """
    CustomerManager class to manage multiple customers.

    Attributes:
        - customers (list): List of current customers.
        - regular_customers (list): List of regular customers.
        - reviews (list): List of reviews.
    """
    def __init__(self):
        """
        Initialize a CustomerManager object.
        """
        self.customers = []  # Initialize an empty list of customers
        self.regular_customers = []  # Initialize an empty list of regular customers
        self.reviews = []  # Initialize an empty list of reviews

    def add_customer(self, customer):
        """
        Add a customer to the list.

        Parameters:
            - customer (Customer): The customer to be added.
        """
        self.customers.append(customer)  # Append the customer to the customers list

    def simulate_customers(self, shop):
        """
        Simulate customer interactions with the shop.

        Parameters:
            - shop (Shop): The shop instance.
        """
        for customer in self.customers:  # Iterate through each customer
            order = customer.generate_order()  # Generate an order for the customer
            result = shop.sell_sub(order['sub_id'], order['size'], order['bread_type'], order['extras'])  # Attempt to sell the sub
            order_successful = "Sold" in result  # Check if the order was successful
            review_score = customer.review_experience(order_successful, shop.cleanliness, shop.customer_service)  # Get the review score
            self.reviews.append({
                'customer': customer.name,
                'review_score': review_score,
                'order_successful': order_successful
            })  # Add the review to the reviews list

            if customer.decide_to_return(review_score):  # Check if the customer decides to return
                self.regular_customers.append(customer)  # Add to regular customers
            else:
                self.customers.remove(customer)  # Remove from customers

    def show_reviews(self):
        """
        Show all reviews.

        Returns:
            str: A string representation of all reviews.
        """
        return "\n".join([f"{review['customer']}: {review['review_score']} (Order Successful: {review['order_successful']})" for review in self.reviews])  # Format and join reviews
