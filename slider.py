import pygame
from config import SLIDER_COLOR, SLIDER_HANDLE_COLOR

# Slider class
class Slider:
    def __init__(self, x, y, width, height, min_value, max_value, initial_value, callback):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value  
        self.callback = callback
        self.handle_height = 20
        self.track_thickness = self.width
        self.is_being_interacted = False
        self.handle_interact_color = (60, 60, 60)  # darker handle color when user is interacting with it 

    def draw(self, screen):
        track_color = SLIDER_COLOR
        handle_color = self.handle_interact_color if self.is_being_interacted else SLIDER_HANDLE_COLOR

        pygame.draw.rect(screen, track_color, (self.x, self.y, self.track_thickness, self.height))
        handle_y = self.y + (self.height - self.handle_height) * (1 - (self.value - self.min_value) / (self.max_value - self.min_value))
        pygame.draw.rect(screen, handle_color, (self.x, handle_y, self.track_thickness, self.handle_height))

    def update(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x <= mouse_pos[0] <= self.x + self.track_thickness and self.y <= mouse_pos[1] <= self.y + self.height:
                self.is_being_interacted = True
                self.set_value_from_mouse(mouse_pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_being_interacted = False
        elif event.type == pygame.MOUSEMOTION:
            if self.is_being_interacted:
                self.set_value_from_mouse(mouse_pos)

    
    def set_value_from_mouse(self, mouse_pos):
        relative_pos = (mouse_pos[1] - self.y) / self.height
        new_size = 5 + (100 - 5) * (1 - relative_pos)  # use interpolation to calculate sizes along slider 
        new_size = max(5, min(100, new_size))  # make sure value is in bounds 
        self.value = new_size
        self.callback(new_size)
        
    def set_value(self, value):
        self.value = value