import pygame
import unicodedata

class TextBox():
    def __init__(self, pos, size, font, font_color, color_background = "white", color_border = "black", border_size: int = -1) -> None:
        
        self.font = font
        self.font_color = font_color
        self.color_background = color_background
        self.color_border = color_border
        self.border_size = border_size
        self.w = size[0]
        self.h = size[1]
        self.x = pos[0]
        self.y = pos[1]
        self.__text = ""

        self.is_selected = False

        self.render()
    
    
    @property
    def text(self):
        return self.__text
    
    @text.setter
    def text(self, texto):
        self.__text = texto

    
    def render(self):
        self.__text_render = self.font.render(self.text, True, self.font_color)

        self.slave = pygame.surface.Surface((self.w, self.h))
        self.slave_rect = self.slave.get_rect()

        self.slave_rect.x = self.x
        self.slave_rect.y = self.y

        self.slave_rect_collide = pygame.Rect(self.slave_rect)
        self.slave.fill(self.color_background)

        media_text_horizontal = self.__text_render.get_width() / 2
        media_text_vertical = self.__text_render.get_height() / 2

        media_horizontal = self.w / 2
        media_vertical  = self.h / 2

        diferencia_horizontal = media_horizontal - media_text_horizontal
        diferencia_vertical = media_vertical - media_text_vertical

        self.slave.blit(self.__text_render, (diferencia_horizontal, diferencia_vertical))

    
    def update(self, evento, screen):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.slave_rect_collide.collidepoint(evento.pos):
                self.is_selected = True
            else:
                self.is_selected = False
            self.render()
        elif self.is_selected and evento.type == pygame.KEYDOWN:
            caracter = evento.unicode
            if evento.key == pygame.K_BACKSPACE:
                self.__text = self.__text[:-1]
            elif len(caracter) == 1 and unicodedata.category(caracter)[0] != "C":
                self.__text += caracter
            self.render()
        self.draw(screen)

    
    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.slave,self.slave_rect)
        pygame.draw.rect(screen, self.color_border, self.slave_rect, self.border_size)