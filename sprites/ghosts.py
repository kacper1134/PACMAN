from sprites.character import Character
from structures.stack import Stack
from settings import *
import random


class GhostMode:
    def __init__(self, name, time=None, mul=1.0, direction=None):
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

        self.spawn_node = self.find_spawn_node()

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
        print(self.current_mode.name)
        self.visible = True
        self.position += self.direction * self.speed * self.game.dt * self.current_mode.speed_multiplication
        self.timer += self.game.dt

        self.change_mode()

        if self.current_mode.name == SCATTER_MODE:
            self.set_scatter_goal()
        elif self.current_mode.name == CHASE_MODE:
            self.set_chase_goal()
        elif self.current_mode.name == FREIGHT_MODE:
            self.set_random_goal()
        elif self.current_mode.name == SPAWN_MODE:
            self.set_spawn_goal()

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

            if self.current_mode.name == SPAWN_MODE:
                if self.position == self.goal:
                    self.current_mode = self.modes.pop()

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

    def set_random_goal(self):
        x = random.randint(0, COLS * TILE_WIDTH)
        y = random.randint(0, ROWS * TILE_HEIGHT)
        self.goal = Vector2Dim(x, y)

    def set_spawn_goal(self):
        self.goal = self.spawn_node.position

    def freight_mode(self):
        if self.current_mode.name != SPAWN_MODE:
            if self.current_mode.name != FREIGHT_MODE:
                if self.current_mode.time:
                    dt = self.current_mode.time - self.timer
                    self.modes.push(GhostMode(name=self.current_mode.name, time=dt))
                else:
                    self.modes.push(GhostMode(name=self.current_mode.name))

            self.current_mode = GhostMode(FREIGHT_MODE, time=7, mul=0.5)
            self.timer = 0
            self.reverse_direction()

    def spawn_mode(self):
        self.current_mode = GhostMode(SPAWN_MODE, mul=1.5)
        self.timer = 0

    def find_spawn_node(self):
        for node in self.nodes.ghost_home_nodes:
            if node.ghost_spawn:
                return node
        return None

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
        self.speed = CHARACTER_SPEED

        if self.node.portal_node or self.target.portal_node:
            self.speed *= 3 / 4
