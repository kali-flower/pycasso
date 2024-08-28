import pygame
import numpy as np
import asyncio
import websockets
from collections import deque
import json

websocket = None
shutdown_event = asyncio.Event()
draw_inbox  = deque()
draw_outbox = deque()
async def ws_connect(uri):
    global websocket, shutdown_event, draw_inbox, draw_outbox
    async with websockets.connect(uri) as ws:
        websocket = ws
        while not shutdown_event.is_set():
            try:
                while draw_outbox:
                    val = draw_outbox.popleft()
                    await ws.send(json.dumps(val))

                message = await asyncio.wait_for(ws.recv(), timeout=1)
                draw_inbox.append(json.loads(message))
            except: continue

pen_color = (0,0,0)
pen_width = 15

pygame.init()
screen = pygame.display.set_mode((800, 600))
screen.fill((255,255,255))

def clamp(val, minVal, maxVal):
    if val < minVal: return minVal
    if val > maxVal: return maxVal
    return val

def custom_line(p1, p2):
    global screen
    x1,y1 = p1
    x2,y2 = p2

    # bounds
    x_lo = min(x1,x2) - pen_width
    x_hi = max(x1,x2) + pen_width
    y_lo = min(y1,y2) - pen_width
    y_hi = max(y1,y2) + pen_width

    # doing logic from https://iquilezles.org/articles/distfunctions2d/ - search "Segment - exact" or "sdSegment" from ^
    vecs = np.dstack(np.mgrid[x_lo:x_hi+1:1, y_lo:y_hi+1:1])
    pa = vecs - p1
    ba = np.array(p2) - np.array(p1)
    dot_paba = np.sum(pa * ba, axis=-1)
    dot_baba = np.sum(np.square(ba), axis=-1)
    divdots = dot_paba / dot_baba
    h = np.clip(divdots, 0, 1)
    h = np.dstack((h,h))

    delta = pa - ba*h
    sdf_vals = np.hypot(delta[:,:,0], delta[:,:,1]) - pen_width

    # convert sdf values to an alpha mask.
    sdf_vals = 255 * (1 - np.clip(sdf_vals, 0, 1))
    sdf_vals = sdf_vals.astype(np.uint8)
    
    surf = pygame.Surface(sdf_vals.shape, pygame.SRCALPHA, 32)  # Pygame surface with alpha channel, black background by default
    pygame.surfarray.pixels_alpha(surf)[:] = sdf_vals
    screen.blit(surf, (x_lo,y_lo))

class Canvas:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

canvas = Canvas(paint_active=False, last_pos=None)

# return false if quitting Pygame
def event_loop():
    global screen, canvas

    while draw_inbox:
        x1,y1,x2,y2 = draw_inbox.popleft()
        custom_line((x1,y1),(x2,y2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            canvas.paint_active = True
            canvas.last_pos = event.pos
            pygame.draw.circle(screen, pen_color, event.pos, pen_width)
        elif event.type == pygame.MOUSEBUTTONUP:
            canvas.paint_active = False
            canvas.last_pos = None
        elif event.type == pygame.MOUSEMOTION:
            if canvas.paint_active:
                custom_line(canvas.last_pos, event.pos)
                draw_outbox.append([*canvas.last_pos, *event.pos])
                canvas.last_pos = event.pos
    
    pygame.display.flip()
    return True

async def run_game():
    while event_loop():
        await asyncio.sleep(0.001) # give websocket chance to run 
    pygame.quit()
    shutdown_event.set()

async def main():
    game_task = asyncio.create_task(run_game())
    ws_task   = asyncio.create_task(ws_connect("ws://localhost:8000"))
    # ws_task   = asyncio.create_task(ws_connect("ws://1.2.3.4:8000"))
    await asyncio.gather(game_task, ws_task)

asyncio.run(main())