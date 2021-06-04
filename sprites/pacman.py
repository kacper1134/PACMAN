from sprites.character import Character
from settings import *
import pygame as pg


class Pacman(Character):
    def __init__(self, game):
        Character.__init__(self, game)
        self.name = "pacman"
        self.color = YELLOW
        self.lives = 5
        self.set_start_position()

    def reset(self):
        self.direction = LEFT
        self.next_direction = STOP
        self.visible = True
        self.set_start_position()

    def set_start_position(self):
        self.node = self.find_start_node()
        self.direction = LEFT
        self.target = self.node.neighbors[self.direction]
        self.set_position()
        self.position.x -= (self.node.position.x - self.target.position.x) // 2

    def find_start_node(self):
        for node in self.game.nodes.nodes:
            if node.pacman_start_position:
                return node
        return None

    def update(self):
        self.visible = True
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
                    if self.node.ghost_house_entrance:  # Ghost House Entrance
                        if self.node.neighbors[self.direction]:
                            self.target = self.node.neighbors[self.direction]
                        else:
                            self.set_position()
                            self.direction = STOP
                    else:  # "Normal" Node
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

    def eat_ghost(self):
        for ghost in self.game.ghosts:
            distance = self.position - ghost.position
            squared_distance = distance.magnitude_squared()
            collide_squared_distance = (self.collide_distance + ghost.collide_distance) ** 2
            if squared_distance <= collide_squared_distance:
                return ghost
        return None

    def eat_fruit(self):
        if self.game.fruit:
            distance = self.position - self.game.fruit.position
            squared_distance = distance.magnitude_squared()
            collide_squared_distance = (self.collide_distance + self.game.fruit.collide_distance) ** 2
            if squared_distance <= collide_squared_distance:
                return True
        return False

    def lose_live(self):
        self.lives -= 1
        self.direction = STOP
        self.next_direction = STOP

    def draw_lives(self):
        for i in range(self.lives - 1):
            x_position = 5 + self.radius + (2 * self.radius + 5) * i
            y_position = TILE_WIDTH * (ROWS - 1)
            pg.draw.circle(self.game.screen, self.color, (x_position, y_position), self.radius)
