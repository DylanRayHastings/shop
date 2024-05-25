"""
Employee Management System

This script defines a simple Employee class and functions for generating random employee data and scheduling shifts.
"""
import random  # Import the random module for generating random values
from datetime import datetime, timedelta  # Import datetime and timedelta for date and time manipulation
from collections import defaultdict  # Import defaultdict for dictionary with default values
from icecream import ic  # Import icecream for debugging and logging

# Define role availability with start and end times
role_availability = {
    "Opener": {"start": 700, "end": 1400},
    "Open Support": {"start": 900, "end": 1400},
    "Rush Support": {"start": 1000, "end": 1400},
    "Close Support": {"start": 1400, "end": 2000},
    "Closer": {"start": 1600, "end": 2130},
    "Shift Lead": {"start": 700, "end": 2130},
}

class Employee:
    """
    Employee class for managing employee information and scheduling shifts.

    Attributes:
        - name (str): Name of the employee.
        - employee_id (str): Unique identifier for the employee.
        - role (str): Role of the employee (e.g., "Opener", "Shift Lead").
        - shifts (list): List of shifts the employee is available for.
        - rating (float): Employee's rating on a scale from 3.0 to 5.0.
        - trained (bool): Flag indicating whether the employee is trained.
        - current_task (str): Current task the employee is performing.
        - activities_log (list): List of activities logged by the employee.
    """
    def __init__(self, name, employee_id, role=None, shifts=None, rating=None):
        """
        Initialize an Employee object.

        Parameters:
            - name (str): Name of the employee.
            - employee_id (str): Unique identifier for the employee.
            - role (str): Role of the employee (e.g., "Opener", "Shift Lead").
            - shifts (list): List of shifts the employee is available for.
            - rating (float): Employee's rating on a scale from 3.0 to 5.0.
        """
        self.name = name  # Assign the name
        self.employee_id = employee_id  # Assign the employee ID
        self.role = role if role else "Default"  # Assign the role, default to "Default" if not provided
        self.shifts = shifts  # Assign the shifts
        self.rating = rating  # Assign the rating
        self.trained = False  # Initialize the trained flag as False
        self.current_task = None  # Initialize the current task as None
        self.activities_log = []  # Initialize an empty activities log

    def train(self, trainer=None):
        """
        Conduct training for the employee.

        Parameters:
            - trainer (Employee, optional): Trainer employee (default is None).
        """
        if trainer and not trainer.trained:
            ic(f'Trainer {trainer.employee_id} is not trained. Training cannot be conducted.')  # Log if trainer is not trained
            return
        if not self.trained:
            ic(f'Employee {self.employee_id} ({self.role}) is undergoing training.')  # Log the training process
            self.trained = True  # Mark the employee as trained
        else:
            ic(f'Employee {self.employee_id} ({self.role}) is already trained.')  # Log if the employee is already trained

    def perform_task(self, task, duration_minutes):
        """
        Perform a task and log the activity.

        Parameters:
            - task (str): Task to be performed.
            - duration_minutes (int): Duration of the task in minutes.
        """
        if not self.trained:
            ic(f'Employee {self.employee_id} ({self.role}) cannot perform tasks without training.')  # Log if the employee is not trained
        else:
            ic(f'Employee {self.employee_id} ({self.role}) is performing {task}.')  # Log the task being performed
            self.current_task = task  # Assign the current task
            self.log_activity(task, duration_minutes)  # Log the activity

    def log_activity(self, task, duration_minutes):
        """
        Log an activity in the activities log.

        Parameters:
            - task (str): Task to be logged.
            - duration_minutes (int): Duration of the task in minutes.
        """
        current_time = datetime.now()  # Get the current time
        end_time = current_time + timedelta(minutes=duration_minutes)  # Calculate the end time
        self.activities_log.append({'task': task, 'start_time': current_time, 'end_time': end_time})  # Log the activity

    def work_shift(self):
        """
        Simulate the employee working a shift.
        """
        current_time = datetime.now()  # Get the current time
        current_shift = None  # Initialize the current shift as None

        for shift in self.shifts:  # Find the current shift based on time
            if shift['start'] <= current_time.time() <= shift['end']:
                current_shift = shift
                break

        if not current_shift:  # Check if the current shift is found
            ic(f'Employee {self.employee_id} ({self.role}) is not scheduled for a shift at the moment.')
            return

        while current_time.time() <= current_shift['end']:  # Simulate the shift work until end time
            if current_time.time() == datetime.strptime('09:30', '%H:%M').time():
                self.perform_task('Prepare ingredients', duration_minutes=10)
            elif current_time.time() == datetime.strptime('10:30', '%H:%M').time():
                self.perform_task('Assemble sandwiches', duration_minutes=15)
            elif current_time.time() == datetime.strptime('12:00', '%H:%M').time():
                self.perform_task('Lunch break', duration_minutes=30)
            elif current_time.time() == datetime.strptime('15:30', '%H:%M').time():
                self.perform_task('Clean and restock', duration_minutes=20)

            current_time += timedelta(minutes=1)  # Increment the current time by one minute

        ic(f'Employee {self.employee_id} ({self.role}) has completed the {current_shift["shift_name"]} shift.')

