import pygame
import random

# intialize Pygame
pygame.init()

# get user screen dimension to make window 80% of the dimension
info = pygame.display.Info()
screen_width = int(info.current_w * 0.8)
screen_height = int(info.current_h * 0.8)

# set up display 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pycasso")

# set colors
background_color = (255, 255, 255)  # White
drawing_color = (0, 0, 0)  # Black

# set brush size
brush_size = 10

# make canvas
canvas = pygame.Surface((screen_width, screen_height))
canvas.fill(background_color)

# running
running = True
drawing = False

# main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
        elif event.type == pygame.MOUSEMOTION and drawing:
            mouse_x, mouse_y = event.pos
            pygame.draw.rect(canvas, drawing_color, (mouse_x, mouse_y, brush_size, brush_size))

    # fill screen with background color
    screen.fill(background_color)
    
    # blit canvas onto screen
    screen.blit(canvas, (0, 0))

    # update display
    pygame.display.flip()

# quit Pygame
pygame.quit()
