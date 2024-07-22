import pygame

pygame.init()


from gui import * # Import GUI initialization
from utils import *
from state import *
from drawing import *


# Original window size based on user screen
info = pygame.display.Info()
screen_width = int(info.current_w * 0.8)
screen_height = int(info.current_h * 0.8)

# Colors
background_color = (255, 255, 255)

# Supersampled window size --> 2x original
SUPER_WIDTH, SUPER_HEIGHT = screen_width * 2, screen_height * 2

# Initialize display for supersampling
super_screen = pygame.Surface((SUPER_WIDTH, SUPER_HEIGHT))
super_screen.fill(background_color)  # Clear supersampled screen

# Initialize display window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pycasso")  # Title

# Initialize GUI components
initialize_gui()

# Set initial tool mode and sizes
sizes = {'pen': 10, 'eraser': 10}
pen_width = sizes['pen']
eraser_width = sizes['eraser']

# Main loop
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
            if (size_slider.x <= mouse_pos[0] <= size_slider.x + size_slider.track_thickness and
                size_slider.y <= mouse_pos[1] <= size_slider.y + size_slider.height):
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
                size_slider.update(event)  # Update slider while moving the mouse

        # Check if the buttons are clicked
        clear_button.is_clicked(event)
        pen_button.is_clicked(event)
        eraser_button.is_clicked(event)
        for button in color_buttons:
            button.is_clicked(event)

    # Clear screen before drawing
    screen.fill(background_color)

    # Downscale supersampled image
    pygame.transform.scale(super_screen, (screen_width, screen_height), screen)

    # Draw the buttons
    clear_button.draw(screen)
    pen_button.draw(screen, is_selected=(current_tool == 'pen'))
    eraser_button.draw(screen, is_selected=(current_tool == 'eraser'))
    for button in color_buttons:
        button.draw(screen)

    # Draw the slider
    size_slider.draw(screen)

    # Update display
    pygame.display.flip()

pygame.quit()
