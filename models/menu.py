import pygame
from models.button import Button
from models.textbox import TextBox

class Menu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.buttons = []
        self.textboxs = []

    def add_button(self, pos, text, color, onclick, onclick_param, size):
        button = Button(pos, self.font, text, color, onclick, onclick_param, size)
        self.buttons.append(button)


    def add_textbox(self, pos, size, font_color):
        textbox = TextBox(pos, size, self.font, font_color)
        self.textboxs.append(textbox)


    def update(self, event):
        for button in self.buttons:
            button.update(event, self.screen)
        for textbox in self.textboxs:
            textbox.update(event, self.screen)

    def draw(self):
        for button in self.buttons:
            button.draw(self.screen)