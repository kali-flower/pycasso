# import pygame
# import math

# from collections import deque
# import copy

# # initialize pygame
# pygame.init()

# # original window size based on user screen
# info = pygame.display.Info()
# screen_width = int(info.current_w * 0.8)
# screen_height = int(info.current_h * 0.8)

# # colors
# background_color = (255, 255, 255)
# pen_color = (0, 0, 0)
# eraser_color = background_color
# button_color = (200, 200, 200)
# button_hover_color = (150, 150, 150)
# button_text_color = (0, 0, 0)
# slider_color = (180, 180, 180)
# slider_handle_color = (100, 100, 100)

# # variables
# current_tool = 'pen'

# max_undo_steps = 11
# undo_stack = deque(maxlen=max_undo_steps)
# current_state = None

# redo_stack = deque(maxlen=max_undo_steps)

# # more colors! :D
# colors = [
#     (0, 0, 0),        # black
#     (255, 142, 156),  # red
#     (255, 185, 147),  # orange
#     (243, 238, 155),  # yellow
#     (171, 232, 162),  # green
#     (153, 214, 234),  # cyan
#     (138, 171, 239),  # blue
#     (178, 160, 255),  # violet
#     (255, 169, 216)   # pink
# ]

# # supersampled window size --> 2x original
# SUPER_WIDTH, SUPER_HEIGHT = screen_width * 2, screen_height * 2

# # initialize display for supersampling
# super_screen = pygame.Surface((SUPER_WIDTH, SUPER_HEIGHT))
# super_screen.fill(background_color)  # clear supersampled screen

# # initialize display window
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("Pycasso") # title :D

# # Button class
# class Button:
#     def __init__(self, text, x, y, width, height, callback, color=None, text_color=button_text_color, selected_color=None):
#         self.text = text
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.callback = callback
#         self.font = pygame.font.Font(None, 36)
#         self.color = color  # button colors
#         self.text_color = text_color  # dynamic text color
#         self.selected_color = selected_color
#         self.hitbox_size = 10  # hitbox for better click detection 
#         self.selected_color = selected_color if selected_color else button_hover_color

#     def draw(self, screen, is_selected=False):
#         mouse_pos = pygame.mouse.get_pos()
#         if is_selected:
#             color = self.selected_color
#         elif self.x - self.hitbox_size <= mouse_pos[0] <= self.x + self.width + self.hitbox_size and \
#         self.y - self.hitbox_size <= mouse_pos[1] <= self.y + self.height + self.hitbox_size:
#             color = button_hover_color
#         else:
#             color = self.color if self.color else button_color

#         pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
#         text_surface = self.font.render(self.text, True, self.text_color)
#         screen.blit(text_surface, (self.x + (self.width - text_surface.get_width()) // 2, self.y + (self.height - text_surface.get_height()) // 2))

#     def is_clicked(self, event):
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             mouse_pos = pygame.mouse.get_pos()
#             if self.x - self.hitbox_size <= mouse_pos[0] <= self.x + self.width + self.hitbox_size and \
#                self.y - self.hitbox_size <= mouse_pos[1] <= self.y + self.height + self.hitbox_size:
#                 self.callback()


# # Slider class
# class Slider:
#     def __init__(self, x, y, width, height, min_value, max_value, initial_value, callback):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.min_value = min_value
#         self.max_value = max_value
#         self.value = initial_value  
#         self.callback = callback
#         self.handle_height = 20
#         self.track_thickness = self.width
#         self.is_being_interacted = False
#         self.handle_interact_color = (60, 60, 60)  # darker handle color when user is interacting with it 

#     def draw(self, screen):
#         track_color = slider_color
#         handle_color = self.handle_interact_color if self.is_being_interacted else slider_handle_color

#         pygame.draw.rect(screen, track_color, (self.x, self.y, self.track_thickness, self.height))
#         handle_y = self.y + (self.height - self.handle_height) * (1 - (self.value - self.min_value) / (self.max_value - self.min_value))
#         pygame.draw.rect(screen, handle_color, (self.x, handle_y, self.track_thickness, self.handle_height))

#     def update(self, event):
#         mouse_pos = pygame.mouse.get_pos()
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if self.x <= mouse_pos[0] <= self.x + self.track_thickness and self.y <= mouse_pos[1] <= self.y + self.height:
#                 self.is_being_interacted = True
#                 self.set_value_from_mouse(mouse_pos)
#         elif event.type == pygame.MOUSEBUTTONUP:
#             self.is_being_interacted = False
#         elif event.type == pygame.MOUSEMOTION:
#             if self.is_being_interacted:
#                 self.set_value_from_mouse(mouse_pos)

    
#     def set_value_from_mouse(self, mouse_pos):
#         relative_pos = (mouse_pos[1] - self.y) / self.height
#         new_size = 5 + (100 - 5) * (1 - relative_pos)  # use interpolation to calculate sizes along slider 
#         new_size = max(5, min(100, new_size))  # make sure value is in bounds 
#         self.value = new_size
#         self.callback(new_size)
        
