import pygame as pg
from settings import *


class Character:
    def __init__(self, game):
        self.name = "character"
        self.game = game
        self.direction = STOP
        self.next_direction = STOP
        self.speed = CHARACTER_SPEED
        self.radius = 10
        self.color = WHITE

        self.nodes = self.game.nodes
        self.node = self.nodes.nodes[0]
        self.target = self.node

        self.collide_distance = 5

        self.visible = True

        self.set_position()

    def set_position(self):
        self.position = self.node.position.copy()

    def update(self):
        self.position += self.direction * self.speed * self.game.dt
        self.move_constantly()

    def draw(self):
        if self.visible:
            pos = self.position.to_int()
            pg.draw.circle(self.game.screen, self.color, pos, self.radius)

    def overshoot_target(self):
        if self.target:
            vector1 = self.target.position - self.node.position
            vector2 = self.position - self.node.position
            target_node_distance = vector1.magnitude_squared()
            self_node_distance = vector2.magnitude_squared()
            return self_node_distance >= target_node_distance
        return False

    def move_constantly(self):
        if self.direction is not STOP:
            if self.overshoot_target():
                self.node = self.target

                self.portal()

                if self.node.neighbors[self.direction]:
                    self.target = self.node.neighbors[self.direction]
                else:
                    self.set_position()
                    self.direction = STOP

    def reverse_direction(self):
        if self.direction == UP:
            self.direction = DOWN
        elif self.direction == DOWN:
            self.direction = UP
        elif self.direction == LEFT:
            self.direction = RIGHT
        elif self.direction == RIGHT:
            self.direction = LEFT

        aux = self.target
        self.target = self.node
        self.node = aux

    def portal(self):
        if self.node.portal_node:
            self.node = self.node.portal_node
            self.set_position()
