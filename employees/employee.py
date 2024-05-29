import datetime
import random
from icecream import ic


class Employee:
    def __init__(self, name, employee_id, role=None, shifts=None, rating=None):
        self.name = name
        self.employee_id = employee_id
        self.role = role if role else "Default"
        self.shifts = shifts or []
        self.rating = rating or round(random.uniform(3.0, 5.0), 1)
        self.trained = False
        self.current_task = None
        self.activities_log = []

    def perform_task(self, task, duration_minutes):
        if not self.trained:
            ic(f'Employee {self.employee_id} ({self.role}) cannot perform tasks without training.')
        else:
            ic(f'Employee {self.employee_id} ({self.role}) is performing {task}.')
            self.current_task = task
            self.log_activity(task, duration_minutes)

    def log_activity(self, task, duration_minutes):
        current_time = datetime.now()
        end_time = current_time + datetime.timedelta(minutes=duration_minutes)
        self.activities_log.append({'task': task, 'start_time': current_time, 'end_time': end_time})

    def work_shift(self, payroll):
        current_time = datetime.now()
        current_shift = next((shift for shift in self.shifts if shift['start'] <= current_time.time() <= shift['end']), None)

        if not current_shift:
            ic(f'Employee {self.employee_id} ({self.role}) is not scheduled for a shift at the moment.')
            return

        shift_start_time = datetime.combine(current_time.date(), current_shift['start'])
        shift_end_time = datetime.combine(current_time.date(), current_shift['end'])

        while current_time.time() <= current_shift['end']:
            if current_time.time() == datetime.strptime('09:30', '%H:%M').time():
                self.perform_task('Prepare ingredients', duration_minutes=10)
            elif current_time.time() == datetime.strptime('10:30', '%H:%M').time():
                self.perform_task('Assemble sandwiches', duration_minutes=15)
            elif current_time.time() == datetime.strptime('12:00', '%H:%M').time():
                self.perform_task('Lunch break', duration_minutes=30)
            elif current_time.time() == datetime.strptime('15:30', '%H:%M').time():
                self.perform_task('Clean and restock', duration_minutes=20)
            current_time += datetime.timedelta(minutes=1)

        shift_duration = log_shift_hours(self, shift_start_time, shift_end_time)
        payroll.log_hours(self.employee_id, shift_duration)
        ic(f'Employee {self.employee_id} ({self.role}) has completed the {current_shift["shift_name"]} shift.')

def log_shift_hours(employee, start_time, end_time):
    shift_duration = (end_time - start_time).seconds / 3600
    return shift_duration
