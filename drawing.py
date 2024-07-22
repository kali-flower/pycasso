import math
import pygame

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