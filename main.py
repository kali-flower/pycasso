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

# supersampled window size --> 4x original 
SUPER_WIDTH, SUPER_HEIGHT = screen_width * 2, screen_height * 2

# initialize display for supersampling
super_screen = pygame.Surface((SUPER_WIDTH, SUPER_HEIGHT))
super_screen.fill(background_color)  # clear supersampled screen

# initialize display window
screen = pygame.display.set_mode((screen_width, screen_height))

# function to interpolate points between two points
def interpolate_points(start, end, distance):
    x0, y0 = start
    x1, y1 = end
    points = []
    dx = x1 - x0
    dy = y1 - y0
    length = math.sqrt(dx * dx + dy * dy)
    num_points = max(int(length / distance), 1)  # make sure at least 1 point is generated
    for i in range(num_points):
        t = i / num_points
        x = x0 + t * dx
        y = y0 + t * dy
        points.append((int(x), int(y)))
    points.append(end)  # include end point
    return points

# draw function using interpolation
def draw_line(screen, color, start, end, width):
    points = interpolate_points(start, end, 1)
    for point in points:
        pygame.draw.circle(screen, color, point, width // 2)

# main loop
running = True
drawing = False
last_pos = None
width = 4

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            last_pos = event.pos[0] * 2, event.pos[1] * 2
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                current_pos = event.pos[0] * 2, event.pos[1] * 2
                draw_line(super_screen, pen_color, last_pos, current_pos, width * 2)
                last_pos = current_pos

    # clear screen before drawing
    screen.fill(background_color)

    # downscale supersampled image
    pygame.transform.scale(super_screen, (screen_width, screen_height), screen)

    # update display
    pygame.display.flip()

pygame.quit()
