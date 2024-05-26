from employees.skills import Skill


def train_employee(employee, skill):
    print(f"Training {employee.name} in {skill.name}")
    current_level = employee.get_skill_level(skill.name)
    employee.add_skill(Skill(skill.name, current_level + 1))
