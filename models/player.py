import pygame
from auxiliar.auxiliar import SurfaceManager as sm
from auxiliar.constantes import DEBUG

class Player(pygame.sprite.Sprite):

    def __init__(self, constraint_x, constraint_y, stage_dict_configs: dict, frame_rate = 100, speed_run = 12, gravity = 16, jump = 32):
        super().__init__()

        self.__player_configs = stage_dict_configs.get('player')
        self.__player_cords = self.__player_configs['coords_player']
        self.image = pygame.image.load(self.__player_configs['player_img']).convert_alpha()
        self.__iddle_r = sm.get_surface('./assets/img/player/idle/Idle1.png', 4, 1)
        self.__iddle_l = sm.get_surface('./assets/img/player/idle/Idle1.png', 4, 1, flip=True)
        self.__run_r = sm.get_surface('./assets/img/player/run/Run1.png', 6, 1)
        self.__run_l = sm.get_surface('./assets/img/player/run/Run1.png', 6, 1, flip=True)
        self.__jump_r = sm.get_surface('./assets/img/player/jump/Jump1.png', 4, 1)
        self.__jump_l = sm.get_surface("./assets/img/player/jump/Jump1.png", 4, 1, flip=True)
        self.__move_x = self.__player_cords['coord_x']
        self.__move_y = self.__player_cords['coord_y']
        self.__speed_run = speed_run
        self.__max_constraint_x = constraint_x
        self.__max_constraint_y = constraint_y
        self.__frame_rate = frame_rate
        self.__player_move_time = 0
        self.__player_animation_time = 0
        self.__gravity = gravity
        self.__initial_frame = 0
        self.__actual_animation = self.__iddle_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.rect = self.__actual_img_animation.get_rect()
        self.__is_looking_right = True

    def __set_x_animations_preset(self, move_x, animation_list: list[pygame.surface.Surface], look_r: bool):
        self.__move_x = move_x
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r


    def __set_y_animations_preset(self):
        self.__move_y = -self.__jump
        self.__move_x = self.__speed_run if self.__is_looking_right else -self.__speed_run
        self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
        self.__initial_frame = 0
        self.__is_jumping = True

    

    def run(self, direction: str = 'Right'):
        self.__initial_frame = 0
        match direction:
            case 'Right':
                look_right = True
                self.__set_x_animations_preset(self.__speed_run, self.__run_r, look_r=look_right)
            case 'Left':
                look_right = False
                self.__set_x_animations_preset(-self.__speed_run, self.__run_l, look_r=look_right)
    

    def stay(self):
        if self.__actual_animation != self.__iddle_l and self.__actual_animation != self.__iddle_r:
            self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
            self.__initial_frame = 0
            self.__move_x = 0
            self.__move_y = 0

    def __set_borders_limits(self):
        pixels_move = 0
        if self.__move_x > 0:
            pixels_move = self.__move_x if self.rect.x < self.__max_constraint_x - self.__actual_img_animation.get_width() else 0
        elif self.__move_x < 0:
            pixels_move = self.__move_x if self.rect.x > 0 else 0
        return pixels_move
    

    def do_movement(self, delta_ms):
        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate:
            self.__player_move_time = 0
            self.rect.x += self.__set_borders_limits()
            self.rect.y += self.__move_y
            # Parte relacionado a saltar
            if self.rect.y < 300:
                self.rect.y += self.__gravity
    

    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0
                # if self.__is_jumping:
                #     self.__is_jumping = False
                #     self.__move_y = 0


    def eventos_teclado(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.run('Right')


    def constraint(self):  # Ajusta al jugador a los limites de la pantalla
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.__max_constraint_x:
            self.rect.right = self.__max_constraint_x
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.__max_constraint_y:
            self.rect.bottom = self.__max_constraint_y
    
    def update(self, delta_ms):
        self.eventos_teclado()
        self.constraint()
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)


    def draw(self, screen: pygame.surface.Surface):
        if DEBUG:
            pygame.draw.rect(screen, 'red', self.rect)
            #pg.draw.rect(screen, 'green', self.__rect.bottom)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation, self.rect)
        
