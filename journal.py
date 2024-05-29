import random
import datetime
from constants import SUBS, SIZES

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
]

payment_methods = ["Visa", "Mastercard", "Amex", "Cash", "DoorDash", "UberEats"]

def get_random_employee():
    return random.choice(employees)

def get_random_subs():
    num_items = random.randint(1, 5)
    items = random.choices(list(SUBS.keys()), k=num_items)
    sizes = random.choices(list(SIZES.keys()), k=num_items)
    return [(item, size, random.uniform(5.0, 15.0)) for item, size in zip(items, sizes)]

def get_random_payment_method():
    return random.choice(payment_methods)

def get_random_time():
    hour = random.randint(6, 18)
    minute = random.randint(0, 59)
    return datetime.time(hour, minute).strftime("%I:%M %p")

def get_random_date():
    return datetime.date.today().strftime("%m/%d/%y")

def get_ticket_number():
    return random.randint(100226901100000, 100226999999999)

def get_random_phone_number():
    return f"{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"

def format_clock_in(employee):
    return f"""
----------------------------------------

                Clock In                
              {employee}              
              Time: {get_random_time()}               

----------------------------------------
"""

def format_clock_out(employee):
    return f"""
----------------------------------------

                Clock Out                
              {employee}              
              Time: {get_random_time()}               

----------------------------------------
"""

def format_order(order_type, items, employee, payment_method):
    sub_total = sum(item[2] for item in items)
    tax = round(sub_total * 0.0825, 2)
    total = sub_total + tax
    points = sum(get_points(item[1]) for item in items)
    payment_info = f"Paid {payment_method} ************{random.randint(1000, 9999)} ${total:.2f}"
    loyalty_card = f"Loyalty Card {random.randint(3700000000000000, 3800000000000000)} \n          {points} points earned"

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
    return "\n".join([f"   {item[0]} ({item[1]})              {item[2]:.2f} T" for item in items])

def get_random_name():
    first_names = ["John", "Jane", "Alex", "Emily", "Chris", "Katie", "Michael", "Sarah"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def get_points(size):
    points_map = {
        'MINI': 4,
        'REGULAR': 6,
        'GIANT': 12
    }
    return points_map.get(size.upper(), 0)

def simulate_activity(shop):
    output = ""

    for _ in range(5):
        employee = get_random_employee()
        output += format_clock_in(employee)

    for _ in range(20):
        order_type = random.choice(["Dine In", "Take Out"])
        items = get_random_subs()
        employee = get_random_employee()
        payment_method = get_random_payment_method()
        output += format_order(order_type, items, employee, payment_method)

    for _ in range(5):
        employee = get_random_employee()
        output += format_clock_out(employee)

    print(output)
