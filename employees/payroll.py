import random
from datetime import datetime, timedelta
from icecream import ic

class Payroll:
    def __init__(self):
        self.employee_hours = {}
        self.hourly_rates = {}

    def set_hourly_rate(self, employee_id, rate):
        self.hourly_rates[employee_id] = rate

    def log_hours(self, employee_id, hours):
        if employee_id not in self.employee_hours:
            self.employee_hours[employee_id] = 0
        self.employee_hours[employee_id] += hours

    def calculate_pay(self, employee_id):
        hours = self.employee_hours.get(employee_id, 0)
        rate = self.hourly_rates.get(employee_id, 0)
        return hours * rate

    def generate_payroll_report(self, employees):
        report = []
        for employee_id, employee in employees.items():
            pay = self.calculate_pay(employee_id)
            report.append((employee_id, employee.name, pay))
            ic(f"Payroll for {employee.name} (ID: {employee_id}): ${pay:.2f}")
        return report

def log_shift_hours(employee, start_time, end_time):
    shift_duration = (end_time - start_time).seconds / 3600
    return shift_duration
