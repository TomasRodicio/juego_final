import pygame
from auxiliar.constantes import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, tile) -> None:
        super().__init__()

        self.image = pygame.image.load(tile)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=pos)
        self.rect_ground_collition = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, 10)
        self.rect_ceiling_collition = pygame.Rect(self.rect.x, self.rect.y + self.rect.h - 10, self.rect.w, 10)
        self.rect_left_collition = pygame.Rect(self.rect.x, self.rect.y + self.rect.h / 4, self.rect.w * 0.2, self.rect.h / 2)
        self.rect_right_collition = pygame.Rect(self.rect.x + self.rect.w - 10, self.rect.y + self.rect.h / 4, self.rect.w * 0.2, self.rect.h / 2)
        

    
    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.image, self.rect)
        if DEBUG:
            pygame.draw.rect(screen, 'blue', self.rect_ground_collition)
            pygame.draw.rect(screen, 'blue', self.rect_ceiling_collition)
            pygame.draw.rect(screen, 'blue', self.rect_left_collition)
            pygame.draw.rect(screen, 'blue', self.rect_right_collition)
    

    def update(self, screen: pygame.surface.Surface):
        self.draw(screen)