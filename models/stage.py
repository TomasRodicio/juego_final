import pygame
from models.player import Player
from models.enemy import Enemy
from models.platform import Tile
from models.coins import Coins
from models.traps import Traps
from models.apple import Apple
from auxiliar.constantes import *

class Stage:
    def __init__(self, screen: pygame.surface.Surface, limit_w, limit_h, stage_name: str):
        # Jugador
        self.__configs = open_configs().get(stage_name)
        self.__enemies_configs = self.__configs.get('enemies')
        self.__stage_configs = self.__configs.get('stage_settings')
        self.__stage_map = self.__stage_configs['stage_map']
        self.player_sprite = Player(limit_w, limit_h, self.__configs)
        self.player = pygame.sprite.GroupSingle(self.player_sprite)
        self.__main_screen = screen
        self.__number_enemies = self.__enemies_configs['number_enemies']
        self.__coords_enemies = self.__enemies_configs['coords_enemies']
        self.__limit_w = limit_w
        self.__limit_h = limit_h
        self.__main_screen = screen
        self.__score = 0
        self.player_platform_hit_list = []
        self.enemies = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()
        self.apples = pygame.sprite.Group()
        self.__time_left = self.__stage_configs['time_seconds']
        self.__seconds_left = 500
        self.__minutes_left = 500
        self.__actual_time = pygame.time.get_ticks()
        self.__time_display = ""
        self.__win = False
        self.__lose = False
        self.__stage_name = stage_name
        self.collect_apple_sound = pygame.mixer.Sound("assets/sounds/effects/Fruit collect 1.wav")
        pygame.mixer.Sound.set_volume(self.collect_apple_sound, 0.2)
        self.collect_coin_sound = pygame.mixer.Sound("assets/sounds/effects/coin-collect-retro-8-bit-sound-effect-145251.mp3")
        pygame.mixer.Sound.set_volume(self.collect_coin_sound, 0.2)

        self.spawn_enemies()
        self.create_stage(self.__stage_map)
        self.set_fonts()


    @property
    def stage_name(self):
        return self.__stage_name
    
    @stage_name.setter
    def stage_name(self, name):
        self.__stage_name = name

    @property
    def score(self):
        return self.__score



    def spawn_enemies(self):
        if self.__number_enemies > len(self.__coords_enemies):
            for coord in self.__coords_enemies:
                self.enemy_sprite = Enemy((coord.get('coord_x'), coord.get('coord_y')), self.__limit_w, self.__limit_h, self.__configs)
                self.enemies.add(self.enemy_sprite)

        elif self.__number_enemies <= len(self.__coords_enemies):
            for coord in range(self.__number_enemies):
                self.enemy_sprite = Enemy((self.__coords_enemies[coord].get('coord_x'), self.__coords_enemies[coord].get('coord_y')), self.__limit_w, self.__limit_h, self.__configs)
                self.enemies.add(self.enemy_sprite)


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
                    case "0":
                        tile_sprite = Tile((x,y), tile_size, 'assets/img/platforms/left_grass.png')
                        self.tiles.add(tile_sprite)
                    case "1":
                        tile_sprite = Tile((x,y), tile_size, 'assets/img/platforms/right_grass.png')
                        self.tiles.add(tile_sprite)
                    case "B":
                        tile_sprite = Tile((x,y), tile_size, 'assets/img/platforms/bottom_grass.png')
                        self.tiles.add(tile_sprite)
                    case "C":
                        coin_sprite  = Coins((x,y), tile_size, self.__configs)
                        self.coins.add(coin_sprite)
                    case "T":
                        trap_sprite = Traps((x,y), tile_size, self.__configs)
                        self.traps.add(trap_sprite)
                    case "A":
                        apple_sprite = Apple((x,y), tile_size, self.__configs)
                        self.apples.add(apple_sprite)


    def set_fonts(self):
        self.__text_font = pygame.font.Font('./assets/fonts/8bitOperatorPlus8-Bold.ttf', 30)


    def render_text(self):
        score_text = self.__text_font.render(f"Score: {self.__score}", True, 'white')
        time_text = self.__text_font.render(f"Time: {self.__time_display}", True, 'white')
        life_text = self.__text_font.render(f"Life: {self.player.sprite.get_life}", True, 'red')

        self.__main_screen.blit(life_text, (10,10))
        self.__main_screen.blit(score_text, (10, time_text.get_height() + 20))
        self.__main_screen.blit(time_text, (screen_w - time_text.get_width(), 10))



    def player_hit_enemy(self):
        enemies_hit = pygame.sprite.groupcollide(self.player.sprite.get_bullets, self.enemies, True, False)
        for enemy in enemies_hit:
            enemy_hit = enemies_hit[enemy][0]
            enemy_hit.hit(self.player.sprite.get_damage)
            if enemy_hit.get_life == 0:
                self.__score += enemy_hit.get_score


    def enemy_hit_player(self):
        for enemy in self.enemies:
            if pygame.sprite.spritecollide(self.player.sprite, enemy.get_bullet_group, True):
                self.player.sprite.hit(enemy.get_damage)



    def enemy_attack(self):
        for enemy in self.enemies:
            if enemy.rect_vision_right.colliderect(self.player.sprite.rect) and enemy.get_is_looking_right and enemy.get_ready:
                enemy.shoot_arrow()
                enemy.set_ready = False
                enemy.set_bullet_time = pygame.time.get_ticks()
                enemy.set_is_shooting = True
            elif enemy.rect_vision_left.colliderect(self.player.sprite.rect) and not enemy.get_is_looking_right and enemy.get_ready:
                enemy.shoot_arrow()
                enemy.set_ready = False
                enemy.set_bullet_time = pygame.time.get_ticks()
                enemy.set_is_shooting = True
            elif enemy.get_ready:
                enemy.set_is_shooting = False


    def bullet_collition_platforms(self):
        pygame.sprite.groupcollide(self.player.sprite.get_bullets, self.tiles, True, False)
        for enemy in self.enemies:
            pygame.sprite.groupcollide(enemy.get_bullet_group, self.tiles, True, False)


    def player_collition_items(self):
        self.collect_coin = pygame.sprite.spritecollide(self.player_sprite, self.coins, False)
        self.collect_apple = pygame.sprite.spritecollide(self.player_sprite, self.apples, False)
        for coin in self.coins:
            if coin in self.collect_coin:
                self.__score += coin.value
                pygame.mixer.Sound.play(self.collect_coin_sound)
                coin.kill()
        for apple in self.apples:
            if apple in self.collect_apple:
                self.player.sprite.heal(apple.heal)
                pygame.mixer.Sound.play(self.collect_apple_sound)
                apple.kill()
        


    def player_collition_traps(self):
        self.trap_hit = pygame.sprite.spritecollide(self.player_sprite, self.traps, False)
        for trap in self.traps:
            if trap in self.trap_hit:
                self.player.sprite.hit(trap.damage)
    





    def movement_collitions(self):
        self.player_platform_hit_list = pygame.sprite.spritecollide(self.player_sprite, self.tiles, False)
        self.enemy_platform_hit_list = pygame.sprite.groupcollide(self.enemies, self.tiles, False, False)
        for tile in self.tiles:
            if self.player.sprite.rect_ceiling_collition.colliderect(tile.rect_ceiling_collition):
                self.player.sprite.on_ceiling = True
            else:
                self.player.sprite.on_ceiling = False
            if self.player.sprite.rect_left_collition.colliderect(tile.rect_right_collition):
                self.player.sprite.on_wall_left = True
            else:
                self.player.sprite.on_wall_left = False
            if self.player.sprite.rect_right_collition.colliderect(tile.rect_left_collition):
                self.player.sprite.on_wall_right = True
            else:
                self.player.sprite.on_wall_right = False
            for enemy in self.enemies:
                
                if (enemy.get_is_looking_right and enemy.rect_right_collition.colliderect(tile.rect_left_collition)) or (not enemy.get_is_looking_right and enemy.rect_left_collition.colliderect(tile.rect_right_collition)):
                    enemy.turn_around = True
                else:
                    enemy.turn_around = False
                


    def update_time(self):
        if self.__time_left >= 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.__actual_time >= 1000:
                self.__minutes_left, self.__seconds_left = divmod(self.__time_left, 60)
                self.__time_display = f"{self.__minutes_left:02.0f}:{self.__seconds_left:02.0f}"
                self.__actual_time = current_time
                self.__time_left -= 1


    def check_win(self) -> bool:
        match self.__stage_name:
            case 'stage_1' | 'stage_2' | 'stage_3':
                self.__win = len(self.enemies) == 0\
                and self.__minutes_left >= 0 and self.__seconds_left >= 0

    
    def check_lose(self):
        match self.__stage_name:
            case 'stage_1' | 'stage_2' | 'stage_3':
                self.__lose = self.player.sprite.get_life <= 0\
                or self.__minutes_left == 0 and self.__seconds_left == 0

    
    def stage_passed(self):
        return self.__win
    
    def stage_loss(self):
        return self.__lose



    def run(self, delta_ms):
        self.update_time()
        self.tiles.update(self.__main_screen)
        self.movement_collitions()
        self.enemy_attack()
        self.player_collition_items()
        self.player.update(delta_ms, self.__main_screen, self.player_platform_hit_list)
        self.enemies.update(delta_ms, self.__main_screen, self.enemy_platform_hit_list)
        self.coins.update(delta_ms, self.__main_screen)
        self.traps.update(delta_ms, self.__main_screen)
        self.apples.update(delta_ms, self.__main_screen)
        self.player_hit_enemy()
        self.enemy_attack()
        self.enemy_hit_player()
        self.bullet_collition_platforms()
        self.player_collition_traps()
        self.render_text()
        self.check_win()
        self.check_lose()


