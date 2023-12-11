import pygame
from auxiliar.auxiliar import SurfaceManager as sm
from auxiliar.constantes import DEBUG
from models.bullet import Bullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, constraint_x, constraint_y, stage_dict_configs: dict, frame_rate = 30, speed_walk = 3, gravity = 16) -> None:
        super().__init__()
        self.__enemies_configs = stage_dict_configs.get('enemies')
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
        self.__max_constraint_x = constraint_x
        self.__max_constraint_y = constraint_y

        self.__ready = True
        self.__bullet_time = 0
        self.__bullet_cooldown = 1000
        self.__bullet_group = pygame.sprite.Group()

        self.rect_ground_collition = pygame.Rect(self.rect.x + self.rect.w / 4, self.rect.y + self.rect.h - 10, self.rect.w / 2, 10)


    def change_animation(self, nueva_animacion: list[pygame.surface.Surface]):
        self.__actual_animation = nueva_animacion
        if self.__initial_frame > 0:
            self.__initial_frame = 0
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]

    
    def __set_x_animations_preset(self, move_x, animation_list: list[pygame.surface.Surface], look_r: bool):
        self.__move_x = move_x
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r
    

    def walk(self, direction: str):
        match direction:
            case "Right":
                look_right = True
                self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, look_r=look_right)
            case 'Left':
                look_right = False
                self.__set_x_animations_preset(-self.__speed_walk, self.__walk_l, look_r=look_right)
    

    def constraint(self):  # Ajusta al jugador a los limites de la pantalla
        if self.__is_looking_right:
            if (self.rect.right + self.__speed_walk ) < self.__max_constraint_x:
                self.add_x(self.__speed_walk)
            else:
                self.__is_looking_right = False
                self.change_animation(self.__walk_l)
                self.walk(direction='Left')
        else:
            if self.rect.left - self.__speed_walk > 0:
                self.add_x(-self.__speed_walk)
            else:
                self.__is_looking_right = True
                self.change_animation(self.__walk_r)
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
    
    
    def add_y(self, delta_y):
        self.rect.y += delta_y
        self.rect_ground_collition.y += delta_y


    def is_on_ground(self, plataformas):
        retorno = False
        for plataforma in plataformas:
            if self.rect_ground_collition.colliderect(plataforma.rect_ground_collition):
                retorno = True
                break
        return retorno
        

    def update(self, delta_ms, screen: pygame.surface.Surface, plataformas):
        self.draw(screen)
        self.do_movement(delta_ms, plataformas)
        self.do_animation(delta_ms)
        # self.recharge()
        self.__bullet_group.draw(screen)
        self.__bullet_group.update()

    
    def draw(self, screen: pygame.surface.Surface):
        if DEBUG:
            pygame.draw.rect(screen, 'red', self.rect)
            pygame.draw.rect(screen, 'blue', self.rect_ground_collition)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.image = self.__actual_img_animation
        screen.blit(self.__actual_img_animation, self.rect)
