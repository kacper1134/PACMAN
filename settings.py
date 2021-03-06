from structures.vector import Vector2Dim
import os

# Game Basic Settings
TILE_SIZE = 16
TILE_HEIGHT = TILE_SIZE
TILE_WIDTH = TILE_SIZE

ROWS = 36
COLS = 28
WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE
SCREEN_SIZE = (WIDTH, HEIGHT)

FPS = 120

# Movement
UP = Vector2Dim(y=-1)
DOWN = Vector2Dim(y=1)
LEFT = Vector2Dim(x=-1)
RIGHT = Vector2Dim(x=1)
STOP = Vector2Dim()

CHARACTER_SPEED = 100
MAXIMUM_GAME_SPEED = 2
NEXT_LEVEL_SPEED_MULTIPLICATION = 1.02


# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

RED = (255, 0, 0)
PINK = (255, 100, 150)
TEAL = (100, 255, 255)
ORANGE = (230, 190, 40)

TRANSPARENT_COLOR = (255, 0, 255)

# Maze symbols
NODE_SYMBOL = "+"
EMPTY_SPACE_SYMBOL = "0"
VERTICAL_PATH_SYMBOL = "|"
HORIZONTAL_PATH_SYMBOL = "-"

HOUSE_SYMBOL = "H"
GHOST_SPAWN_SYMBOL = "S"

PACMAN_START_NODE = "P"
BLINKY_START_NODE = "B"
INKY_START_NODE = "I"
CLYDE_START_NODE = "C"

FRUIT_SYMBOL = "F"

# Pellets symbols
PELLET_SYMBOL = "p"
POWER_PELLET_SYMBOL = "P"

# Ghost settings
CHASE_MODE = "CHASE"
SCATTER_MODE = "SCATTER"
SPAWN_MODE = "SPAWN"
FREIGHT_MODE = "FREIGHT"
GUIDE_MODE = "GUIDE"
GHOST_HOUSE = [[EMPTY_SPACE_SYMBOL, EMPTY_SPACE_SYMBOL, BLINKY_START_NODE, EMPTY_SPACE_SYMBOL, EMPTY_SPACE_SYMBOL],
               [EMPTY_SPACE_SYMBOL, EMPTY_SPACE_SYMBOL, VERTICAL_PATH_SYMBOL, EMPTY_SPACE_SYMBOL, EMPTY_SPACE_SYMBOL],
               [NODE_SYMBOL, EMPTY_SPACE_SYMBOL, VERTICAL_PATH_SYMBOL, EMPTY_SPACE_SYMBOL, NODE_SYMBOL],
               [INKY_START_NODE, HORIZONTAL_PATH_SYMBOL, GHOST_SPAWN_SYMBOL, HORIZONTAL_PATH_SYMBOL, CLYDE_START_NODE],
               [NODE_SYMBOL, EMPTY_SPACE_SYMBOL, EMPTY_SPACE_SYMBOL, EMPTY_SPACE_SYMBOL, NODE_SYMBOL]]

GHOST_FREIGHT_MODE_MULTIPLIER = 0.98
GHOST_FREIGHT_MODE_TIME = 7

# Pause settings
PAUSE_CLEAR = "clear pause"
PAUSE_DIE = "die pause"
PAUSE_GHOST = "ghost pause"

# Font directory
FONT_DIRECTORY = os.path.join(os.path.dirname(__file__), "fonts")
FONT_FILE = "PressStart2P-Regular.ttf"

# Fonts
FONT_SIZE = 16

# Image directory
IMAGE_DIRECTORY = os.path.join(os.path.dirname(__file__), "img")
SPRITE_SHEET_FILE = "spritesheet.png"

# Images
IMAGE_SIZE = 32

# Animation
PACMAN_ANIMATION_SPEED = 15
PACMAN_ANIMATION_DEATH_SPEED = 8
GHOST_ANIMATION_SPEED = 10
LOOP_ANIMATION_TYPE = "loop"
ONCE_ANIMATION_TYPE = "once"
STATIC_ANIMATION_TYPE = "static"

# Maze
NUMBER_OF_MAZE_FRAGMENTS = 11
MAZE_DIRECTORY = os.path.join(os.path.dirname(__file__), "mazes")
FLASH_TIME = 0.25

# Sound directory
SOUND_DIRECTORY = os.path.join(os.path.dirname(__file__), "sound")
BEGINNING_SOUND_FILE = "pacman_beginning.wav"
CHOMP_SOUND_FILE = "pacman_chomp.wav"
DEATH_SOUND_FILE = "pacman_death.wav"
EAT_FRUIT_SOUND_FILE = "pacman_eatfruit.wav"
EAT_GHOST_SOUND_FILE = "pacman_eatghost.wav"
BACKGROUND_SOUND_FILE = "siren_1.wav"
