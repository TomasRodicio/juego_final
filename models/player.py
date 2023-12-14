import pygame
import sys
from auxiliar.auxiliar import SurfaceManager as sm
from auxiliar.constantes import *
from models.bullet import Bullet

class Player(pygame.sprite.Sprite):

    def __init__(self, constraint_x, constraint_y, stage_dict_configs: dict, frame_rate = 40, speed_run = 20, gravity = 16, jump = 30):
        super().__init__()

        self.__player_configs = stage_dict_configs.get('player')
        self.__player_cords = self.__player_configs['coords_player']
        self.__players_stats = self.__player_configs['stats']
        self.__iddle_r = sm.get_surface('./assets/img/player/idle/Idle.png', 9, 1, step= 2)
        self.__iddle_l = sm.get_surface('./assets/img/player/idle/Idle.png', 9, 1, step=2, flip=True)
        self.__run_r = sm.get_surface('./assets/img/player/run/Run.png', 8, 1)
        self.__run_l = sm.get_surface('./assets/img/player/run/Run.png', 8, 1, flip=True)
        self.__jump_r = sm.get_surface('./assets/img/player/jump/Jump.png', 9, 1)
        self.__jump_l = sm.get_surface("./assets/img/player/jump/Jump.png", 9, 1, flip=True)
        self.__shoot_r = sm.get_surface("./assets/img/player/attack/Shoot.png", 14, 1)
        self.__shoot_l = sm.get_surface("./assets/img/player/attack/Shoot.png", 14, 1, flip=True)
        self.__dead_r = sm.get_surface("./assets/img/player/dead/Dead.png", 5, 1)
        self.__dead_l = sm.get_surface("./assets/img/player/dead/Dead.png", 5, 1, flip=True)
        self.hit_sound = pygame.mixer.Sound("assets/sounds/effects/Hit damage 1.wav")
        pygame.mixer.Sound.set_volume(self.hit_sound, 0.2)
        self.shoot_sound = pygame.mixer.Sound("assets/sounds/effects/fire_bow_sound-mike-koenig.wav")
        pygame.mixer.Sound.set_volume(self.shoot_sound, 0.2)
        self.__move_x = 0
        self.__move_y = 0
        self.__speed_run = speed_run
        self.__jump = jump
        self.__max_constraint_x = constraint_x
        self.__max_constraint_y = constraint_y
        self.__frame_rate = frame_rate
        self.__player_move_time = 0
        self.__player_animation_time = 0
        self.__gravity = gravity
        self.__initial_frame = 0
        self.__actual_animation = self.__iddle_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.image = self.__actual_img_animation
        self.rect = self.image.get_rect()
        self.rect.x = self.__player_cords['coord_x']
        self.rect.y = self.__player_cords['coord_y']
        self.__is_looking_right = True
        self.__is_jumping = False
        self.__is_falling = False
        self.__on_ground = True
        self.__on_ceiling = False
        self.__on_wall_right = False
        self.__on_wall_left = False
        self.__is_alive = True

        self.__ready = True
        self.__bullet_time = 0
        self.__bullet_cooldown = 850
        self.__bullet_group = pygame.sprite.Group()

        self.__life = self.__players_stats['life']
        self.__damage = self.__players_stats['damage']

        self.rect_ground_collition = pygame.Rect(self.rect.x + self.rect.w / 4, self.rect.y + self.rect.h - 10, self.rect.w / 2, 10)
        self.rect_ceiling_collition = pygame.Rect(self.rect.x + self.rect.w / 4, self.rect.y + self.rect.h / 2 - 10, self.rect.w / 2, 10)
        self.rect_right_collition = pygame.Rect(self.rect.x + self.rect.w / 2 + 10, self.rect.y + self.rect.h / 2, 10, self.rect.h / 2)
        self.rect_left_collition = pygame.Rect(self.rect.x + self.rect.w / 2 - 30, self.rect.y + self.rect.h / 2, 10, self.rect.h / 2)

    
    @property
    def get_life(self) -> int:
        return self.__life


    @property
    def get_damage(self):
        return self.__damage
    
    
    @property
    def get_bullets(self) -> list[Bullet]:
        return self.__bullet_group


    @property
    def on_ceiling(self):
        return self.__on_ceiling
    

    @on_ceiling.setter
    def on_ceiling(self, status):
        self.__on_ceiling = status

    
    @property
    def on_wall_right(self):
        return self.__on_wall_right
    

    @on_wall_right.setter
    def on_wall_right(self, status):
        self.__on_wall_right = status
    

    @property
    def on_wall_left(self):
        return self.__on_wall_left
    

    @on_wall_left.setter
    def on_wall_left(self, status):
        self.__on_wall_left = status



    def __set_x_animations_preset(self, move_x, animation_list: list[pygame.surface.Surface], look_r: bool):
        self.__move_x = move_x
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r


    def __set_y_animations_preset(self):
        self.__move_y = -self.__jump
        # self.__move_x = self.__speed_run if self.__is_looking_right else -self.__speed_run
        self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
        self.__initial_frame = 0
        self.__is_jumping = True
        

    def eventos_teclado(self):
        keys = pygame.key.get_pressed()
        if self.__is_alive:
            if keys[pygame.K_d]:
                self.run('Right')
            if keys[pygame.K_a]:
                self.run('Left')
            if not keys[pygame.K_d] and not keys[pygame.K_a] and not keys[pygame.K_SPACE] and not keys[pygame.K_j]:
                self.stay()
            if keys[pygame.K_j] and self.__ready:
                self.shoot_arrow()
                pygame.mixer.Sound.play(self.shoot_sound)
                self.__ready = False
                self.__bullet_time = pygame.time.get_ticks()
            if keys[pygame.K_SPACE]:
                self.jump()
        

    def run(self, direction: str):
        match direction:
            case 'Right':
                look_right = True
                self.__set_x_animations_preset(self.__speed_run, self.__run_r, look_r=look_right)
            case 'Left':
                look_right = False
                self.__set_x_animations_preset(-self.__speed_run, self.__run_l, look_r=look_right)
    

    def stay(self):
       if self.__actual_animation not in (self.__iddle_l, self.__iddle_r):
            self.change_animation(self.__iddle_r) if self.__is_looking_right else  self.change_animation(self.__iddle_l)
            self.__move_x = 0
            self.__move_y = 0
    

    
    def jump(self):
        if not self.__is_jumping and not self.__is_falling:
            self.__set_y_animations_preset() 
    
    


    def shoot_arrow(self):
        self.__bullet_group.add(self.create_arrow())
        if self.__actual_animation not in (self.__shoot_l, self.__shoot_r):
            self.change_animation(self.__shoot_r if self.__is_looking_right else self.__shoot_l)
        
        


    def create_arrow(self):
        if self.__is_looking_right:
            return Bullet(self.rect.right, self.rect.centery + 10, "right", "assets/img/player/bullet/Arrow.png")
        else:
            return Bullet(self.rect.left, self.rect.centery + 10, "left", "assets/img/player/bullet/Arrow.png")
        

    def recharge(self):
        if not self.__ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.__bullet_time >= self.__bullet_cooldown:
                self.__ready = True


    def hit(self, damage):
        if self.__life > 0:
            self.__life -= damage
            pygame.mixer.Sound.play(self.hit_sound)

    def heal(self, value):
        self.__life += value

    
    def __set_borders_limits_x(self):
        pixels_move = 0
        if self.__move_x > 0:
            pixels_move = self.__move_x if self.rect.x < self.__max_constraint_x - self.__actual_img_animation.get_width() else 0
        elif self.__move_x < 0:
            pixels_move = self.__move_x if self.rect.x > 0 else 0
        return pixels_move
    

    def __set_borders_limits_y(self):
        pixels_move = 0
        if self.__move_y > 0:
            pixels_move = self.__move_y if self.rect.y < self.__max_constraint_y - self.__actual_img_animation.get_height() else 0
        elif self.__move_y < 0:
            pixels_move = self.__move_y if self.rect.y > 0 else 0
        return pixels_move
    


    def do_movement(self, delta_ms, plataformas):
        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate:
            self.__player_move_time = 0
            self.add_x(self.__set_borders_limits_x())
            self.add_y(self.__set_borders_limits_y())
            # Parte relacionado a saltar
            if not self.is_on_ground(plataformas):
                self.add_y(self.__gravity)
                self.__is_falling = True
            elif not self.on_ceiling:
                self.add_y(self.__move_y)
                self.__is_falling = False

            
    

    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            elif self.__is_alive:
                self.__initial_frame = 0
                if self.__is_jumping:
                    self.__is_jumping = False
                    self.__move_y = 0

    def add_x(self, delta_x):
        if not self.__on_wall_right:
            self.rect.x += delta_x
            self.rect_ground_collition.x += delta_x
            self.rect_ceiling_collition.x += delta_x
            self.rect_right_collition.x += delta_x
            self.rect_left_collition.x += delta_x

    
    def add_y(self, delta_y):
        self.rect.y += delta_y
        self.rect_ground_collition.y += delta_y
        self.rect_ceiling_collition.y += delta_y
        self.rect_right_collition.y += delta_y
        self.rect_left_collition.y += delta_y

    
    def change_animation(self, nueva_animacion: list[pygame.surface.Surface]):
        self.__actual_animation = nueva_animacion
        if self.__initial_frame > 0:
            self.__initial_frame = 0
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
    

    def is_on_ground(self, plataformas):
        retorno = False
        for plataforma in plataformas:
            if self.rect_ground_collition.colliderect(plataforma.rect_ground_collition):
                retorno = True
                break
        return retorno
    

    def dead(self):
        if self.__life <= 0:
            if self.__actual_animation not in (self.__dead_l, self.__dead_r):
                self.change_animation(self.__dead_r) if self.__is_looking_right else  self.change_animation(self.__dead_l)
                self.__is_alive = False
                self.__move_x = 0
                print("Perdiste")

        


    def constraint(self):  # Ajusta al jugador a los limites de la pantalla
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.__max_constraint_x:
            self.rect.right = self.__max_constraint_x
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.__max_constraint_y:
            self.rect.bottom = self.__max_constraint_y
    
    def update(self, delta_ms, screen: pygame.surface.Surface, plataformas):
        self.do_animation(delta_ms)
        self.do_movement(delta_ms, plataformas)
        self.draw(screen)
        self.eventos_teclado()
        self.constraint()
        self.recharge()
        self.dead()
        self.__bullet_group.draw(screen)
        self.__bullet_group.update(screen)


    def draw(self, screen: pygame.surface.Surface):
        if DEBUG:
            # pygame.draw.rect(screen, 'red', self.rect)
            pygame.draw.rect(screen, 'blue', self.rect_ground_collition)
            pygame.draw.rect(screen, 'blue', self.rect_ceiling_collition)
            pygame.draw.rect(screen, 'blue', self.rect_right_collition)
            pygame.draw.rect(screen, 'blue', self.rect_left_collition)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation, self.rect)
        
