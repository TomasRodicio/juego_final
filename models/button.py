import pygame


class Button():
    def __init__(self, pos, font, text, color, onclick, onclick_param, size, color_background = "black", color_border = "red", border_size: int = -1) -> None:
        
        self.on_click = onclick
        self.on_click_param = onclick_param
        self.font = font
        self.text = text
        self.font_color = color
        self.color_background = color_background
        self.color_border= color_border
        self.border_size = border_size
        self.w = size[0]
        self.h = size[1]
        self.x = pos[0]
        self.y = pos[1]
        self.__is_clicked = False

        self.render()


    
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
        media_vertical  =self.h / 2

        diferencia_horizontal = media_horizontal - media_text_horizontal
        diferencia_vertical = media_vertical - media_text_vertical

        self.slave.blit(self.__text_render, (diferencia_horizontal, diferencia_vertical))
    

    def update(self, evento, screen):
        self.__is_clicked = False
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.slave_rect_collide.collidepoint(evento.pos):
                self.__is_clicked = True
                self.on_click(self.on_click_param)
        self.draw(screen)

    
    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.slave,self.slave_rect)
        pygame.draw.rect(screen, self.color_border, self.slave_rect, self.border_size)