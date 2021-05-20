from sprites.character import Character
from settings import *
import pygame as pg


class Pacman(Character):
    def __init__(self, game):
        Character.__init__(self, game)
        self.name = "pacman"
        self.color = YELLOW

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

                self.portal()

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

    def eat_pellet(self):
        for pellet in self.game.pellets.pellets:
            distance = self.position - pellet.position
            squared_distance = distance.magnitude_squared()
            collision_distance = (pellet.radius + self.collide_distance) ** 2
            if squared_distance <= collision_distance:
                return pellet
        return None
