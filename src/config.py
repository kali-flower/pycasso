import pygame

# original window size based on user screen
INFO = pygame.display.Info()
SCREEN_WIDTH = int(INFO.current_w * 0.8)
SCREEN_HEIGHT = int(INFO.current_h * 0.8)

# supersampled window size --> 2x original
SUPER_WIDTH, SUPER_HEIGHT = SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2

# colors
BACKGROUND_COLOR = (255, 255, 255)
PEN_COLOR = (0, 0, 0)
ERASER_COLOR = BACKGROUND_COLOR
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (150, 150, 150)
BUTTON_TEXT_COLOR = (0, 0, 0)
SLIDER_COLOR = (180, 180, 180)
SLIDER_HANDLE_COLOR = (100, 100, 100)

# more pen colors! :D
COLORS = [
    (0, 0, 0),        # black
    (255, 142, 156),  # red
    (255, 185, 147),  # orange
    (243, 238, 155),  # yellow
    (171, 232, 162),  # green
    (153, 214, 234),  # cyan
    (138, 171, 239),  # blue
    (178, 160, 255),  # violet
    (255, 169, 216)   # pink
]