def generate_random_availability(role):
    """
    Generate random availability for a given role.

    Parameters:
        - role (str): Role of the employee.

    Returns:
        tuple: Start time, end time, and day of the week.
    """
    if role not in role_availability:
        role = "Default"  # Default role if not found in role_availability

    day = random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])  # Random day of the week
    start_time = role_availability[role]["start"]  # Start time based on role
    end_time = role_availability[role]["end"]  # End time based on role

    return start_time, end_time, day

def generate_random_employee_objects(employees_data):
    """
    Generate random employee objects from given employee data.

    Parameters:
        - employees_data (dict): Dictionary containing employee data.

    Returns:
        dict: Dictionary of Employee objects.
    """
    employees_objects = {}
    for employee_id, data in employees_data.items():  # Iterate through employee data
        role = data['role']
        rating = data['rating']
        name = data['name']
        shifts = data['availability']

        employee = Employee(name=name, employee_id=employee_id, role=role, shifts=shifts, rating=rating)  # Create Employee object
        employees_objects[employee_id] = employee  # Add to employees_objects dictionary
    return employees_objects

def generate_random_employee_data(num_employees):
    """
    Generate random employee data.

    Parameters:
        - num_employees (int): Number of employees to generate.

    Returns:
        dict: Dictionary of employee data.
    """
    employees_data = {}
    for i in range(num_employees):  # Generate data for each employee
        role = random.choice(["Opener", "Open Support", "Rush Support", "Close Support", "Closer", "Shift Lead"])
        availability = [generate_random_availability(role) for _ in range(random.randint(2, 5))]  # Generate random availability
        name = ''  # Placeholder for employee name
        employee_id = generate_employee_id()  # Generate unique employee ID
        employees_data[employee_id] = {
            'name': name,
            'role': role,
            'availability': availability,
            'rating': round(random.uniform(3.0, 5.0), 1),
        }
    return employees_data

def generate_employee_id():
    """
    Generate a unique employee ID.

    Returns:
        str: Unique employee ID.
    """
    return f"EMP_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"

def calculate_shift_duration(start_time, end_time):
    """
    Calculate the duration of a shift.

    Parameters:
        - start_time (int): Start time of the shift in HHMM format.
        - end_time (int): End time of the shift in HHMM format.

    Returns:
        float: Duration of the shift in hours.
    """
    start_datetime = datetime.strptime(str(start_time), "%H%M")  # Convert start time to datetime
    end_datetime = datetime.strptime(str(end_time), "%H%M")  # Convert end time to datetime
    duration = end_datetime - start_datetime  # Calculate duration
    return duration.total_seconds() / 3600.0  # Return duration in hours

def check_availability(employee, shift, role_availability):
    """
    Check if an employee is available for a given shift.

    Parameters:
        - employee (Employee): The employee object.
        - shift (tuple): The shift to check availability for.
        - role_availability (dict): Dictionary of role availabilities.

    Returns:
        bool: True if the employee is available, False otherwise.
    """
    start_time, end_time, day = shift

    if role_availability.get(employee.role):  # Get role availability
        role_start_time = role_availability[employee.role]["start"]
        role_end_time = role_availability[employee.role]["end"]
    else:
        role_start_time, role_end_time = 700, 2130  # Default availability

    is_available = role_start_time <= start_time <= role_end_time and role_start_time <= end_time <= role_end_time  # Check availability
    ic(f"  - Employee {employee.employee_id} ({employee.role}) availability for shift ({start_time}-{end_time}): {is_available}")

    return is_available

