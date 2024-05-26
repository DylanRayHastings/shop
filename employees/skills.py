class Skill:
    SKILLS = []

    def __init__(self, name, level):
        self.name = name
        self.level = level
        Skill.SKILLS.append(self)
    
# Define some example skills
customer_service = Skill("Customer Service", 0)
sandwich_making = Skill("Sandwich Making", 0)
