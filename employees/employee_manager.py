import random
from .employee import Employee
from .skills import Skill

class EmployeeManager:
    def __init__(self):
        self.employees = []

    def generate_employee(self, name, position):
        skill_level = {skill.name: random.randint(1, 5) for skill in Skill.SKILLS}
        return Employee(name, position, skill_level)

    def hire_employee(self, name, position):
        new_employee = self.generate_employee(name, position)
        self.employees.append(new_employee)
        self.onboard_employee(new_employee)
        return new_employee

    def fire_employee(self, employee):
        self.employees.remove(employee)

    def get_employee(self, name):
        for employee in self.employees:
            if employee.name == name:
                return employee
        return None

    def onboard_employee(self, employee):
        print(f"Onboarding {employee.name} for position {employee.position}")
        # Basic onboarding processes
        basic_skills = [Skill("Customer Service", 1), Skill("Sandwich Making", 1)]
        for skill in basic_skills:
            employee.add_skill(skill)

    def train_employee(self, employee, skill):
        print(f"Training {employee.name in skill.name}")
        current_level = employee.get_skill_level(skill.name)
        employee.add_skill(Skill(skill.name, current_level + 1))
