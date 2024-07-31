import pygame
from config import *
from graphics_utils import *
from collections import deque

active_widgets = set()

class Widget:
    def handle_event(self, event):
        raise NotImplementedError("Subclass needs to define handle_event")

    def __init__(self):
        self.priority = 0 # Lower means it has more priority.
        active_widgets.add(self)
    
    def __del__(self):
        active_widgets.discard(self)

# Button class
class Button(Widget):
    def __init__(self, text, x, y, width, height, callback, color=None, text_color=button_text_color, selected_color=None):
        super().__init__()
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
        self.selected_color = selected_color if selected_color else button_hover_color

        self.is_selected = False
        active_widgets.add(self)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.is_selected:
            color = self.selected_color
        elif self.x - self.hitbox_size <= mouse_pos[0] <= self.x + self.width + self.hitbox_size and \
        self.y - self.hitbox_size <= mouse_pos[1] <= self.y + self.height + self.hitbox_size:
            color = button_hover_color
        else:
            color = self.color if self.color else button_color

        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.x + (self.width - text_surface.get_width()) // 2, self.y + (self.height - text_surface.get_height()) // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if point_in_box(mouse_pos, (self.x, self.y, self.width, self.width), mode='size'):
                self.callback()
                return True


# Slider class
class Slider(Widget):
    def __init__(self, x, y, width, height, min_value, max_value, initial_value, callback, orient='down2up'):
        super().__init__()
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
        self.orient = orient

    def draw(self, screen):
        track_color = slider_color
        handle_color = self.handle_interact_color if self.is_being_interacted else slider_handle_color

        pygame.draw.rect(screen, track_color, (self.x, self.y, self.track_thickness, self.height))
        handle_y = self.y + (self.height - self.handle_height) * (1 - (self.value - self.min_value) / (self.max_value - self.min_value))
        pygame.draw.rect(screen, handle_color, (self.x, handle_y, self.track_thickness, self.handle_height))

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if point_in_box(mouse_pos, (self.x, self.y, self.track_thickness, self.height), mode='size'):
                self.is_being_interacted = True
                self.set_value_from_mouse(mouse_pos)
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_being_interacted = False
            if self.is_being_interacted:
                return True
        elif event.type == pygame.MOUSEMOTION:
            if self.is_being_interacted:
                self.set_value_from_mouse(mouse_pos)
                return True
    
    def set_value_from_mouse(self, mouse_pos):
        self.value = (mouse_pos[1] - self.y) / self.height
        self.value = clamp(self.value, 0, 1)
        if self.orient == 'down2up':
            self.value = 1 - self.value
        self.callback(self.value)
        
    def set_value(self, value):
        self.value = value

# We'll just assume it takes up the whole screen for now
# But it would be nice to not have to assume this (maybe you
# want to leave room for a chat window later for example).
class Canvas(Widget):
    def __init__(self, screen, on_stroke_finish=lambda: None):
        super().__init__()

        self.screen = screen
        self.on_stroke_finish = on_stroke_finish

        # setting initial tool mode, color, and sizes
        self.curr_tool = 'pen'
        self.pen_color = initial_pen_color
        self.tool_sizes = {'pen': 5, 'eraser': 20, 'rectangle': 5, 'circle': 5}

        self.is_being_interacted = False
        self.stroke_made = False
        self.start_pos = None
        self.last_pos = None

        self.curr_state = None
        self.undo_stack = deque(maxlen=max_undo_steps)
        self.redo_stack = deque(maxlen=max_undo_steps)

    def draw(self, screen):
        pass

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.is_being_interacted = True
            self.stroke_made = False
            self.start_pos = event.pos[0] * 2, event.pos[1] * 2
            self.last_pos = self.start_pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if not self.is_being_interacted:
                return False
            
            if self.stroke_made:
                self.on_stroke_finish()

            self.is_being_interacted = False
            self.start_pos = None
            self.last_pos = None
        elif event.type == pygame.MOUSEMOTION:
            if not self.is_being_interacted:
                return False
            
            screen = self.screen
            curr_state = self.curr_state
            curr_tool = self.curr_tool

            start_pos = self.start_pos
            sx, sy = start_pos
            curr_pos  = event.pos[0] * 2, event.pos[1] * 2
            cx, cy = curr_pos
            last_pos  = self.last_pos
            curr_width = self.tool_sizes[curr_tool]
            curr_color = background_color if curr_tool == 'eraser' else self.pen_color

            if curr_tool == 'pen' or curr_tool == 'eraser':
                draw_line(self.screen, curr_color, last_pos, curr_pos, curr_width)
            elif curr_tool == 'rectangle' and start_pos:
                screen.blit(curr_state, (0, 0))  # restore the screen to the state before drawing the shape
                pygame.draw.rect(screen, curr_color, (sx, sy, cx - sx, cy - sy), curr_width // 2)
            elif curr_tool == 'circle' and start_pos:
                screen.blit(curr_state, (0, 0))  # restore the screen to the state before drawing the shape
                radius = int(math.hypot(cx-sx,cy-sy))
                pygame.draw.circle(screen, curr_color, start_pos, radius, curr_width // 2)
            self.last_pos = curr_pos
            self.stroke_made = True

        return True
    
    def set_curr_tool_size(self, new_size):
        self.tool_sizes[self.curr_tool] = new_size
    
    def clear(self):
        self.save_state()
        self.screen.fill(background_color)

    def save_state(self):
        self.curr_state = self.screen.copy()
        self.undo_stack.append(self.curr_state)
        self.redo_stack.clear()
    
    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.undo_stack.pop())
            self.curr_state = self.undo_stack[-1].copy()
            self.screen.blit(self.curr_state, (0, 0))
    
    def redo(self):
        if self.redo_stack:
            self.curr_state = self.redo_stack.pop()
            self.undo_stack.append(self.curr_state)
            self.screen.blit(self.curr_state, (0, 0))



