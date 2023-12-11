import pygame
from auxiliar.constantes import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, tile) -> None:
        super().__init__()

        self.image = pygame.image.load(tile)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=pos)
        self.rect_ground_collition = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, 10)
        

    
    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.image, self.rect)
        if DEBUG:
            pygame.draw.rect(screen, 'green', self.rect_ground_collition)
    

    def update(self, screen: pygame.surface.Surface):
        self.draw(screen)