def schedule_employee(shift, required_role, hours_worked, final_schedule, role_availability, day):
    """
    Schedule an employee for a shift.

    Parameters:
        - shift (tuple): The shift to be scheduled.
        - required_role (str): The required role for the shift.
        - hours_worked (dict): Dictionary of hours worked by employees.
        - final_schedule (dict): Dictionary of the final schedule.
        - role_availability (dict): Dictionary of role availabilities.
        - day (str): Day of the week.

    Returns:
        int: 1 if successfully scheduled, 0 otherwise.
    """
    employee_id, start_time, end_time = shift

    if employee_id in role_availability[required_role] and (employee_id not in final_schedule or not is_overlapping(final_schedule[employee_id], start_time, end_time)):
        if employee_id not in final_schedule:
            final_schedule[employee_id] = []
        final_schedule[employee_id].append((start_time, end_time))
        return 1  # Successfully scheduled
    else:
        return 0  # Unable to schedule

def is_overlapping(existing_schedule, start_time, end_time):
    """
    Check if a new shift overlaps with existing shifts.

    Parameters:
        - existing_schedule (list): List of existing shifts.
        - start_time (int): Start time of the new shift.
        - end_time (int): End time of the new shift.

    Returns:
        bool: True if overlapping, False otherwise.
    """
    for shift_start, shift_end in existing_schedule:
        if not (end_time <= shift_start or start_time >= shift_end):
            return True  # Overlapping shift found
    return False

def generate_final_schedule(sorted_shifts, required_roles, hours_worked, final_schedule, employees, role_availability, day):
    """
    Generate the final schedule for all roles.

    Parameters:
        - sorted_shifts (list): List of sorted shifts.
        - required_roles (dict): Dictionary of required roles and number of employees.
        - hours_worked (dict): Dictionary of hours worked by employees.
        - final_schedule (dict): Dictionary of the final schedule.
        - employees (dict): Dictionary of Employee objects.
        - role_availability (dict): Dictionary of role availabilities.
        - day (str): Day of the week.

    Returns:
        int: Total number of roles scheduled.
    """
    role_count = 0

    for required_role, required_employees in required_roles.items():
        role_shifts = [shift for shift in sorted_shifts if shift[3] == required_role]
        role_count += generate_final_schedule_for_role(role_shifts, required_role, required_employees, hours_worked, final_schedule, employees, role_availability, day)

    ic(f"Role: {required_role}, Scheduled: {role_count}")

    return role_count

def generate_final_schedule_for_role(sorted_shifts, required_role, required_employees, hours_worked, final_schedule, employees, role_availability, day):
    """
    Generate the final schedule for a specific role.

    Parameters:
        - sorted_shifts (list): List of sorted shifts.
        - required_role (str): The required role for the shift.
        - required_employees (int): Number of employees required for the role.
        - hours_worked (dict): Dictionary of hours worked by employees.
        - final_schedule (dict): Dictionary of the final schedule.
        - employees (dict): Dictionary of Employee objects.
        - role_availability (dict): Dictionary of role availabilities.
        - day (str): Day of the week.

    Returns:
        int: Total number of shifts scheduled for the role.
    """
    role_count = 0

    for shift in sorted_shifts:
        if role_count == required_employees:
            break

        scheduled = schedule_employee(shift, required_role, hours_worked, final_schedule, role_availability, day)
        role_count += scheduled

    return role_count

def generate_weekly_schedule(employees, role_availability, day):
    """
    Generate a weekly schedule for employees.

    Parameters:
        - employees (dict): Dictionary of Employee objects.
        - role_availability (dict): Dictionary of role availabilities.
        - day (str): Day of the week.

    Returns:
        list: List of weekly schedule shifts.
    """
    weekly_schedule = []

    for employee_id, employee in employees.items():
        ic(f"Checking availability for Employee {employee_id} ({employee.role}):")
        for shift in employee.shifts:
            if shift[2] == day and check_availability(employee, shift, role_availability):
                ic(f"  - Employee {employee_id} is available on {shift[2]} from {shift[0]} to {shift[1]}.")
                weekly_schedule.append((employee_id, shift[0], shift[1], employee.role))
            else:
                ic(f"  - Employee {employee_id} is NOT available on {shift[2]} from {shift[0]} to {shift[1]}.")

    return weekly_schedule

