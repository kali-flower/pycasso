import pygame
import tkinter as tk
from tkinter import simpledialog

import math

from collections import deque
import copy

# self imports
from config import *
from graphics_utils import *
from widgets import Button, Slider, Canvas, active_widgets, ColorIndicator

# initialize pygame
pygame.init()

# original window size based on user screen
info = pygame.display.Info()
screen_width = int(info.current_w * 0.8)
screen_height = int(info.current_h * 0.8)

# supersampled window size --> 2x original
SUPER_WIDTH, SUPER_HEIGHT = screen_width * 2, screen_height * 2

# initialize display for supersampling
super_screen = pygame.Surface((SUPER_WIDTH, SUPER_HEIGHT))
super_screen.fill(background_color)  # clear supersampled screen

# initialize display window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pycasso") # title :D

def set_pen_tool():
    global canvas
    canvas.curr_tool = 'pen'
    size_slider.set_value(canvas.tool_sizes['pen'])
    pen_button.color = button_selected_color
    eraser_button.color = button_color
    rectangle_button.color = button_color
    circle_button.color = button_color

def set_eraser_tool():
    global canvas
    canvas.curr_tool = 'eraser'
    size_slider.set_value(canvas.tool_sizes['eraser'])
    eraser_button.color = button_selected_color
    pen_button.color = button_color
    rectangle_button.color = button_color
    circle_button.color = button_color


# Function to update brush size
def update_brush_size(new_size):
    global canvas
    canvas.set_curr_tool_size(round(new_size))
    size_slider.set_value(new_size)  # update slider's value to reflect new size
    # canvas.is_being_interacted = False    # probably not needed

# set pen color function 
def set_color(color):
    global canvas
    canvas.pen_color = color
    color_indicator.update_color(color)  # updates the color indicator
    # reset button colors
    pen_button.color = button_color  
    eraser_button.color = button_color
    rectangle_button.color = button_color
    circle_button.color = button_color

# function to set shape tool
def set_shape_tool(shape):
    global canvas
    canvas.curr_tool = shape
    pen_button.color = button_color
    eraser_button.color = button_color
    rectangle_button.color = button_selected_color if shape == 'rectangle' else button_color
    circle_button.color = button_selected_color if shape == 'circle' else button_color

# button to save image as a png 
def save_image():
    root = tk.Tk()
    root.withdraw()  # hide the root window
    filename = simpledialog.askstring("Save Image", "Enter filename (without extension):")
    
    if filename:  # only save if a filename was provided
        filename = filename + ".png"
        pygame.image.save(super_screen, filename)
        print(f"Image saved as {filename}")
    else:
        print("Save cancelled.")



# create the canvas
canvas = Canvas(super_screen)
canvas.on_stroke_finish = canvas.save_state
canvas.priority = 1 # Process canvas after everything else
canvas.save_state() # Save initial blank state

# create button instances
clear_button = Button('Clear', 10, 10, 100, 50, canvas.clear)
pen_button = Button('Pen', 120, 10, 100, 50, set_pen_tool, text_color=initial_pen_color, selected_color=(100, 100, 100))
eraser_button = Button('Eraser', 230, 10, 100, 50, set_eraser_tool, selected_color=(100, 100, 100))
save_button = Button('Save', 560, 10, 100, 50, save_image)


# create undo and redo buttons
undo_button = Button('Undo', 340, 10, 100, 50, canvas.undo)
redo_button = Button('Redo', 450, 10, 100, 50, canvas.redo)

# create shape buttons 
rectangle_button = Button('Rect', 670, 10, 100, 50, lambda: set_shape_tool('rectangle'), selected_color=button_selected_color)
circle_button = Button('Circle', 780, 10, 100, 50, lambda: set_shape_tool('circle'), selected_color=button_selected_color)

# create color indicator instance
color_indicator = ColorIndicator(900, 35, 15) 


# create color buttons
color_buttons = []
color_x = 10
for color in colors:
    color_buttons.append(Button('', color_x, screen_height - 60, 50, 50, lambda c=color: set_color(c), color, selected_color=(max(0, color[0] - 50), max(0, color[1] - 50), max(0, color[2] - 50))))
    color_x += 60
  
# slider height and positioning
slider_width = 20
slider_height = int(screen_height * 0.7)
slider_x = 10
slider_y = (screen_height - slider_height) // 2

# create slider instance 
size_slider = Slider(slider_x, slider_y, slider_width, slider_height, 5, 100, 10,
                     lambda percentage: update_brush_size(mix(5,100,percentage)))

def sorted_widgets():
    return sorted(active_widgets, key=lambda w: w.priority)

# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        for widget in sorted_widgets():
            claimed = widget.handle_event(event)
            if claimed:
                break

    # clear screen before drawing
    screen.fill(background_color)

    # downscale supersampled image
    pygame.transform.scale(super_screen, (screen_width, screen_height), screen)

    # Update button states
    pen_button.is_selected = (canvas.curr_tool == 'pen')
    eraser_button.is_selected = (canvas.curr_tool == 'eraser')
    rectangle_button.is_selected = (canvas.curr_tool == 'rectangle')
    circle_button.is_selected = (canvas.curr_tool == 'circle')
    
    for button in color_buttons:
        button.is_selected = (canvas.pen_color == button.color and canvas.curr_tool == 'pen')

    # draw widgets
    for widget in active_widgets:
        widget.draw(screen)

    # Draw the preview outline
    canvas.draw_preview_outline(screen)

    color_indicator.draw(screen)

    # update display
    pygame.display.flip()

pygame.quit()