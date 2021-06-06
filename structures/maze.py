import pygame as pg
from settings import *


class Maze:
    def __init__(self, game):
        self.game = game
        self.sprite_sheet = self.game.sprite_sheet
        self.maze_fragments_info = None
        self.maze_fragments_rotation_info = None
        self.images = []
        self.flash_images = []
        self.image_row = 16

    def get_maze_images(self, row_number=0):
        self.images = []
        for i in range(NUMBER_OF_MAZE_FRAGMENTS):
            self.images.append(self.sprite_sheet.get_image_from_sheet(i, self.image_row + row_number, TILE_WIDTH,
                                                                      TILE_SIZE))

    def get_maze(self, maze_name):
        maze_name = os.path.join(MAZE_DIRECTORY, maze_name)
        self.maze_fragments_info = self.read_maze_file(maze_name + "_fragments.txt")
        self.maze_fragments_rotation_info = self.read_maze_file(maze_name + "_fragments_rotation.txt")

    def create_maze(self, row_number=0):
        self.get_maze_images(row_number)

        number_of_rows = len(self.maze_fragments_info)
        number_of_cols = len(self.maze_fragments_info[0])

        for row in range(number_of_rows):
            for col in range(number_of_cols):
                x = col * TILE_WIDTH
                y = row * TILE_HEIGHT

                value = self.maze_fragments_info[row][col]
                if value.isdecimal():
                    rotation_value = self.maze_fragments_rotation_info[row][col]
                    image = self.rotate_maze_fragment(self.images[int(value)], int(rotation_value))
                    self.game.background.blit(image, (x, y))
                elif value == "=":
                    self.game.background.blit(self.images[10], (x, y))

    def rotate_maze_fragment(self, image, value):
        return pg.transform.rotate(image, value * 90)

    def read_maze_file(self, maze_file):
        with open(maze_file, "r") as f:
            lines = [line.strip() for line in f]
            return [line.split(" ") for line in lines]

