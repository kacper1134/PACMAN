from sprites.character import Character
from structures.stack import Stack
from structures.animation import Animation
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

        self.guide_directions = [UP]

        self.pellets_needed_for_release = 0
        self.released_from_house = True
        self.banned_directions = []

        self.animation = None
        self.animations = {}

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

    def set_start_position(self, ghost_name):
        self.node = self.find_start_node(ghost_name)
        self.target = self.node
        self.set_position()

    def find_start_node(self, ghost_name):
        for node in self.game.nodes.nodes:
            if (node.blinky_start_position and ghost_name == "blinky") or \
                    (node.inky_start_position and ghost_name == "inky") or \
                    (node.pinky_start_position and ghost_name == "pinky") or \
                    (node.clyde_start_position and ghost_name == "clyde"):
                return node
        return None

    def update(self):
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
        self.update_animation()

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
                    self.direction = self.current_mode.direction
                    self.target = self.node.neighbors[self.direction]
                    self.set_position()
            elif self.current_mode.name == GUIDE_MODE:
                self.current_mode = self.modes.pop()
                if self.current_mode.name == GUIDE_MODE:
                    self.direction = self.current_mode.direction
                    self.target = self.node.neighbors[self.direction]
                    self.set_position()

    def change_mode(self):
        if not self.released_from_house:
            self.timer = 0
        elif self.current_mode.time:
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
        if self.current_mode.name != SPAWN_MODE and self.current_mode.name != GUIDE_MODE:
            if self.current_mode.name != FREIGHT_MODE:
                if self.current_mode.time:
                    dt = self.current_mode.time - self.timer
                    self.modes.push(GhostMode(name=self.current_mode.name, time=dt))
                else:
                    self.modes.push(GhostMode(name=self.current_mode.name))

            self.current_mode = GhostMode(FREIGHT_MODE, time=GHOST_FREIGHT_MODE_TIME * GHOST_FREIGHT_MODE_MULTIPLIER **
                                                             self.game.level_manager.level, mul=0.5)
            self.timer = 0
            self.reverse_direction()

    def spawn_mode(self):
        self.current_mode = GhostMode(SPAWN_MODE, mul=1.5)
        self.timer = 0

        for direction in self.guide_directions:
            self.modes.push(GhostMode(GUIDE_MODE, mul=0.5, direction=direction))

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
        aux = [neighbor for neighbor in self.node.neighbors.keys() if self.node.neighbors[neighbor]
               and neighbor != self.previous_direction * -1]
        possible_directions = []

        # Close Entrance To House For Ghost Not In Spawn Mode
        for direction in aux:
            if not(self.current_mode.name != SPAWN_MODE and self.node.ghost_house_entrance and direction == DOWN):
                if direction not in self.banned_directions:
                    possible_directions.append(direction)

        return possible_directions

    def portal_slow(self):
        self.speed = CHARACTER_SPEED * self.game.game_speed

        if self.node.portal_node or self.target.portal_node:
            self.speed *= 3 / 4

    def reverse_direction(self):
        if self.current_mode.name != GUIDE_MODE and self.current_mode.name != SPAWN_MODE:
            Character.reverse_direction(self)

    def update_animation(self):
        if self.current_mode.name == SPAWN_MODE:
            if self.direction == UP:
                self.animation = self.animations["spawnup"]
            elif self.direction == DOWN:
                self.animation = self.animations["spawndown"]
            elif self.direction == LEFT:
                self.animation = self.animations["spawnleft"]
            elif self.direction == RIGHT:
                self.animation = self.animations["spawnright"]
        elif self.current_mode.name == SCATTER_MODE or self.current_mode.name == CHASE_MODE:
            if self.direction == UP:
                self.animation = self.animations["up"]
            elif self.direction == DOWN:
                self.animation = self.animations["down"]
            elif self.direction == LEFT:
                self.animation = self.animations["left"]
            elif self.direction == RIGHT:
                self.animation = self.animations["right"]
        elif self.current_mode.name == FREIGHT_MODE:
            if self.timer >= (self.current_mode.time * 0.7):
                self.animation = self.animations["flash"]
            else:
                self.animation = self.animations["freight"]

        self.image = self.animation.update()

    def define_animations(self, ghost_number):
        directions = ["up", "down", "left", "right"]

        for image_number, direction in enumerate(directions):
            self.create_move_animation(direction, image_number * 2, ghost_number)
            self.create_spawn_animation(direction, image_number + 4)

        self.create_freight_animation()
        self.create_flash_animation()

    def create_move_animation(self, direction, image_number, ghost_number):
        animation = Animation(self.game, LOOP_ANIMATION_TYPE)
        animation.animation_speed = GHOST_ANIMATION_SPEED
        animation.add_frame(self.sprite_sheet.get_image_from_sheet(image_number, ghost_number, IMAGE_SIZE, IMAGE_SIZE))
        animation.add_frame(self.sprite_sheet.get_image_from_sheet(image_number + 1, ghost_number,
                                                                   IMAGE_SIZE, IMAGE_SIZE))
        self.animations[direction] = animation

    def create_spawn_animation(self, direction, image_number):
        animation = Animation(self.game, STATIC_ANIMATION_TYPE)
        animation.animation_speed = GHOST_ANIMATION_SPEED
        animation.add_frame(self.sprite_sheet.get_image_from_sheet(image_number, 6, IMAGE_SIZE, IMAGE_SIZE))
        self.animations["spawn" + direction] = animation

    def create_freight_animation(self):
        animation = Animation(self.game, LOOP_ANIMATION_TYPE)
        animation.animation_speed = GHOST_ANIMATION_SPEED

        for i in range(2):
            animation.add_frame(self.sprite_sheet.get_image_from_sheet(i, 6, IMAGE_SIZE, IMAGE_SIZE))

        self.animations["freight"] = animation

    def create_flash_animation(self):
        animation = Animation(self.game, LOOP_ANIMATION_TYPE)
        animation.animation_speed = GHOST_ANIMATION_SPEED
        animation.add_frame(self.sprite_sheet.get_image_from_sheet(0, 6, IMAGE_SIZE, IMAGE_SIZE))
        animation.add_frame(self.sprite_sheet.get_image_from_sheet(2, 6, IMAGE_SIZE, IMAGE_SIZE))
        animation.add_frame(self.sprite_sheet.get_image_from_sheet(1, 6, IMAGE_SIZE, IMAGE_SIZE))
        animation.add_frame(self.sprite_sheet.get_image_from_sheet(3, 6, IMAGE_SIZE, IMAGE_SIZE))
        self.animations["flash"] = animation