#     def set_value(self, value):
#         self.value = value


# # function to interpolate points between two points
# def interpolate_points(start, end, distance):
#     x0, y0 = start
#     x1, y1 = end
#     points = []
#     dx = x1 - x0
#     dy = y1 - y0
#     length = math.sqrt(dx * dx + dy * dy)
#     num_points = max(int(length / distance), 1)
#     for i in range(num_points):
#         t = i / num_points
#         x = x0 + t * dx
#         y = y0 + t * dy
#         points.append((int(x), int(y)))
#     points.append(end)
#     return points

# # draw function using interpolation
# def draw_line(screen, color, start, end, width):
#     points = interpolate_points(start, end, 1)
#     for point in points:
#         pygame.draw.circle(screen, color, point, width // 2)

# def save_state():
#     global current_state
#     current_state = super_screen.copy()
#     undo_stack.append(current_state)
#     redo_stack.clear()  # clear redo stack when a new action is performed

# def undo():
#     global current_state
#     if len(undo_stack) > 1:
#         redo_stack.append(undo_stack.pop())  # move current state to redo stack
#         current_state = undo_stack[-1].copy()
#         super_screen.blit(current_state, (0, 0))

# def redo():
#     global current_state
#     if redo_stack:
#         current_state = redo_stack.pop()
#         undo_stack.append(current_state)
#         super_screen.blit(current_state, (0, 0))

# def clear_canvas():
#     save_state()  # save the current state before clearing
#     super_screen.fill(background_color)

# def set_pen_tool():
#     global current_tool, pen_color
#     current_tool = 'pen'
#     pen_color = pen_button.text_color  # restore the previous pen color
#     size_slider.set_value(sizes['pen'])
#     pen_button.color = button_hover_color
#     eraser_button.color = button_color

# def set_eraser_tool():
#     global current_tool, pen_color
#     current_tool = 'eraser'
#     pen_color = background_color  # set pen_color to background_color for erasing
#     size_slider.set_value(sizes['eraser'])
#     eraser_button.color = button_hover_color
#     pen_button.color = button_color


# # Function to update brush size
# def update_brush_size(new_size):
#     sizes[current_tool] = new_size  # save current tool's size 
#     if current_tool == 'pen':
#         pen_width = new_size
#     else:
#         eraser_width = new_size
#     size_slider.set_value(new_size)  # update slider's value to reflect new size

# # set pen color function 
# def set_color(color):
#     global pen_color, current_tool
#     pen_color = color
#     pen_button.text_color = color
#     current_tool = 'pen'  # switch to pen tool when color is selected
#     pen_button.color = button_color  # reset pen button color
#     eraser_button.color = button_color  # reset eraser button color

# def set_shape_tool(shape):
#     global current_tool
#     current_tool = shape
#     pen_button.color = button_color
#     eraser_button.color = button_color
#     # set behavior when shapes are selected 
#     rectangle_button.color = button_hover_color if shape == 'rectangle' else button_color
#     circle_button.color = button_hover_color if shape == 'circle' else button_color

# # button to save image as a png 
# def save_image(filename):
#     pygame.image.save(super_screen, filename)
#     print(f"Image saved as {filename}")


# # create button instances
# clear_button = Button('Clear', 10, 10, 100, 50, clear_canvas)
# pen_button = Button('Pen', 120, 10, 100, 50, set_pen_tool, text_color=pen_color, selected_color=(100, 100, 100))
# eraser_button = Button('Eraser', 230, 10, 100, 50, set_eraser_tool, selected_color=(100, 100, 100))
# save_button = Button('Save', 560, 10, 100, 50, lambda: save_image('drawing.png'))


# # create undo and redo buttons
# undo_button = Button('Undo', 340, 10, 100, 50, undo)
# redo_button = Button('Redo', 450, 10, 100, 50, redo)

# # create shape buttons 
# rectangle_button = Button('Rect', 670, 10, 100, 50, lambda: set_shape_tool('rectangle'))
# circle_button = Button('Circle', 780, 10, 100, 50, lambda: set_shape_tool('circle'))


# # create color buttons
# color_buttons = []
# color_x = 10
# for color in colors:
#     color_buttons.append(Button('', color_x, screen_height - 60, 50, 50, lambda c=color: set_color(c), color, selected_color=(max(0, color[0] - 50), max(0, color[1] - 50), max(0, color[2] - 50))))
#     color_x += 60
    
