import pygame
import math

# initialize Pygame
pygame.init()

# get user screen dimensions, make window 80% of each  
info = pygame.display.Info()
screen_width = int(info.current_w * 0.8)
screen_height = int(info.current_h * 0.8)

# set up display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Drawing App")

# set colors 
background_color = (255, 255, 255)  # white
drawing_color = (0, 0, 0)  # black

# set brush size 
brush_size = 10

# create canvas 
canvas = pygame.Surface((screen_width, screen_height))
canvas.fill(background_color)

# running
running = True
drawing = False

strokes = []
last_pos = None

# interpolate points between two points 
def interpolate_points(start, end, distance): 
    # get x and y coordinates of start and end points 
    x0, y0 = start
    x1, y1 = end
    points = []

    # difference in x and y between start and end points 
    dx = x1 - x0
    dy = y1 - y0
    # total distance between start and end points using Pythagorean theorem 
    length = math.sqrt(dx * dx + dy * dy) 

    # find how many points needed based on total distance 
    num_points = max(int(length / distance), 1)

    # loop to create each point  
    for i in range(num_points):
        t = i / num_points # fraction of the way from start to end 
        x = x0 + t * dx # interpolated x coordinate 
        y = y0 + t * dy # interpolated y coordinate 
        points.append((int(x), int(y)))
    points.append(end)  # include end point 
    return points

# main loop 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            last_pos = event.pos
            strokes.append([event.pos])  # start a new stroke
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            last_pos = None
        elif event.type == pygame.MOUSEMOTION and drawing:
            current_pos = event.pos
            if last_pos is not None:
                # interpolate points between last_pos and current_pos
                points = interpolate_points(last_pos, current_pos, brush_size / 2)
                strokes[-1].extend(points)  # add interpolated points to the current stroke
            last_pos = current_pos

    # clear canvas and redraw strokes 
    canvas.fill(background_color)
    for stroke in strokes:
        if len(stroke) > 1:
            for i in range(len(stroke) - 1):
                pygame.draw.line(canvas, drawing_color, stroke[i], stroke[i + 1], brush_size)
                
    # fill background 
    screen.fill(background_color)

    # blit canvas surface onto screen 
    screen.blit(canvas, (0, 0))

    # update display
    pygame.display.flip()

# quit Pygame
pygame.quit()




import pygame
import math

# initialize Pygame
pygame.init()

# get user screen dimensions, make window 80% of each   
info = pygame.display.Info()
screen_width = int(info.current_w * 0.8)
screen_height = int(info.current_h * 0.8)

# set up display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pycasso")

# set colors 
background_color = (255, 255, 255)  # white
drawing_color = (0, 0, 0)  # black

# set brush size 
brush_size = 10

# create canvas 
canvas = pygame.Surface((screen_width, screen_height))
canvas.fill(background_color)

# running
running = True
drawing = False

strokes = []
last_pos = None

# compute points along a cubic bezier curve 
def bezier_curve(p0, p1, p2, p3, num_points):
    points = []
    if num_points <= 0: # check edge cases and return early 
        return points
    for t in range(num_points + 1):
        t /= num_points
        x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
        y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
        points.append((int(x), int(y)))
    return points


# interpolate points between two points 
def interpolate_points(start, end, distance): 
    # get x and y coordinates of start and end points 
    x0, y0 = start
    x1, y1 = end
    points = []

    # difference in x and y between start and end points 
    dx = x1 - x0
    dy = y1 - y0
    # total distance between start and end points using Pythagorean theorem 
    length = math.sqrt(dx * dx + dy * dy) 

    # find how many points needed based on total distance 
    num_points = max(int(length / distance), 1)

    # loop to create each point  
    for i in range(num_points):
        t = i / num_points # fraction of the way from start to end 
        x = x0 + t * dx # interpolated x coordinate 
        y = y0 + t * dy # interpolated y coordinate 
        points.append((int(x), int(y)))
    points.append(end)  # include end point 
    return points

# main loop 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            last_pos = event.pos
            strokes.append([event.pos])  # start a new stroke
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            last_pos = None
        elif event.type == pygame.MOUSEMOTION and drawing:
            current_pos = event.pos
            if last_pos is not None:
                if len(strokes[-1]) >= 3:
                    # use the last three points to create bezier curve control points
                    p0 = strokes[-1][-3]
                    p1 = strokes[-1][-2]
                    p2 = last_pos
                    p3 = current_pos
                    # increase number of points sampled along the curve
                    num_points = max(int(math.hypot(current_pos[0] - last_pos[0], current_pos[1] - last_pos[1]) / (brush_size / 4)), 1)
                    points = bezier_curve(p0, p1, p2, p3, num_points)  # use increased num_points
                else:
                    # not enough points for bezier curve --> use a simple line
                    points = interpolate_points(last_pos, current_pos, brush_size / 4)
                strokes[-1].extend(points)  # add interpolated points to the current stroke
            last_pos = current_pos

    # clear canvas and redraw strokes 
    canvas.fill(background_color)
    for stroke in strokes:
        if len(stroke) > 1:
            for i in range(len(stroke) - 1):
                pygame.draw.line(canvas, drawing_color, stroke[i], stroke[i + 1], brush_size)
                
    # fill background 
    screen.fill(background_color)

    # blit canvas surface onto screen 
    screen.blit(canvas, (0, 0))

    # update display
    pygame.display.flip()

# quit pygame
pygame.quit()
