from sprites.character import Character
from structures.stack import Stack
from settings import *
import random


class GhostMode:
    def __init__(self, name, time=None, mul=1, direction=None):
        self.name = name
        self.time = time
        self.speed_multiplication = mul
        self.direction = direction


class Ghost(Character):
    def __init__(self, game):
        Character.__init__(self, game)
        self.name = "Ghost"
        self.points = 200
        self.previous_direction = STOP
        self.goal = Vector2Dim()

        self.modes = self.set_up_initial_modes()
        self.current_mode = self.modes.pop()
        self.timer = 0

    def set_up_initial_modes(self):
        modes = Stack()
        modes.push(GhostMode(CHASE_MODE))
        modes.push(GhostMode(SCATTER_MODE, 5))
        modes.push(GhostMode(CHASE_MODE, 20))
        modes.push(GhostMode(SCATTER_MODE, 7))
        modes.push(GhostMode(CHASE_MODE, 20))
        modes.push(GhostMode(SCATTER_MODE, 7))
        modes.push(GhostMode(CHASE_MODE, 20))
        modes.push(GhostMode(SCATTER_MODE, 7))
        return modes

    def update(self):
        self.visible = True
        self.position += self.direction * self.speed * self.game.dt
        self.timer += self.game.dt

        self.change_mode()

        if self.current_mode.name == SCATTER_MODE:
            self.set_scatter_goal()
        elif self.current_mode.name == CHASE_MODE:
            self.set_chase_goal()

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

    def change_mode(self):
        if self.current_mode.time:
            if self.timer >= self.current_mode.time:
                self.reverse_direction()
                self.previous_direction = self.direction
                self.current_mode = self.modes.pop()
                self.timer = 0

    def set_scatter_goal(self):
        self.goal = Vector2Dim(SCREEN_SIZE[0], 0)

    def set_chase_goal(self):
        self.goal = self.game.pacman.position

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
