# gui.py
from button import Button
from slider import Slider
from state import sizes, pen_width, eraser_width, current_tool
from config import COLORS, SCREEN_HEIGHT, SCREEN_WIDTH, BACKGROUND_COLOR
from utils import set_pen_tool, set_eraser_tool, set_color, update_brush_size, clear_canvas

def initialize_gui():
    global clear_button, pen_button, eraser_button, color_buttons, size_slider

    clear_button = Button('Clear', 10, 10, 100, 50, clear_canvas)
    pen_button = Button('Pen', 120, 10, 100, 50, set_pen_tool, text_color=(0, 0, 0), selected_color=(100, 100, 100))
    eraser_button = Button('Eraser', 230, 10, 100, 50, set_eraser_tool, selected_color=(100, 100, 100))

    color_buttons = []
    color_x = 10
    for color in COLORS:
        color_buttons.append(Button('', color_x, SCREEN_HEIGHT - 60, 50, 50, lambda c=color: set_color(c), color))
        color_x += 60

    slider_width = 20
    slider_height = int(SCREEN_HEIGHT * 0.7)
    slider_x = 10
    slider_y = (SCREEN_HEIGHT - slider_height) // 2

    size_slider = Slider(slider_x, slider_y, slider_width, slider_height, 5, 100, 10, update_brush_size)
