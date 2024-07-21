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

# supersampled window size --> 2x original
SUPER_WIDTH, SUPER_HEIGHT = screen_width * 2, screen_height * 2

# initialize display for supersampling
super_screen = pygame.Surface((SUPER_WIDTH, SUPER_HEIGHT))
super_screen.fill(background_color)  # clear supersampled screen

# initialize display window
screen = pygame.display.set_mode((screen_width, screen_height))

# button class
class Button:
    def __init__(self, text, x, y, width, height, callback):
        # initialize button 
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.callback = callback
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        # draw button on the screen 
        mouse_pos = pygame.mouse.get_pos()
        # check if mouse is hovering over button
        if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
            color = button_hover_color
        else:
            color = button_color

        # draw rectangle and render text 
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        text_surface = self.font.render(self.text, True, button_text_color)
        screen.blit(text_surface, (self.x + (self.width - text_surface.get_width()) // 2, self.y + (self.height - text_surface.get_height()) // 2))

    def is_clicked(self, event):
        # check if button is clicked 
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
                self.callback()

# slider class
class Slider:
    def __init__(self, x, y, width, height, min_value, max_value, initial_value, callback):
        # initialize slider
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value  
        self.callback = callback
        self.handle_height = 20
        self.track_thickness = self.handle_height + 15  # make track thickness 15 px thicker 
        self.is_being_interacted = False  # flag to check if slider is being interacted with 

    def draw(self, screen):
        # draw slider track and handle
        pygame.draw.rect(screen, slider_color, (self.x - 7.5, self.y, self.track_thickness, self.height))  # Track centered on x position
        # calculate handle position 
        handle_y = self.y + (self.height - self.handle_height) * (1 - (self.value - self.min_value) / (self.max_value - self.min_value))
        pygame.draw.rect(screen, slider_handle_color, (self.x - 7.5, handle_y, self.track_thickness, self.handle_height))
    
    def update(self, event):
        # update slider value based on mouse position
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (self.x - 7.5 <= mouse_pos[0] <= self.x - 7.5 + self.track_thickness) and \
               self.y <= mouse_pos[1] <= self.y + self.height:
                self.is_being_interacted = True
                self.set_value_from_mouse(mouse_pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_being_interacted = False
        elif event.type == pygame.MOUSEMOTION:
            if self.is_being_interacted:
                self.set_value_from_mouse(mouse_pos)
    
    def set_value_from_mouse(self, mouse_pos):
        # calculate value from mouse position
        self.value = self.min_value + (self.max_value - self.min_value) * (1 - (mouse_pos[1] - self.y) / self.height)
        self.value = max(self.min_value, min(self.max_value, self.value))
        self.callback(self.value)

# function to interpolate points between two points
def interpolate_points(start, end, distance):
    x0, y0 = start
    x1, y1 = end
    points = []
    dx = x1 - x0
    dy = y1 - y0
    length = math.sqrt(dx * dx + dy * dy)
    num_points = max(int(length / distance), 1)  # ensure at least 1 point is generated
    for i in range(num_points):
        t = i / num_points
        x = x0 + t * dx
        y = y0 + t * dy
        points.append((int(x), int(y)))
    points.append(end)  # include the end point
    return points

# draw function using interpolation
def draw_line(screen, color, start, end, width):
    points = interpolate_points(start, end, 1)
    for point in points:
        pygame.draw.circle(screen, color, point, width // 2)

# clear canvas function
def clear_canvas():
    super_screen.fill(background_color)

# function to set pen tool
def set_pen_tool():
    global pen_color
    pen_color = (0, 0, 0)  # pen color

# function to set eraser tool
def set_eraser_tool():
    global pen_color
    pen_color = eraser_color  # eraser color

# function to update brush size
def update_brush_size(new_size):
    global width
    width = int(new_size)

# create button instances
clear_button = Button('Clear', 10, 10, 100, 50, clear_canvas)
pen_button = Button('Pen', 120, 10, 100, 50, set_pen_tool)
eraser_button = Button('Eraser', 230, 10, 100, 50, set_eraser_tool)

# slider height and positioning
slider_width = 20
slider_height = int(screen_height * 0.7)  # 70% of screen height
slider_x = 10
slider_y = (screen_height - slider_height) // 2  # Centered vertically

# create slider instance 
brush_size_slider = Slider(slider_x, slider_y, slider_width, slider_height, 5, 50, 10, update_brush_size)

# set initial tool mode
pen_color = (0, 0, 0)
width = 10

# main loop
running = True
drawing = False
last_pos = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if within slider area
            mouse_pos = pygame.mouse.get_pos()
            if (slider_x - 7.5 <= mouse_pos[0] <= slider_x - 7.5 + brush_size_slider.track_thickness) and \
               slider_y <= mouse_pos[1] <= slider_y + slider_height:
                brush_size_slider.update(event)
                drawing = False
            else:
                drawing = True
                last_pos = event.pos[0] * 2, event.pos[1] * 2
                brush_size_slider.update(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            brush_size_slider.update(event)
            drawing = False
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                current_pos = event.pos[0] * 2, event.pos[1] * 2
                draw_line(super_screen, pen_color, last_pos, current_pos, width * 2)
                last_pos = current_pos
            else:
                brush_size_slider.update(event)  # update slider while moving the mouse

        # check if the buttons are clicked
        clear_button.is_clicked(event)
        pen_button.is_clicked(event)
        eraser_button.is_clicked(event)

    # clear screen before drawing
    screen.fill(background_color)

    # downscale supersampled image
    pygame.transform.scale(super_screen, (screen_width, screen_height), screen)

    # draw the buttons
    clear_button.draw(screen)
    pen_button.draw(screen)
    eraser_button.draw(screen)
    
    # draw the slider
    brush_size_slider.draw(screen)

    # update display
    pygame.display.flip()

pygame.quit()
