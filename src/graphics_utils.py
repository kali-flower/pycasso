import math
import pygame

# function to interpolate points between two points
def interpolate_points(start, end, distance):
    x0, y0 = start
    x1, y1 = end
    points = []
    dx = x1 - x0
    dy = y1 - y0
    length = math.hypot(dx, dy)
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
    scaled_width = width * 2  # scale the width according to the supersampled resolution
    for point in points:
        pygame.draw.circle(screen, color, point, scaled_width // 2)


# interpolate from a to b by percentage amt.
# amt=0 results in a
# amt=1 results in b
def mix(a, b, amt):
    return a + (b-a)*amt

def clamp(val, minVal, maxVal):
    if val < minVal: return minVal
    if val > maxVal: return maxVal
    return val

# point is tuple (x,y)
# region is tuple (x1,y1,x2,y2) OR (x1,y1,width,height)
#                   'corners'            'size'
def point_in_box(point, region, mode='corners'):
    x,y = point

    if mode == 'corners':
        x1,y1,x2,y2 = region
    elif mode == 'size':
        x1,y1,width,height = region
        x2,y2 = x1 + width, y1 + height
    else:
        raise ValueError(f"Invalid in_bounds mode: \"{mode}\"")

    # make x1,y1 top left and x2,y2 bottom right
    if x1 > x2: x1,x2 = x2,x1
    if y1 > y2: y1,y2 = y2,y1
    
    return x1 <= x <= x2 and y1 <= y <= y2