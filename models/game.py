import pygame 
import sys
from auxiliar.constantes import *
from models.stage import Stage

class Game:
    
    def __init__(self) -> None:
        pass

    def run_stage(stage_name: str):
        pygame.init()
    
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

            screen.blit(back_img, back_img.get_rect())
            delta_ms = clock.tick(60)
            game.run(delta_ms)
            pygame.display.flip()