def print_final_schedule(final_schedule, employees):
    """
    Print the final schedule.

    Parameters:
        - final_schedule (dict): Dictionary of the final schedule.
        - employees (dict): Dictionary of Employee objects.
    """
    for day, shifts in final_schedule.items():
        if shifts:
            ic(f"\n{day}:")
            for shift in shifts:
                ic(f"  - Employee {shift[0]} ({employees[shift[0]].role}): {format_time(shift[1], employees[shift[0]].role)} to {format_time(shift[2], employees[shift[0]].role)}")
        else:
            ic(f"\n{day}:\n  - No shifts scheduled.")

def schedule(employees, role_availability, week_start_date):
    """
    Generate the final schedule for a week.

    Parameters:
        - employees (dict): Dictionary of Employee objects.
        - role_availability (dict): Dictionary of role availabilities.
        - week_start_date (datetime): The start date of the week.

    Returns:
        dict: The final schedule for the week.
    """
    required_roles = {
        "Opener": 1,
        "Open Support": 1,
        "Rush Support": 2,
        "Close Support": 1,
        "Closer": 2,
        "Shift Lead": 1,
    }

    final_schedule = defaultdict(list)
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    hours_worked = defaultdict(float)

    for day in days_of_week:
        final_schedule[day] = []

        weekly_schedule = generate_weekly_schedule(employees, role_availability, day)

        sorted_shifts = sorted(weekly_schedule, key=lambda x: (x[1], x[2]))

        for required_role, required_employees in required_roles.items():
            role_count = generate_final_schedule(sorted_shifts, required_roles, hours_worked, final_schedule, employees, role_availability, day)

    print_final_schedule(final_schedule, employees)

    return final_schedule

def format_time(time, role):
    """
    Format the time for display.

    Parameters:
        - time (int): Time in HHMM format.
        - role (str): Role of the employee.

    Returns:
        str: Formatted time string.
    """
    if role in role_availability:
        return f"{time:04d}"[:2] + ":" + f"{time:04d}"[2:]
    else:
        return "Default Availability"

def calculate_weighted_labor_cost_percentage(total_labor_cost, total_revenue, performance_rating):
    """
    Calculate the weighted labor cost percentage.

    Parameters:
        - total_labor_cost (float): Total amount spent on employee payroll.
        - total_revenue (float): Total revenue generated by the business.
        - performance_rating (float): Performance rating for the business (e.g., between 1 and 5).

    Returns:
        float: Weighted labor cost percentage.
    """
    if total_revenue == 0:
        return 0  # Avoid division by zero

    labor_cost_percentage = (total_labor_cost / total_revenue) * 100  # Calculate labor cost percentage
    weighted_labor_cost_percentage = labor_cost_percentage * (performance_rating / 5.0)  # Weight the percentage by performance rating

    return weighted_labor_cost_percentage

def calculate_and_print_weighted_labor_cost_percentage(total_labor_cost, total_revenue, performance_rating):
    """
    Calculate and print the weighted labor cost percentage.

    Parameters:
        - total_labor_cost (float): Total amount spent on employee payroll.
        - total_revenue (float): Total revenue generated by the business.
        - performance_rating (float): Performance rating for the business (e.g., between 1 and 5).
    """
    weighted_labor_cost_percentage = calculate_weighted_labor_cost_percentage(total_labor_cost, total_revenue, performance_rating)  # Calculate the weighted labor cost percentage
    print(f"Weighted Labor Cost Percentage: {weighted_labor_cost_percentage:.2f}%")  # Print the result

if __name__ == "__main__":
    # Generate random employee data
    num_employees = 14  # Number of employees to generate
    employees_data = generate_random_employee_data(num_employees)  # Generate random employee data

    # Generate employee objects
    employees_objects = generate_random_employee_objects(employees_data)  # Generate employee objects from data

    # Print employee information
    for employee_id, employee in employees_objects.items():  # Iterate through employee objects
        ic(f"Employee ID: {employee_id}")
        ic(f"Name: {employee.name}")
        ic(f"Role: {employee.role}")
        ic(f"Shifts: {employee.shifts}")
        ic(f"Rating: {employee.rating}")
        ic(f"Trained: {employee.trained}")
        ic(f"Current Task: {employee.current_task}")
        ic(f"Activities Log: {employee.activities_log}")
        ic("\n")

    # Schedule shifts for a specific week (e.g., week starting from '2024-01-29')
    week_start_date = datetime.strptime('2024-01-29', '%Y-%m-%d')  # Define the start date of the week
    final_schedule = schedule(employees_objects, role_availability, week_start_date)  # Generate the final schedule