class Blinky(Ghost):
    def __init__(self, game):
        Ghost.__init__(self, game)
        self.name = "blinky"
        self.color = RED
        self.set_start_position(self.name)
        self.image = self.sprite_sheet.get_image_from_sheet(4, 2, IMAGE_SIZE, IMAGE_SIZE)
        self.define_animations(2)
        self.animation = self.animations["left"]


class Pinky(Ghost):
    def __init__(self, game):
        Ghost.__init__(self, game)
        self.name = "pinky"
        self.color = PINK
        self.set_start_position(self.name)
        self.image = self.sprite_sheet.get_image_from_sheet(0, 3, IMAGE_SIZE, IMAGE_SIZE)
        self.define_animations(3)
        self.animation = self.animations["up"]

    def set_scatter_goal(self):
        self.goal = Vector2Dim()

    def set_chase_goal(self):
        self.goal = self.game.pacman.position + self.game.pacman.direction * TILE_WIDTH * 4


class Inky(Ghost):
    def __init__(self, game):
        Ghost.__init__(self, game)
        self.name = "inky"
        self.color = TEAL
        self.set_start_position(self.name)
        self.image = self.sprite_sheet.get_image_from_sheet(2, 4, IMAGE_SIZE, IMAGE_SIZE)
        self.define_animations(4)
        self.animation = self.animations["down"]

        self.banned_directions = [RIGHT]
        self.pellets_needed_for_release = 30
        self.released_from_house = False
        self.guide_directions += [RIGHT]
        self.spawn_node = self.node

    def set_scatter_goal(self):
        self.goal = Vector2Dim(x=SCREEN_SIZE[0], y=SCREEN_SIZE[1])

    def set_chase_goal(self):
        pacman_future_position = self.game.pacman.position + self.game.pacman.direction * 2 * TILE_WIDTH
        aux_vec = (pacman_future_position - self.game.ghosts.get_blinky().position) * 2
        self.goal = self.game.ghosts.get_blinky().position + aux_vec


class Clyde(Ghost):
    def __init__(self, game):
        Ghost.__init__(self, game)
        self.name = "clyde"
        self.color = ORANGE
        self.set_start_position(self.name)
        self.image = self.sprite_sheet.get_image_from_sheet(2, 5, IMAGE_SIZE, IMAGE_SIZE)
        self.define_animations(5)
        self.animation = self.animations["down"]

        self.banned_directions = [LEFT]
        self.pellets_needed_for_release = 60
        self.released_from_house = False
        self.guide_directions += [LEFT]
        self.spawn_node = self.node

    def set_scatter_goal(self):
        self.goal = Vector2Dim(x=0, y=SCREEN_SIZE[1])

    def set_chase_goal(self):
        distance = (self.game.pacman.position - self.position).magnitude_squared()
        if distance <= (TILE_WIDTH * 8) ** 2:
            self.set_scatter_goal()
        else:
            self.goal = self.game.pacman.position + self.game.pacman.direction * 4 * TILE_WIDTH


class GhostGroup:
    def __init__(self, game):
        self.game = game
        self.ghosts = [Blinky(game), Pinky(game), Inky(game), Clyde(game)]

    def __iter__(self):
        return iter(self.ghosts)

    def get_blinky(self):
        return self.ghosts[0]

    def update(self):
        for ghost in self:
            ghost.update()

    def freight_mode(self):
        for ghost in self:
            if ghost.released_from_house:
                ghost.freight_mode()

    def update_points_for_eating(self):
        for ghost in self:
            ghost.points *= 2

    def reset_points_for_eating(self):
        for ghost in self:
            ghost.points = 200

    def hide(self):
        for ghost in self:
            ghost.visible = False

    def release_from_home(self):
        for ghost in self:
            if not ghost.released_from_house and ghost.pellets_needed_for_release <= self.game.eaten_pellets:
                ghost.released_from_house = True
                ghost.banned_directions = []
                ghost.spawn_mode()

    def draw(self):
        for ghost in self:
            ghost.draw()