# # slider height and positioning
# slider_width = 20
# slider_height = int(screen_height * 0.7)
# slider_x = 10
# slider_y = (screen_height - slider_height) // 2

# # create slider instance 
# size_slider = Slider(slider_x, slider_y, slider_width, slider_height, 5, 100, 10, update_brush_size)

# # set initial tool mode and sizes
# sizes = {'pen': 5, 'eraser': 20, 'rectangle': 5, 'circle': 5}
# pen_width = sizes['pen']
# eraser_width = sizes['eraser']

# # save initial blank state
# save_state()

# # main loop
# running = True
# drawing = False
# last_pos = None
# color_button_active = False
# stroke_made = False  # flag to track if stroke was made 

# start_pos = None

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             mouse_pos = pygame.mouse.get_pos()
#             if (slider_x <= mouse_pos[0] <= slider_x + size_slider.track_thickness and
#                 slider_y <= mouse_pos[1] <= slider_y + slider_height):
#                 size_slider.update(event)
#                 drawing = False
#             else:
#                 color_button_active = False
#                 for button in color_buttons:
#                     if (button.x - button.hitbox_size <= mouse_pos[0] <= button.x + button.width + button.hitbox_size and
#                         button.y - button.hitbox_size <= mouse_pos[1] <= button.y + button.height + button.hitbox_size):
#                         color_button_active = True
#                         button.is_clicked(event)
#                         drawing = False
#                         break

#                 if not color_button_active:
#                     drawing = True
#                     stroke_made = False  # reset stroke_made flag
#                     start_pos = event.pos[0] * 2, event.pos[1] * 2
#                     last_pos = start_pos
#         elif event.type == pygame.MOUSEBUTTONUP:
#             size_slider.update(event)
#             if drawing and stroke_made:
#                 save_state()  # save state after finishing a stroke or shape
#             drawing = False
#             color_button_active = False
#             start_pos = None
#         elif event.type == pygame.MOUSEMOTION:
#             if drawing:
#                 current_pos = event.pos[0] * 2, event.pos[1] * 2
#                 current_width = sizes[current_tool] * 2
#                 current_color = background_color if current_tool == 'eraser' else pen_color
#                 if current_tool == 'pen' or current_tool == 'eraser':
#                     draw_line(super_screen, current_color, last_pos, current_pos, current_width)
#                 elif current_tool == 'rectangle' and start_pos:
#                     super_screen.blit(current_state, (0, 0))  # restore the screen to the state before drawing the shape
#                     pygame.draw.rect(super_screen, current_color, (start_pos[0], start_pos[1], current_pos[0] - start_pos[0], current_pos[1] - start_pos[1]), current_width // 2)
#                 elif current_tool == 'circle' and start_pos:
#                     super_screen.blit(current_state, (0, 0))  # restore the screen to the state before drawing the shape
#                     radius = int(math.sqrt((current_pos[0] - start_pos[0]) ** 2 + (current_pos[1] - start_pos[1]) ** 2))
#                     pygame.draw.circle(super_screen, current_color, start_pos, radius, current_width // 2)
#                 last_pos = current_pos
#                 stroke_made = True  # set stroke_made flag
#             else:
#                 size_slider.update(event)  # update slider while moving the mouse

#         # check if the buttons are clicked
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if clear_button.is_clicked(event):
#                 save_state()  # save state before clearing
#                 clear_canvas()
#             elif undo_button.is_clicked(event):
#                 undo()
#             elif redo_button.is_clicked(event):
#                 redo()
#             elif save_button.is_clicked(event):
#                 save_image('drawing.png')  # save the current drawing
#             else:
#                 pen_button.is_clicked(event)
#                 eraser_button.is_clicked(event)
#                 rectangle_button.is_clicked(event)
#                 circle_button.is_clicked(event)
#                 for button in color_buttons:
#                     button.is_clicked(event)

#     # clear screen before drawing
#     screen.fill(background_color)

#     # downscale supersampled image
#     pygame.transform.scale(super_screen, (screen_width, screen_height), screen)

#     # draw the buttons
#     clear_button.draw(screen)
#     pen_button.draw(screen, is_selected=(current_tool == 'pen'))
#     eraser_button.draw(screen, is_selected=(current_tool == 'eraser'))
#     undo_button.draw(screen)
#     redo_button.draw(screen)
#     save_button.draw(screen)  # draw save button
#     rectangle_button.draw(screen, is_selected=(current_tool == 'rectangle'))
#     circle_button.draw(screen, is_selected=(current_tool == 'circle'))
#     for button in color_buttons:
#         button.draw(screen, is_selected=(pen_color == button.color and current_tool == 'pen'))

#     # draw the slider
#     size_slider.draw(screen)

#     # update display
#     pygame.display.flip()

# pygame.quit()
