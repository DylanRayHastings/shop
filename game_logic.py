from decimal import Decimal, InvalidOperation
import json
import os
import random

import pygame

from constants import EXTRAS, SIZES, SUBS
from data_handler import Item

class Shop:
    def __init__(self):
        self.inventory = {}
        self.cash = Decimal(1000.0)
        self.product_map = {}
        self.cleanliness = 20
        self.customer_service = 20

    def add_item(self, item):
        self.inventory[item.product_number] = item
        self.product_map[item.product_number] = item.name

    def buy_stock_by_text(self, item_text):
        product_number = item_text.split(',')[0].split(':')[-1].strip()
        quantity = 1
        return self.buy_stock(product_number, quantity)

    def buy_stock(self, product_number, quantity):
        if product_number not in self.inventory:
            return "Item not found in inventory."

        try:
            quantity = Decimal(quantity)
        except InvalidOperation:
            return "Invalid quantity."

        item = self.inventory[product_number]
        cost = item.unit_price * quantity
        if self.cash < cost:
            return "Not enough cash to buy this stock."

        self.cash -= cost
        item.stock += quantity
        return f"Bought {quantity:.2f} {item.vendor_unit} of {item.name} for ${cost:.2f}"

    def sell_sub(self, sub_id, size='REGULAR', bread_type='WHITE', extras=[]):
        if sub_id not in SUBS:
            return "Sub ID not found."

        required_ingredients = SUBS[sub_id]
        size_multiplier = SIZES[size.upper()]
        total_price = 0

        for ingredient in required_ingredients:
            required_amount = Decimal(size_multiplier)
            if ingredient not in self.inventory or self.inventory[ingredient].stock < required_amount:
                ingredient_name = self.product_map.get(ingredient, "Unknown Product")
                return f"Not enough stock of {ingredient_name} to make {size} {bread_type} {sub_id}."

        for ingredient in required_ingredients:
            required_amount = Decimal(size_multiplier)
            self.inventory[ingredient].stock -= required_amount
            total_price += self.inventory[ingredient].price_per_unit * required_amount

        for extra in extras:
            if extra in EXTRAS and random.random() < EXTRAS[extra]:
                extra_item = self.product_map.get(extra, "Unknown Product")
                if extra in self.inventory and self.inventory[extra].stock >= 1:
                    self.inventory[extra].stock -= 1
                    total_price += self.inventory[extra].price_per_unit
                else:
                    return f"Not enough stock of {extra_item} to add to {size} {bread_type} {sub_id}."

        revenue = total_price * Decimal(1.5)
        self.cash += revenue

        return f"Sold a {size} {bread_type} {sub_id} with extras for ${revenue:.2f}"

    def show_inventory(self):
        inventory_list = [str(item) for item in self.inventory.values()]
        return "\n".join(inventory_list)

    def save_game(self, filename='savegame.json'):
        data = {
            'cash': str(self.cash),
            'inventory': {k: {'name': v.name, 'unit_price': str(v.unit_price), 'vendor_unit': v.vendor_unit, 'stock': str(v.stock)} for k, v in self.inventory.items()}
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_game(self, filename='savegame.json'):
        if not os.path.exists(filename):
            return False

        with open(filename, 'r') as f:
            data = json.load(f)
        self.cash = Decimal(data['cash'])
        self.inventory = {k: Item(k, v['name'], v['unit_price'], v['vendor_unit']) for k, v in data['inventory'].items()}
        for k, v in data['inventory'].items():
            self.inventory[k].stock = Decimal(v['stock'])
            self.product_map[k] = v['name']
        return True

    def adjust_cleanliness(self, amount):
        self.cleanliness = max(0, min(20, self.cleanliness + amount))

    def adjust_customer_service(self, amount):
        self.customer_service = max(0, min(20, self.customer_service + amount))

def begin_day(shop):
    store_open = True
    start_time = 10 * 60
    end_time = 21 * 60
    current_time = start_time

    popularity = 50

    while store_open:
        pygame.time.wait(1000)
        current_time += 1

        if current_time >= end_time:
            store_open = False
            return "Store is closed for the day."

        if random.randint(0, 100) < popularity:
            generate_customer_order(shop)

        popularity = adjust_popularity(popularity)

    return "Day ended."

def generate_customer_order(shop):
    sub_id = random.choice(list(SUBS.keys()))
    quantity = random.randint(1, 5)
    shop.sell_sub(sub_id)

def adjust_popularity(popularity):
    return min(100, max(0, popularity + random.randint(-5, 5)))
