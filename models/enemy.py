import pygame
from auxiliar.auxiliar import SurfaceManager as sm
from auxiliar.constantes import *
from models.bullet import Bullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, constraint_x, constraint_y, stage_dict_configs: dict, frame_rate = 40, speed_walk = 3, gravity = 16) -> None:
        super().__init__()
        self.__enemies_configs = stage_dict_configs.get('enemies')
        self.__enemies_stats  = self.__enemies_configs['stats']
        self.__walk_r = sm.get_surface("./assets/img/enemy/walk/Walk.png", 8, 1)
        self.__walk_l = sm.get_surface("./assets/img/enemy/walk/Walk.png", 8, 1, flip=True)
        self.__attack_r = sm.get_surface("./assets/img/enemy/attack/Shot_1.png", 15, 1)
        self.__attack_l = sm.get_surface("./assets/img/enemy/attack/Shot_1.png", 15, 1, flip=True)
        self.__dead_r = sm.get_surface("./assets/img/enemy/dead/Dead.png", 5, 1)
        self.__dead_l = sm.get_surface("./assets/img/enemy/dead/Dead.png", 5, 1, flip=True)
        self.__move_x = 0
        self.__move_y = 0
        self.__score = self.__enemies_configs['enemies_score']
        self.__speed_walk = speed_walk
        self.__frame_rate = frame_rate
        self.__time_move = 0
        self.__enemy_animation_time = 0
        self.__gravity = gravity
        self.__initial_frame = 0
        self.__actual_animation = self.__walk_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.image = self.__actual_img_animation
        self.rect = self.image.get_rect(midbottom=pos)
        self.__is_looking_right = True
        self.__is_shooting = False
        self.__max_constraint_x = constraint_x
        self.__max_constraint_y = constraint_y
        self.turn_around = False
        self.__ready = True
        self.__bullet_time = 0
        self.__bullet_cooldown = 850
        self.__bullet_group = pygame.sprite.Group()

        self.__life = self.__enemies_stats['life']
        self.__damage = self.__enemies_stats['damage']

        self.rect_ground_collition = pygame.Rect(self.rect.x + self.rect.w / 4, self.rect.y + self.rect.h - 10, self.rect.w / 2, 10)
        self.rect_vision_right = pygame.Rect(self.rect.x + self.rect.w / 2, self.rect.y + self.rect.h / 2, enemy_range, 10)
        self.rect_vision_left = pygame.Rect(self.rect.x + self.rect.w / 2 - enemy_range, self.rect.y + self.rect.h / 2, enemy_range, 10)
        self.rect_right_collition = pygame.Rect(self.rect.x + self.rect.w / 2 + 10, self.rect.y + self.rect.h / 2, 10, self.rect.h / 2 - 10)
        self.rect_left_collition = pygame.Rect(self.rect.x + self.rect.w / 2 - 30, self.rect.y + self.rect.h / 2, 10, self.rect.h / 2 - 10)


    @property
    def get_life(self) -> int:
        return self.__life
    

    @property
    def get_damage(self) -> int:
        return self.__damage
    

    @property
    def get_score(self) -> int:
        return self.__score
    

    @property
    def get_bullet_time(self):
        return self.__bullet_time
    

    @get_bullet_time.setter
    def set_bullet_time(self, bullet_time):
        self.__bullet_time = bullet_time

    
    @property
    def get_ready(self):
        return self.__ready
    

    @get_ready.setter
    def set_ready(self, ready):
        self.__ready = ready
    

    @property
    def get_is_looking_right(self):
        return self.__is_looking_right
    

    @property
    def get_is_shooting(self):
        return  self.__is_shooting
    

    @get_is_shooting.setter
    def set_is_shooting(self, status: bool):
        self.__is_shooting = status
    

    @property
    def get_bullet_group(self):
        return self.__bullet_group



    def create_arrow(self):
        if self.__is_looking_right:
            return Bullet(self.rect.right, self.rect.centery + 20, "right", "assets/img/enemy/bullet/Arrow.png")
        else:
            return Bullet(self.rect.left, self.rect.centery + 20, "left", "assets/img/enemy/bullet/Arrow.png")
        
    
    def shoot_arrow(self):
        if self.__ready:
            self.__bullet_group.add(self.create_arrow())
            self.change_animation(self.__attack_r if self.__is_looking_right else self.__attack_l)
        


    def recharge(self):
        if not self.__ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.__bullet_time >= self.__bullet_cooldown:
                self.__ready = True


    def change_animation(self, nueva_animacion: list[pygame.surface.Surface]):
        self.__actual_animation = nueva_animacion
        if self.__initial_frame > 0:
            self.__initial_frame = 0
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]

    
    def __set_x_animations_preset(self, animation_list: list[pygame.surface.Surface], look_r: bool):
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r
    

    def walk(self, direction: str):
        match direction:
            case "Right":
                look_right = True
                self.__set_x_animations_preset(self.__walk_r, look_r=look_right)
            case 'Left':
                look_right = False
                self.__set_x_animations_preset(self.__walk_l, look_r=look_right)
    

    def constraint(self):
        if self.__life > 0 and not self.__is_shooting:
            if self.__is_looking_right:
                if (self.rect.right + self.__speed_walk ) < self.__max_constraint_x:
                    if self.__actual_animation not in (self.__walk_l, self.__walk_r):
                        self.change_animation(self.__walk_r)
                    self.add_x(self.__speed_walk)
                else:
                    self.__is_looking_right = False
                    self.walk(direction='Left')
            else:
                if self.rect.left - self.__speed_walk > 0:
                    if self.__actual_animation not in (self.__walk_l, self.__walk_r):
                        self.change_animation(self.__walk_l)
                    self.add_x(-self.__speed_walk)
                else:
                    self.__is_looking_right = True
                    self.walk(direction='Right')
    

    def do_movement(self, delta_ms, plataformas):
        self.__time_move += delta_ms
        if self.__time_move >= self.__frame_rate:
            self.constraint()
            if not self.is_on_ground(plataformas):
                self.add_y(self.__gravity)
            else: self.add_y(self.__move_y)

    
    def do_animation(self, delta_ms):
        self.__enemy_animation_time += delta_ms
        if self.__enemy_animation_time >= self.__frame_rate:
            self.__enemy_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0
        
    

    def add_x(self, delta_x):
        self.rect.x += delta_x
        self.rect_ground_collition.x += delta_x
        self.rect_vision_left.x += delta_x
        self.rect_vision_right.x += delta_x
        self.rect_right_collition.x += delta_x
        self.rect_left_collition.x += delta_x
    
    
    def add_y(self, delta_y):
        self.rect.y += delta_y
        self.rect_ground_collition.y += delta_y
        self.rect_vision_left.y += delta_y
        self.rect_vision_right.y += delta_y
        self.rect_right_collition.y += delta_y
        self.rect_left_collition.y += delta_y


    def is_on_ground(self, plataformas):
        retorno = False
        for plataforma in plataformas:
            if self.rect_ground_collition.colliderect(plataforma.rect_ground_collition):
                retorno = True
                break
        return retorno
    

    

    

    def hit(self, damage):
        if self.__life > 0:
            self.__life -= damage

    
    def dead(self):
        if self.__life == 0:
            if self.__actual_animation not in (self.__dead_l, self.__dead_r):
                self.change_animation(self.__dead_r) if self.__is_looking_right else  self.change_animation(self.__dead_l)
                self.kill()


        

    def update(self, delta_ms, screen: pygame.surface.Surface, plataformas):
        self.draw(screen)
        self.do_movement(delta_ms, plataformas)
        self.do_animation(delta_ms)
        self.recharge()
        self.dead()
        self.__bullet_group.draw(screen)
        self.__bullet_group.update(screen)

    
    def draw(self, screen: pygame.surface.Surface):
        if DEBUG:
            pygame.draw.rect(screen, 'red', self.rect)
            pygame.draw.rect(screen, 'blue', self.rect_ground_collition)
            pygame.draw.rect(screen, 'blue', self.rect_right_collition)
            pygame.draw.rect(screen, 'blue', self.rect_left_collition)
            # pygame.draw.rect(screen, 'green', self.rect_vision_left)
            # pygame.draw.rect(screen, 'grey', self.rect_vision_right)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation, self.rect)
