import random  # Import random module for generating random values
import datetime  # Import datetime module for date and time manipulation
from constants import SUBS, SIZES  # Import constants for subs and sizes

# DATA
employees = [
    "Dylan Hastings",
    "Morgan Buckner",
    "Jazmyne Chin",
    "Damya Edmonson",
    "Anneyah Flowers",
    "Myles Jackson",
    "Grant Jimerson",
    "Nemaway Jones",
    "Morgan Langdon",
    "Naomi Lopez",
    "Carlos Marion",
    "Rubin Martinez",
    "Sean Matasick",
    "Rolando Robles",
    "Hannah Salazar",
    "Austin Smith",
    "Joshua Walker",
    "Caleb Williams",
]  # List of employee names

payment_methods = ["Visa", "Mastercard", "Amex", "Cash", "DoorDash", "UberEats"]  # List of payment methods

# FUNCTIONS
def get_random_employee():
    """
    Get a random employee name from the list.

    Returns:
        str: Random employee name.
    """
    return random.choice(employees)  # Return a random employee name

def get_random_subs():
    """
    Get a random list of subs with their sizes and prices.

    Returns:
        list: List of tuples containing sub ID, size, and price.
    """
    num_items = random.randint(1, 5)  # Random number of items
    items = random.choices(list(SUBS.keys()), k=num_items)  # Randomly select sub IDs
    sizes = random.choices(list(SIZES.keys()), k=num_items)  # Randomly select sizes
    return [(item, size, random.uniform(5.0, 15.0)) for item, size in zip(items, sizes)]  # Return list of subs with sizes and prices

def get_random_payment_method():
    """
    Get a random payment method from the list.

    Returns:
        str: Random payment method.
    """
    return random.choice(payment_methods)  # Return a random payment method

def get_random_time():
    """
    Get a random time of day.

    Returns:
        str: Random time formatted as a string.
    """
    hour = random.randint(6, 18)  # Random hour between 6 AM and 6 PM
    minute = random.randint(0, 59)  # Random minute
    return datetime.time(hour, minute).strftime("%I:%M %p")  # Return formatted time string

def get_random_date():
    """
    Get the current date.

    Returns:
        str: Current date formatted as a string.
    """
    return datetime.date.today().strftime("%m/%d/%y")  # Return formatted date string

def get_ticket_number():
    """
    Get a random ticket number.

    Returns:
        int: Random ticket number.
    """
    return random.randint(100226901100000, 100226999999999)  # Return a random ticket number

def get_random_phone_number():
    """
    Get a random phone number.

    Returns:
        str: Random phone number formatted as a string.
    """
    return f"{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"  # Return formatted phone number

# FORMAT FUNCTIONS
def format_clock_in(employee):
    """
    Format a clock-in message for an employee.

    Parameters:
        - employee (str): Employee name.

    Returns:
        str: Formatted clock-in message.
    """
    return f"""
----------------------------------------

                Clock In                
              {employee}              
              Time: {get_random_time()}               

----------------------------------------
"""

def format_clock_out(employee):
    """
    Format a clock-out message for an employee.

    Parameters:
        - employee (str): Employee name.

    Returns:
        str: Formatted clock-out message.
    """
    return f"""
----------------------------------------

                Clock Out                
              {employee}              
              Time: {get_random_time()}               

----------------------------------------
"""

def format_order(order_type, items, employee, payment_method):
    """
    Format an order receipt.

    Parameters:
        - order_type (str): Type of order (e.g., "Dine In", "Take Out").
        - items (list): List of items in the order.
        - employee (str): Employee who took the order.
        - payment_method (str): Payment method used.

    Returns:
        str: Formatted order receipt.
    """
    sub_total = sum(item[2] for item in items)  # Calculate subtotal
    tax = round(sub_total * 0.0825, 2)  # Calculate tax
    total = sub_total + tax  # Calculate total
    points = sum(get_points(item[1]) for item in items)  # Calculate loyalty points
    payment_info = f"Paid {payment_method} ************{random.randint(1000, 9999)} ${total:.2f}"  # Format payment information
    loyalty_card = f"Loyalty Card {random.randint(3700000000000000, 3800000000000000)} \n          {points} points earned"  # Format loyalty card information

    return f"""
{order_type}

Jersey Mike's Franchise Systems 15172
7118 FM 1960 E
Atascocita, TX 77346-2702
Phone Number: 281-623-5947

Ticket: {get_ticket_number()}
===================================
Server: {employee}   {get_random_date()} {get_random_time()}
===================================
{format_items(items)}
   ================================
              Sub Total    ${sub_total:.2f}  
              Taxable      ${sub_total:.2f}  
              8.25% Tax     ${tax:.2f}  
              Total        ${total:.2f}  

{payment_info}         
{loyalty_card}
===================================
   ORDERED BY:                     
     {get_random_name()}                     
     Phone: {get_random_phone_number()}             
     Pickup: {get_random_date()} {get_random_time()}      

----------------------------------------
"""

def format_items(items):
    """
    Format the items in an order.

    Parameters:
        - items (list): List of items in the order.

    Returns:
        str: Formatted items string.
    """
    return "\n".join([f"   {item[0]} ({item[1]})              {item[2]:.2f} T" for item in items])  # Return formatted items string

def get_random_name():
    """
    Get a random name.

    Returns:
        str: Random name.
    """
    first_names = ["John", "Jane", "Alex", "Emily", "Chris", "Katie", "Michael", "Sarah"]  # List of first names
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]  # List of last names
    return f"{random.choice(first_names)} {random.choice(last_names)}"  # Return a random name

def get_points(size):
    """
    Get loyalty points based on sub size.

    Parameters:
        - size (str): Size of the sub.

    Returns:
        int: Loyalty points for the size.
    """
    points_map = {
        'MINI': 4,
        'REGULAR': 6,
        'GIANT': 12
    }
    return points_map.get(size.upper(), 0)  # Return loyalty points for the size

# MAIN FUNCTION
def simulate_activity(shop):
    """
    Simulate a day's activity in the shop.

    Parameters:
        - shop (Shop): The shop instance.
    """
    output = ""  # Initialize output string

    # SIM CLOCK-INS
    for _ in range(5):
        employee = get_random_employee()  # Get a random employee
        output += format_clock_in(employee)  # Add clock-in message to output

    # SIM ORDERS
    for _ in range(20):
        order_type = random.choice(["Dine In", "Take Out"])  # Randomly choose order type
        items = get_random_subs()  # Get random subs
        employee = get_random_employee()  # Get a random employee
        payment_method = get_random_payment_method()  # Get a random payment method
        output += format_order(order_type, items, employee, payment_method)  # Add formatted order to output

    # SIM CLOCK-OUTS
    for _ in range(5):
        employee = get_random_employee()  # Get a random employee
        output += format_clock_out(employee)  # Add clock-out message to output

    print(output)  # Print the output

