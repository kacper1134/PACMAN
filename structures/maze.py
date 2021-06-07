import pygame as pg
from settings import *
import random


class Maze:
    def __init__(self, game):
        self.game = game
        self.sprite_sheet = self.game.sprite_sheet
        self.maze_fragments_info = None
        self.maze_fragments_rotation_info = None
        self.images = []
        self.flash_images = []
        self.image_row = 16

        self.timer = 0
        self.normal_background = None
        self.flash_background = None
        self.normal_view = True

    def get_maze_images(self, row_number=0):
        self.images = []
        self.flash_images = []

        maze_color_number = random.randint(0, 4)

        for i in range(NUMBER_OF_MAZE_FRAGMENTS):
            self.images.append(self.sprite_sheet.get_image_from_sheet(i, self.image_row + row_number +
                                                                      maze_color_number, TILE_WIDTH, TILE_HEIGHT))
            self.flash_images.append(self.sprite_sheet.get_image_from_sheet(i + NUMBER_OF_MAZE_FRAGMENTS, self.image_row
                                                                            + row_number + maze_color_number,
                                                                            TILE_WIDTH, TILE_HEIGHT))

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
                    flash_image = self.rotate_maze_fragment(self.flash_images[int(value)], int(rotation_value))
                    self.game.background.blit(image, (x, y))
                    self.game.flash_background.blit(flash_image, (x, y))
                elif value == "=":
                    self.game.background.blit(self.images[10], (x, y))
                    self.game.flash_background.blit(self.flash_images[10], (x, y))

        self.normal_background = self.game.background
        self.flash_background = self.game.flash_background

    def rotate_maze_fragment(self, image, value):
        return pg.transform.rotate(image, value * 90)

    def read_maze_file(self, maze_file):
        with open(maze_file, "r") as f:
            lines = [line.strip() for line in f]
            return [line.split(" ") for line in lines]

    def reset_maze(self):
        self.game.background = self.normal_background
        self.timer = 0

    def flash_maze(self):
        self.timer += self.game.dt
        if self.timer >= FLASH_TIME:
            self.timer = 0
            self.normal_view = not self.normal_view

            if self.normal_view:
                self.game.background = self.normal_background
            else:
                self.game.background = self.flash_background
