import pygame 
import sys
from auxiliar.constantes import *
from models.stage import Stage
from models.button import Button
from models.textbox import TextBox
from models.menu import Menu
import sqlite3

class Game:
    
    def __init__(self) -> None:

        pygame.init()
        self.__screen = pygame.display.set_mode((screen_w, screen_h))
        self.clock = pygame.time.Clock()
        self.__font = pygame.font.Font('./assets/fonts/8bitOperatorPlus8-Bold.ttf', 30)
        self.volumen = 0.2


        pygame.mixer.init()
        pygame.mixer.music.load("assets/sounds/ost/sonatina_letsadventure_5InLoneliness.wav")
        pygame.mixer.music.set_volume(self.volumen)
        pygame.mixer.music.play(-1)
        self.flag_mute = True


    def main_menu(self):
        self.__screen.fill((0, 0, 0))
        self.menu = Menu(self.__screen, self.__font)
        self.menu.add_button((screen_w / 2, 200), 'START', 'white', self.button_play_click, "", (110,30))
        self.menu.add_button((screen_w / 2 - 20, 300), 'OPTIONS', 'white', self.button_option_click, "", (150, 30))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            
                self.menu.update(event)
                self.menu.draw()
            
                pygame.display.flip()

    def select_level_menu(self):
        self.__screen.fill((0, 0, 0))
        self.menu = Menu(self.__screen, self.__font)
        self.menu.add_button((screen_w / 2, 200), 'LEVEL 1', 'white', self.button_level_1, "", (130,30))
        self.menu.add_button((screen_w / 2, 300), 'LEVEL 2', 'white', self.button_level_2, "", (130,30))
        self.menu.add_button((screen_w / 2, 400), 'LEVEL 3', 'white', self.button_level_3, "", (130,30))
        self.menu.add_button((screen_w / 2, 500), 'BACK', 'white', self.button_back, "", (130,30))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                self.menu.update(event)
                self.menu.draw()

                pygame.display.flip()

    def options_menu(self):
        self.__screen.fill((0, 0, 0))
        self.menu = Menu(self.__screen, self.__font)
        self.menu.add_button((screen_w / 2, 200), 'MUTE', 'white', self.button_mute, "", (130,30))
        self.menu.add_button((screen_w / 2, 300), 'BACK', 'white', self.button_back, "", (130,30))
        
    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                self.menu.update(event)
                self.menu.draw()

                pygame.display.flip()


    def submit_score(self):
        self.__screen.fill((0, 0, 0))
        self.menu = Menu(self.__screen, self.__font)
        self.menu.add_textbox((screen_w / 2, 200), (200, 30), 'black')
        self.menu.add_button((screen_w / 2 + 200, 200), 'SUBMIT', 'white', self.submit_score_buttom, "", (130,30))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                self.menu.update(event)
                self.menu.draw()

                pygame.display.flip()
    
    
    def submit_score_buttom(self):
        return True

    def button_play_click(self, param):
        self.select_level_menu()
        print("hola")
    
    def button_level_1(self, param):
        self.run_stage("stage_1")
    
    def button_level_2(self, param):
        self.run_stage("stage_2")

    def button_level_3(self, param):
        self.run_stage("stage_3")
    
    def button_mute(self, param):
        if self.flag_mute:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        self.flag_mute = not self.flag_mute
    
    def button_back(self, param):
        self.main_menu()


    def button_option_click(self, param):
        self.options_menu()
    



    def run_stage(self, stage_name: str):
    
        screen = pygame.display.set_mode((screen_w, screen_h))
        clock = pygame.time.Clock()
        game = Stage(screen, screen_w, screen_h, stage_name)

        back_img = pygame.image.load('./assets/img/background/background.png')
        back_img = pygame.transform.scale(back_img, (screen_w, screen_h))
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            if game.stage_name == "stage_1" and game.stage_passed():
                game.stage_name = "stage_2"
                self.run_stage(game.stage_name)
            if game.stage_name == "stage_2" and game.stage_passed():
                game.stage_name = "stage_3"
                self.run_stage(game.stage_name)
            if game.stage_name == "stage_3" and game.stage_passed():
                print("Win!")
                self.main_menu()
            if game.stage_loss():
                self.main_menu()
        

            

            screen.blit(back_img, back_img.get_rect())
            delta_ms = clock.tick(60)
            game.run(delta_ms)
            pygame.display.flip()