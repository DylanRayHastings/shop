class Employee:
    def __init__(self, name, position, skill_level):
        self.name = name
        self.position = position
        self.skill_level = skill_level
        self.training = []

    def add_skill(self, skill):
        self.skill_level[skill.name] = skill.level

    def train(self, skill):
        self.training.append(skill)

    def get_skill_level(self, skill_name):
        return self.skill_level.get(skill_name, 0)
