import re
from decimal import Decimal, InvalidOperation
from icecream import ic

class Item:
    def __init__(self, product_number, name, unit_price, vendor_unit):
        ic(f"Creating item: {product_number}, {name}, {unit_price}, {vendor_unit}")
        self.product_number = product_number
        self.name = name
        self.unit_price = Decimal(unit_price.replace('$', ''))
        self.vendor_unit = vendor_unit
        self.stock = Decimal(0)
        self.price_per_unit = self.calculate_price_per_unit()
        ic(self)

    def calculate_price_per_unit(self):
        parts = self.vendor_unit.split('/')
        if len(parts) != 2:
            return self.unit_price

        try:
            num_units = Decimal(parts[0])
            unit_quantity = Decimal(re.findall(r"(\d+(\.\d+)?)", parts[1])[0][0])
            total_units = num_units * unit_quantity
            return self.unit_price / total_units
        except (IndexError, ValueError, InvalidOperation) as e:
            ic(e)
            return self.unit_price

    def __repr__(self):
        return (f"Product Number: {self.product_number}, {self.name} - ${self.unit_price:.2f} per {self.vendor_unit} "
                f"(${self.price_per_unit:.3f} per unit, Stock: {self.stock:.2f} {self.vendor_unit})")

def parse_data(data):
    ic("Parsing data")
    lines = data.strip().split("\n")
    items = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if re.match(r'^\d+$', line):
            try:
                product_number = line
                name = lines[i+1].strip()
                unit_price = lines[i+4].strip()
                vendor_unit = lines[i+6].strip()
                items.append(Item(product_number, name, unit_price, vendor_unit))
                i += 7
            except IndexError as e:
                ic(e)
                i += 1
        i += 1
    ic(items)
    return items
