# utils.py
from gui import size_slider, pen_button, eraser_button
from state import super_screen, sizes, pen_width, eraser_width, current_tool
from config import ERASER_COLOR, BACKGROUND_COLOR

# Clear canvas function
def clear_canvas():
    super_screen.fill(BACKGROUND_COLOR)

# Set pen tool function
def set_pen_tool():
    global pen_color, current_tool
    pen_color = (0, 0, 0)  # Pen color
    current_tool = 'pen'
    size_slider.set_value(sizes['pen'])

def set_eraser_tool():
    global pen_color, current_tool
    pen_color = ERASER_COLOR  # Eraser color
    current_tool = 'eraser'
    size_slider.set_value(sizes['eraser'])

# Function to update brush size
def update_brush_size(new_size):
    sizes[current_tool] = new_size
    if current_tool == 'pen':
        pen_width = new_size
    else:
        eraser_width = new_size
    size_slider.set_value(new_size)

# Set pen color function
def set_color(color):
    global pen_color
    pen_color = color
    pen_button.text_color = color
