import pygame
from config import *
from graphics_utils import *
from collections import deque

active_widgets = set()

# utility function to darken colors
def darken_color(color, factor=0.7):
    return tuple(int(c * factor) for c in color)

class Widget:
    def handle_event(self, event):
        raise NotImplementedError("Subclass needs to define handle_event")

    def __init__(self):
        self.priority = 0 # lower = more priority 
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
            self.color = color if color else button_color
            self.text_color = text_color
            self.selected_color = selected_color if selected_color else button_hover_color
            self.hover_color = darken_color(self.color) if color else button_hover_color
            self.hitbox_size = 10
            self.is_selected = False

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.is_selected:
            color = self.selected_color
        elif self.x - self.hitbox_size <= mouse_pos[0] <= self.x + self.width + self.hitbox_size and \
             self.y - self.hitbox_size <= mouse_pos[1] <= self.y + self.height + self.hitbox_size:
            color = self.hover_color
        else:
            color = self.color

        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.x + (self.width - text_surface.get_width()) // 2, 
                                   self.y + (self.height - text_surface.get_height()) // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
                self.callback()
                return True
        return False


# Slider class
class Slider(Widget):
    def __init__(self, x, y, width, height, min_value, max_value, initial_value, callback, orient='vertical'):
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
        self.is_being_dragged = False
        self.orient = orient

    def draw(self, screen):
        # draw track
        pygame.draw.rect(screen, slider_color, (self.x, self.y, self.width, self.height))
        
        # calculate handle position
        handle_pos = self.y + (self.height - self.handle_height) * (1 - (self.value - self.min_value) / (self.max_value - self.min_value))
        
        # draw handle
        pygame.draw.rect(screen, slider_handle_color, (self.x, handle_pos, self.width, self.handle_height))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x <= event.pos[0] <= self.x + self.width and self.y <= event.pos[1] <= self.y + self.height:
                self.is_being_dragged = True
                self.update_value(event.pos[1])
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_being_dragged = False
        elif event.type == pygame.MOUSEMOTION and self.is_being_dragged:
            self.update_value(event.pos[1])
            return True
        return False

    def update_value(self, y_pos):
        normalized_pos = 1 - (y_pos - self.y) / self.height
        self.value = self.min_value + normalized_pos * (self.max_value - self.min_value)
        self.value = max(self.min_value, min(self.max_value, self.value))
        self.callback(self.value)

    def set_value(self, value):
        self.value = max(self.min_value, min(self.max_value, value))


# assume it takes up whole screen -- change later (chat window? :O)
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
            curr_pos = event.pos[0] * 2, event.pos[1] * 2
            cx, cy = curr_pos
            last_pos = self.last_pos
            curr_width = self.tool_sizes[curr_tool] * 2  # scale width for supersampling
            curr_color = background_color if curr_tool == 'eraser' else self.pen_color

            if curr_tool == 'pen' or curr_tool == 'eraser':
                draw_line(self.screen, curr_color, last_pos, curr_pos, curr_width)
            elif curr_tool == 'rectangle' and start_pos:
                screen.blit(curr_state, (0, 0))  # restore screen to state before drawing the shape
                rect_x = min(sx, cx)  # calculate the top-left x coordinate
                rect_y = min(sy, cy)  # calculate the top-left y coordinate
                rect_width = abs(cx - sx)  # calculate the width
                rect_height = abs(cy - sy)  # calculate the height
                pygame.draw.rect(screen, curr_color, (rect_x, rect_y, rect_width, rect_height), curr_width // 2)
            elif curr_tool == 'circle' and start_pos:
                screen.blit(curr_state, (0, 0))  # restore screen to state before drawing the shape
                radius = int(math.hypot(cx - sx, cy - sy))
                pygame.draw.circle(screen, curr_color, start_pos, radius, curr_width // 2)
            
            self.last_pos = curr_pos
            self.stroke_made = True

        return True

    
    def set_curr_tool_size(self, size):
        self.tool_sizes[self.curr_tool] = round(size)
    
    def clear(self):
        # save current state
        self.save_state()  
        # fill screen with background color
        self.screen.fill(background_color)
        # clear current state to avoid drawing over it later
        self.curr_state = self.screen.copy()  

    def save_state(self):
        self.curr_state = self.screen.copy()
        self.undo_stack.append(self.curr_state)
        self.redo_stack.clear()
    
    def undo(self):
        if len(self.undo_stack) > 1:  # check if there are more than one states in the undo stack
            self.redo_stack.append(self.undo_stack.pop())
            self.curr_state = self.undo_stack[-1].copy()
            self.screen.blit(self.curr_state, (0, 0))
        elif len(self.undo_stack) == 1:  # if it's the last state, keep it and do nothing
            self.curr_state = self.undo_stack[-1].copy()
            self.screen.blit(self.curr_state, (0, 0))


    def redo(self):
        if self.redo_stack:
            self.curr_state = self.redo_stack.pop()
            self.undo_stack.append(self.curr_state)
            self.screen.blit(self.curr_state, (0, 0))

    def draw_preview_outline(self, screen):
        curr_tool = self.curr_tool
        curr_width = self.tool_sizes[curr_tool] 
        curr_color = (0, 0, 0)  # color for outline 

        # get mouse position without scaling
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if curr_tool in ['pen', 'eraser']:
            pygame.draw.circle(screen, curr_color, (mouse_x, mouse_y), curr_width // 2, 1)
        elif curr_tool == 'rectangle':
            rect_x = mouse_x - curr_width // 2
            rect_y = mouse_y - curr_width // 2
            rect_width = curr_width
            rect_height = curr_width
            pygame.draw.rect(screen, curr_color, (rect_x, rect_y, rect_width, rect_height), 1)
        elif curr_tool == 'circle':
            radius = curr_width // 2
            pygame.draw.circle(screen, curr_color, (mouse_x, mouse_y), radius, 1)


class ColorIndicator(Widget):
    def __init__(self, x, y, radius):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.color = initial_pen_color  # default to initial pen color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def update_color(self, new_color):
        self.color = new_color

    def handle_event(self, event):
        return False