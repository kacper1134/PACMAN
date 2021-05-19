from structures.vector import Vector2Dim

# Game Basic Settings
TILE_SIZE = 16
TILE_HEIGHT = TILE_SIZE
TILE_WIDTH = TILE_SIZE

ROWS = 36
COLS = 28
WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE
SCREEN_SIZE = (WIDTH, HEIGHT)

# Movement
UP = Vector2Dim(y=-1)
DOWN = Vector2Dim(y=1)
LEFT = Vector2Dim(x=-1)
RIGHT = Vector2Dim(x=1)
STOP = Vector2Dim()

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
