import pygame
from config import BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR

# Button class
class Button:
    def __init__(self, text, x, y, width, height, callback, color=None, text_color=BUTTON_TEXT_COLOR, selected_color=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.callback = callback
        self.font = pygame.font.Font(None, 36)
        self.color = color  # button colors
        self.text_color = text_color  # dynamic text color
        self.selected_color = selected_color
        self.hitbox_size = 10  # hitbox for better click detection 

    def draw(self, screen, is_selected=False):
        mouse_pos = pygame.mouse.get_pos()
        if is_selected:
            color = self.selected_color
        elif self.x - self.hitbox_size <= mouse_pos[0] <= self.x + self.width + self.hitbox_size and \
           self.y - self.hitbox_size <= mouse_pos[1] <= self.y + self.height + self.hitbox_size:
            color = BUTTON_HOVER_COLOR
        else:
            color = self.color if self.color else BUTTON_COLOR

        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.x + (self.width - text_surface.get_width()) // 2, self.y + (self.height - text_surface.get_height()) // 2))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.x - self.hitbox_size <= mouse_pos[0] <= self.x + self.width + self.hitbox_size and \
               self.y - self.hitbox_size <= mouse_pos[1] <= self.y + self.height + self.hitbox_size:
                self.callback()