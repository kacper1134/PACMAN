import pygame as pg
from settings import *


class Pacman:
    def __init__(self, game):
        self.name = "pacman"
        self.game = game
        self.direction = STOP
        self.next_direction = STOP
        self.speed = 100
        self.radius = 10
        self.color = YELLOW

        self.nodes = self.game.nodes
        self.node = self.nodes.nodes[0]
        self.target = self.node
        self.set_position()

    def set_position(self):
        self.position = self.node.position.copy()

    def update(self):
        self.position += self.direction * self.speed * self.game.dt
        self.get_next_direction()

        if self.next_direction is not STOP:
            self.move_by_key()
        else:
            self.move_constantly()

    def get_next_direction(self):
        key = pg.key.get_pressed()
        if key[pg.K_UP]:
            self.next_direction = UP
        if key[pg.K_DOWN]:
            self.next_direction = DOWN
        if key[pg.K_LEFT]:
            self.next_direction = LEFT
        if key[pg.K_RIGHT]:
            self.next_direction = RIGHT
        return None

    def move_by_key(self):
        if self.direction is STOP:
            if self.node.neighbors[self.next_direction]:
                self.direction = self.next_direction
                self.target = self.node.neighbors[self.next_direction]
            self.next_direction = STOP
        else:
            if self.next_direction == self.direction * -1:
                self.reverse_direction()
                self.next_direction = STOP

            if self.overshoot_target():
                self.node = self.target

                if self.node.neighbors[self.next_direction]:
                    self.target = self.node.neighbors[self.next_direction]

                    if self.direction != self.next_direction:
                        self.set_position()
                        self.direction = self.next_direction
                        self.next_direction = STOP

                else:
                    if self.node.neighbors[self.direction]:
                        self.target = self.node.neighbors[self.direction]
                    else:
                        self.set_position()
                        self.direction = STOP

    def move_constantly(self):
        if self.direction is not STOP:
            if self.overshoot_target():
                self.node = self.target
                if self.node.neighbors[self.direction]:
                    self.target = self.node.neighbors[self.direction]
                else:
                    self.set_position()
                    self.direction = STOP

    def draw(self):
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
