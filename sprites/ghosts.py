from sprites.character import Character
from settings import *
import random


class Ghost(Character):
    def __init__(self, game):
        Character.__init__(self, game)
        self.name = "Ghost"
        self.points = 200
        self.previous_direction = STOP

        self.goal = Vector2Dim()

    def update(self):
        self.position += self.direction * self.speed * self.game.dt
        self.change_direction()
        self.move_constantly()
        self.portal_slow()

    def change_direction(self):
        if self.direction is STOP:
            new_direction = self.get_best_direction_to_goal()

            if new_direction:
                self.direction = new_direction
                self.target = self.node.neighbors[self.direction]
            else:
                self.reverse_direction()

            self.previous_direction = self.direction
        elif self.overshoot_target():
            self.node = self.target
            self.set_position()

            new_direction = self.get_best_direction_to_goal()

            if new_direction:
                self.direction = new_direction
                self.target = self.node.neighbors[self.direction]
                self.previous_direction = self.direction
            else:
                self.portal()
                self.direction = STOP

    def get_best_direction_to_goal(self):
        possible_directions = self.get_possible_directions()

        distances = []

        if not possible_directions:
            return None

        for direction in possible_directions:
            distance = self.node.position + direction - self.goal
            distances.append(distance.magnitude_squared())

        return possible_directions[distances.index(min(distances))]

    def get_random_direction(self):
        possible_directions = self.get_possible_directions()

        if possible_directions:
            return random.choice(self.get_possible_directions())
        return None

    def get_possible_directions(self):
        return [neighbor for neighbor in self.node.neighbors.keys() if self.node.neighbors[neighbor]
                and neighbor != self.previous_direction * -1]

    def portal_slow(self):
        self.speed = 100

        if self.node.portal_node or self.target.portal_node:
            self.speed *= 3 / 4
