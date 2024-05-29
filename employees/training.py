import random
import pygame
from pygame.locals import *
from icecream import ic
from employees.skills import Skill

class TrainingProgram:
    def __init__(self, name, required_level, challenge, questions):
        self.name = name
        self.required_level = required_level
        self.challenge = challenge
        self.questions = questions

    def __repr__(self):
        return f"TrainingProgram(name={self.name}, required_level={self.required_level}, challenge={self.challenge}, questions={len(self.questions)})"

def train_employee(employee, training_program, screen):
    ic(f"Attempting to train {employee.name} in {training_program.name}")

    current_level = employee.get_skill_level(training_program.name)
    if current_level < training_program.required_level:
        ic(f"{employee.name} does not meet the required level for {training_program.name}. Current level: {current_level}")
        return

    ic(f"Starting training for {employee.name} in {training_program.name}.")
    employee.training.append(training_program)
    challenge_result = conduct_challenge(training_program.challenge, training_program.questions, screen)

    if challenge_result:
        complete_training(employee, training_program)
    else:
        ic(f"{employee.name} failed the training challenge for {training_program.name}.")

def complete_training(employee, training_program):
    ic(f"Training completed for {employee.name} in {training_program.name}.")
    current_level = employee.get_skill_level(training_program.name)
    employee.add_skill(Skill(training_program.name, current_level + 1))
    employee.training.remove(training_program)

def conduct_challenge(challenge, questions, screen):
    ic(f"Conducting challenge: {challenge}")
    if challenge == "quiz":
        return quiz_challenge(questions, screen)
    return False

def quiz_challenge(questions, screen):
    question, options, correct_answer = random.choice(questions)
    return display_quiz_popup(screen, question, options, correct_answer)

def display_quiz_popup(screen, question, options, correct_answer):
    font = pygame.font.Font(None, 36)
    screen.fill((255, 255, 255))

    # Display the question
    question_text = font.render(question, True, (0, 0, 0))
    screen.blit(question_text, (50, 50))

    # Define colors for the options
    colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]  # Red, Blue, Green, Yellow
    option_buttons = []
    for i, option in enumerate(options):
        button_rect = pygame.Rect(50, 150 + i * 50, 200, 40)
        pygame.draw.rect(screen, colors[i], button_rect)
        option_text = font.render(option, True, (255, 255, 255))
        screen.blit(option_text, (60, 160 + i * 50))
        option_buttons.append((button_rect, option))

    # Initialize the countdown bar
    countdown_start_time = pygame.time.get_ticks()
    countdown_duration = 10000  # 10 seconds

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            elif event.type == MOUSEBUTTONDOWN:
                for button_rect, option in option_buttons:
                    if button_rect.collidepoint(event.pos):
                        ic(f"Selected option: {option}")
                        return option == correct_answer

        # Update the countdown bar
        elapsed_time = pygame.time.get_ticks() - countdown_start_time
        countdown_width = max(0, 500 * (1 - elapsed_time / countdown_duration))

        # Draw the countdown bar
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(50, 350, 500, 30))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(50, 350, countdown_width, 30))

        pygame.display.flip()

        if elapsed_time >= countdown_duration:
            ic("Time's up!")
            return False
