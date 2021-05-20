import pygame as pg
from structures.vector import Vector2Dim
from settings import *


class Pellet:
    def __init__(self, x, y):
        self.name = "pellet"
        self.position = Vector2Dim(x, y)
        self.color = WHITE
        self.radius = 4
        self.points = 10
        self.visible = True

    def draw(self, screen):
        if self.visible:
            position = self.position.to_int()
            pg.draw.circle(screen, self.color, position, self.radius)


class PowerPellet(Pellet):
    def __init__(self, x, y):
        Pellet.__init__(self, x, y)
        self.name = "powerpellet"
        self.radius = 8
        self.points = 50
        self.blink_time = 0.2
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.blink_time:
            self.visible = not self.visible
            self.timer = 0


class PelletGroup:
    def __init__(self, pellets_file):
        self.pellets = []
        self.power_pellets = []
        self.create_pellets(pellets_file)

    def update(self, dt):
        for power_pellet in self.power_pellets:
            power_pellet.update(dt)

    def create_pellets(self, pellets_file):
        grid = self.read_pellets_file(pellets_file)
        number_of_rows = len(grid)
        number_of_cols = len(grid[0])

        for row in range(number_of_rows):
            for col in range(number_of_cols):
                if grid[row][col] == PELLET_SYMBOL:
                    self.pellets.append(Pellet(col * TILE_WIDTH, row * TILE_HEIGHT))
                elif grid[row][col] == POWER_PELLET_SYMBOL:
                    power_pellet = PowerPellet(col * TILE_WIDTH, row * TILE_HEIGHT)
                    self.pellets.append(power_pellet)
                    self.power_pellets.append(power_pellet)

    def read_pellets_file(self, pellets_file):
        with open(pellets_file, "r") as f:
            return [row.strip().split(" ") for row in f]

    def empty(self):
        return not self.pellets

    def draw(self, screen):
        for pellet in self.pellets:
            pellet.draw(screen)