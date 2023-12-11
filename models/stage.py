import pygame
from models.player import Player
from models.enemy import Enemy
from models.platform import Tile
from auxiliar.constantes import open_configs
from auxiliar.constantes import tile_size

class Stage:
    def __init__(self, screen: pygame.surface.Surface, limit_w, limit_h, stage_name: str):
        # Jugador
        self.__configs = open_configs().get(stage_name)
        self.__enemies_configs = self.__configs.get('enemies')
        self.__stage_map = self.__configs.get('stage_map')
        self.player_sprite = Player(limit_w, limit_h, self.__configs)
        self.player = pygame.sprite.GroupSingle(self.player_sprite)
        self.__main_screen = screen
        self.__number_enemies = self.__enemies_configs['number_enemies']
        self.__coords_enemies = self.__enemies_configs['coords_enemies']
        self.__limit_w = limit_w
        self.__limit_h = limit_h
        self.__main_screen = screen
        self.player_platform_hit_list = []
        self.enemies = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()

        self.spawn_enemies()
        self.create_stage(self.__stage_map)



    def spawn_enemies(self):
        if self.__number_enemies > len(self.__coords_enemies):
            for coord in self.__coords_enemies:
                enemy_sprite = Enemy((coord.get('coord_x'), coord.get('coord_y')), self.__limit_w, self.__limit_h, self.__configs)
                self.enemies.add(enemy_sprite)
                
        elif self.__number_enemies <= len(self.__coords_enemies):
            for coord in range(self.__number_enemies):
                enemy_sprite = Enemy((self.__coords_enemies[coord].get('coord_x'), self.__coords_enemies[coord].get('coord_y')), self.__limit_w, self.__limit_h, self.__configs)
                self.enemies.add(enemy_sprite)

    
    def create_stage(self, layeout):
        for row_index, row in enumerate(layeout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                match(cell):
                    case 'X':
                        tile_sprite = Tile((x,y), tile_size, 'assets/img/platforms/top_grass.png')
                        self.tiles.add(tile_sprite)
                    case "D":
                        tile_sprite = Tile((x,y), tile_size, 'assets/img/platforms/dirt.png')
                        self.tiles.add(tile_sprite)
            

        
        
        
        pass
    

    def player_movement_collitions(self):
        self.player_platform_hit_list = pygame.sprite.spritecollide(self.player_sprite, self.tiles, False)
        
        for enemy in self.enemies:
            self.enemy_platform_hit_list = pygame.sprite.spritecollide(self.enemy_sprite, self.tiles, False)


    def run(self, delta_ms):
            # Actualizar todos los grupos de sprites
            # Dibujar todos los grupos de sprites

            # Actualizar y Dibujar Jugador
            self.tiles.update(self.__main_screen)
            self.player_movement_collitions()
            self.player.update(delta_ms, self.__main_screen, self.player_platform_hit_list)
            self.enemies.update(delta_ms, self.__main_screen)
        
        