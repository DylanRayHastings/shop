import re  # Import regular expression module for string matching and manipulation
from decimal import Decimal, InvalidOperation  # Import Decimal for precise decimal arithmetic and InvalidOperation for exception handling
from icecream import ic  # Import icecream for debugging and logging

class Item:
    """
    Item class to represent and manage individual items in inventory.

    Attributes:
        - product_number (str): The product number of the item.
        - name (str): The name of the item.
        - unit_price (Decimal): The unit price of the item.
        - vendor_unit (str): The vendor unit description of the item.
        - stock (Decimal): The current stock of the item.
        - price_per_unit (Decimal): The calculated price per individual unit.
    """
    def __init__(self, product_number, name, unit_price, vendor_unit):
        """
        Initialize an Item object.

        Parameters:
            - product_number (str): The product number of the item.
            - name (str): The name of the item.
            - unit_price (str): The unit price of the item as a string.
            - vendor_unit (str): The vendor unit description of the item.
        """
        ic(f"Creating item: {product_number}, {name}, {unit_price}, {vendor_unit}")  # Log the creation of the item
        self.product_number = product_number  # Assign the product number
        self.name = name  # Assign the name
        self.unit_price = Decimal(unit_price.replace('$', ''))  # Convert and assign the unit price as a Decimal
        self.vendor_unit = vendor_unit  # Assign the vendor unit
        self.stock = Decimal(0)  # Initialize the stock to 0
        self.price_per_unit = self.calculate_price_per_unit()  # Calculate and assign the price per unit
        ic(self)  # Log the created item

    def calculate_price_per_unit(self):
        """
        Calculate the price per individual unit based on the vendor unit.

        Returns:
            Decimal: The price per individual unit.
        """
        parts = self.vendor_unit.split('/')  # Split the vendor unit into parts
        if len(parts) != 2:  # Check if the parts are not equal to 2
            return self.unit_price  # Return the unit price if split is not valid

        try:
            num_units = Decimal(parts[0])  # Convert the first part to Decimal
            unit_quantity = Decimal(re.findall(r"(\d+(\.\d+)?)", parts[1])[0][0])  # Extract and convert the quantity to Decimal
            total_units = num_units * unit_quantity  # Calculate the total units
            return self.unit_price / total_units  # Return the price per unit
        except (IndexError, ValueError, InvalidOperation) as e:  # Handle exceptions
            ic(e)  # Log the exception
            return self.unit_price  # Return the unit price if an exception occurs

    def __repr__(self):
        """
        Return a string representation of the item.

        Returns:
            str: String representation of the item.
        """
        return (f"Product Number: {self.product_number}, {self.name} - ${self.unit_price:.2f} per {self.vendor_unit} "
                f"(${self.price_per_unit:.3f} per unit, Stock: {self.stock:.2f} {self.vendor_unit})")

def parse_data(data):
    """
    Parse data to create Item objects.

    Parameters:
        - data (str): The data string containing item information.

    Returns:
        list: List of Item objects.
    """
    ic("Parsing data")  # Log the start of data parsing
    lines = data.strip().split("\n")  # Split the data into lines
    items = []  # Initialize an empty list to store items
    i = 0  # Initialize the line index
    while i < len(lines):  # Loop through the lines
        line = lines[i].strip()  # Strip whitespace from the current line
        if re.match(r'^\d+$', line):  # Check if the line matches a product number format
            try:
                product_number = line  # Assign the product number
                name = lines[i+1].strip()  # Get and strip the name from the next line
                unit_price = lines[i+4].strip()  # Get and strip the unit price from the fifth line
                vendor_unit = lines[i+6].strip()  # Get and strip the vendor unit from the seventh line
                items.append(Item(product_number, name, unit_price, vendor_unit))  # Create an Item object and add to the list
                i += 7  # Move to the next item block
            except IndexError as e:  # Handle index errors
                ic(e)  # Log the exception
                i += 1  # Move to the next line
        else:
            i += 1  # Move to the next line if the format doesn't match
    ic(items)  # Log the parsed items
    return items  # Return the list of items
