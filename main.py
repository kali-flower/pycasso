import pygame
import math

# initialize pygame
pygame.init()

# original window size based on user screen
info = pygame.display.Info()
screen_width = int(info.current_w * 0.8)
screen_height = int(info.current_h * 0.8)

# colors
background_color = (255, 255, 255)
pen_color = (0, 0, 0)
eraser_color = background_color
button_color = (200, 200, 200)
button_hover_color = (150, 150, 150)
button_text_color = (0, 0, 0)
slider_color = (180, 180, 180)
slider_handle_color = (100, 100, 100)

# variables
current_tool = 'pen'

# more colors! :D
colors = [
    (0, 0, 0),        # black
    (255, 142, 156),  # red
    (255, 185, 147),  # orange
    (243, 238, 155),  # yellow
    (171, 232, 162),  # green
    (153, 214, 234),  # cyan
    (138, 171, 239),  # blue
    (178, 160, 255),  # violet
    (255, 169, 216)   # pink
]

# supersampled window size --> 2x original
SUPER_WIDTH, SUPER_HEIGHT = screen_width * 2, screen_height * 2

# initialize display for supersampling
super_screen = pygame.Surface((SUPER_WIDTH, SUPER_HEIGHT))
super_screen.fill(background_color)  # clear supersampled screen

# initialize display window
screen = pygame.display.set_mode((screen_width, screen_height))

# Button class
class Button:
    def __init__(self, text, x, y, width, height, callback, color=None, text_color=button_text_color, selected_color=None):
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
            color = button_hover_color
        else:
            color = self.color if self.color else button_color

        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.x + (self.width - text_surface.get_width()) // 2, self.y + (self.height - text_surface.get_height()) // 2))

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.x - self.hitbox_size <= mouse_pos[0] <= self.x + self.width + self.hitbox_size and \
               self.y - self.hitbox_size <= mouse_pos[1] <= self.y + self.height + self.hitbox_size:
                self.callback()

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

    def draw(self, screen):
        pygame.draw.rect(screen, slider_color, (self.x, self.y, self.track_thickness, self.height))
        handle_y = self.y + (self.height - self.handle_height) * (1 - (self.value - self.min_value) / (self.max_value - self.min_value))
        pygame.draw.rect(screen, slider_handle_color, (self.x, handle_y, self.track_thickness, self.handle_height))
    
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


# function to interpolate points between two points
def interpolate_points(start, end, distance):
    x0, y0 = start
    x1, y1 = end
    points = []
    dx = x1 - x0
    dy = y1 - y0
    length = math.sqrt(dx * dx + dy * dy)
    num_points = max(int(length / distance), 1)
    for i in range(num_points):
        t = i / num_points
        x = x0 + t * dx
        y = y0 + t * dy
        points.append((int(x), int(y)))
    points.append(end)
    return points

# draw function using interpolation
def draw_line(screen, color, start, end, width):
    points = interpolate_points(start, end, 1)
    for point in points:
        pygame.draw.circle(screen, color, point, width // 2)

# clear canvas function
def clear_canvas():
    super_screen.fill(background_color)

# set pen tool function 
def set_pen_tool():
    global pen_color, current_tool
    pen_color = (0, 0, 0)  # pen color
    current_tool = 'pen'
    size_slider.set_value(sizes['pen'])  # slider will match with pen size --> retrieve from hashmap 

def set_eraser_tool():
    global pen_color, current_tool
    pen_color = eraser_color  # eraser color
    current_tool = 'eraser'
    size_slider.set_value(sizes['eraser'])  # slider will match with eraser size -- retrieve from hashmap 


# Function to update brush size
def update_brush_size(new_size):
    sizes[current_tool] = new_size  # save current tool's size 
    if current_tool == 'pen':
        pen_width = new_size
    else:
        eraser_width = new_size
    size_slider.set_value(new_size)  # update slider's value to reflect new size

# set pen color function 
def set_color(color):
    global pen_color
    pen_color = color
    pen_button.text_color = color  # update pen button text color

# create button instances
clear_button = Button('Clear', 10, 10, 100, 50, clear_canvas)
pen_button = Button('Pen', 120, 10, 100, 50, set_pen_tool, text_color=pen_color, selected_color=(100, 100, 100))
eraser_button = Button('Eraser', 230, 10, 100, 50, set_eraser_tool, selected_color=(100, 100, 100))

# create color buttons
color_buttons = []
color_x = 10
for color in colors:
    color_buttons.append(Button('', color_x, screen_height - 60, 50, 50, lambda c=color: set_color(c), color))
    color_x += 60

# slider height and positioning
slider_width = 20
slider_height = int(screen_height * 0.7)
slider_x = 10
slider_y = (screen_height - slider_height) // 2

# create slider instance 
size_slider = Slider(slider_x, slider_y, slider_width, slider_height, 5, 100, 10, update_brush_size)

# set initial tool mode and sizes
sizes = {'pen': 10, 'eraser': 10} 
pen_width = sizes['pen']
eraser_width = sizes['eraser']

# main loop
running = True
drawing = False
last_pos = None
color_button_active = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if (slider_x <= mouse_pos[0] <= slider_x + size_slider.track_thickness and
                slider_y <= mouse_pos[1] <= slider_y + slider_height):
                size_slider.update(event)
                drawing = False
            else:
                color_button_active = False
                for button in color_buttons:
                    if (button.x - button.hitbox_size <= mouse_pos[0] <= button.x + button.width + button.hitbox_size and
                        button.y - button.hitbox_size <= mouse_pos[1] <= button.y + button.height + button.hitbox_size):
                        color_button_active = True
                        button.is_clicked(event)
                        drawing = False
                        break

                if not color_button_active:
                    drawing = True
                    last_pos = event.pos[0] * 2, event.pos[1] * 2
        elif event.type == pygame.MOUSEBUTTONUP:
            size_slider.update(event)
            drawing = False
            color_button_active = False
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                current_pos = event.pos[0] * 2, event.pos[1] * 2
                current_width = sizes[current_tool] * 2
                draw_line(super_screen, pen_color, last_pos, current_pos, current_width)
                last_pos = current_pos
            else:
                size_slider.update(event)  # update slider while moving the mouse

        # check if the buttons are clicked
        clear_button.is_clicked(event)
        pen_button.is_clicked(event)
        eraser_button.is_clicked(event)
        for button in color_buttons:
            button.is_clicked(event)

    # clear screen before drawing
    screen.fill(background_color)

    # downscale supersampled image
    pygame.transform.scale(super_screen, (screen_width, screen_height), screen)

    # draw the buttons
    clear_button.draw(screen)
    pen_button.draw(screen, is_selected=(current_tool == 'pen'))
    eraser_button.draw(screen, is_selected=(current_tool == 'eraser'))
    for button in color_buttons:
        button.draw(screen)

    # draw the slider
    size_slider.draw(screen)

    # update display
    pygame.display.flip()

pygame.quit()