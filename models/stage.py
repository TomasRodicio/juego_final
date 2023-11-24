import pygame
from models.player import Player
from auxiliar.constantes import open_configs

class Stage:
    def __init__(self, screen: pygame.surface.Surface, limit_w, limit_h, stage_name: str):
        # Jugador
        self.__configs = open_configs().get(stage_name)
        self.player_sprite = Player(limit_w, limit_h, self.__configs)  # posicion inicial
        self.player = pygame.sprite.GroupSingle(self.player_sprite)
        self.__main_screen = screen


    def run(self, delta_ms):
            # Actualizar todos los grupos de sprites
            # Dibujar todos los grupos de sprites

            # Actualizar y Dibujar Jugador
            self.player.update(delta_ms, self.__main_screen)
            self.player.draw(self.__main_screen)
            
            #self.enemies.draw(screen)
        
        