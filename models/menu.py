import pygame
from models.button import Button

class Menu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.buttons = []

    def add_button(self, pos, text, color, onclick, onclick_param, size):
        button = Button(pos, self.font, text, color, onclick, onclick_param, size)
        self.buttons.append(button)

    def update(self, event):
        for button in self.buttons:
            button.update(event, self.screen)

    def draw(self):
        for button in self.buttons:
            button.draw(self.screen)