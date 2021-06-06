from sprites.character import Character
from structures.animation import Animation
from settings import *
import pygame as pg


class Pacman(Character):
    def __init__(self, game):
        Character.__init__(self, game)
        self.name = "pacman"
        self.color = YELLOW
        self.lives = 5

        self.start_image = self.sprite_sheet.get_image_from_sheet(0, 1, IMAGE_SIZE, IMAGE_SIZE)
        self.image = self.start_image
        self.life_icon = self.image

        self.animation = None
        self.animations = {}
        self.define_animations()
        self.set_start_position()

        self.death_animation = False

    def reset(self):
        self.direction = LEFT
        self.next_direction = STOP
        self.visible = True
        self.set_start_position()
        self.image = self.start_image
        self.animations["death"].reset_animation()
        self.death_animation = False

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
        self.update_animation()
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
        self.animation = self.animations["death"]
        self.death_animation = True
        self.direction = STOP
        self.next_direction = STOP

    def draw_lives(self):
        for i in range(self.lives - 1):
            x_position = 10 + 42 * i
            y_position = TILE_WIDTH * ROWS - 32
            self.game.screen.blit(self.life_icon, (x_position, y_position))

    def update_animation(self):
        if self.direction == UP:
            self.animation = self.animations["up"]
        elif self.direction == DOWN:
            self.animation = self.animations["down"]
        elif self.direction == LEFT:
            self.animation = self.animations["left"]
        elif self.direction == RIGHT:
            self.animation = self.animations["right"]
        elif self.direction == STOP:
            self.animation = self.animations["idle"]

        self.image = self.animation.update()

    def update_death(self):
        self.image = self.animation.update()

    def define_animations(self):
        directions = ["left", "right", "down", "up"]
        for image_number, direction in enumerate(directions):
            self.create_move_animation(direction, image_number)

        self.create_death_animation()
        self.create_idle_animation()

    def create_move_animation(self, direction, image_number):
        animation = Animation(self.game, LOOP_ANIMATION_TYPE)
        animation.animation_speed = PACMAN_ANIMATION_SPEED
        animation.add_frame(self.sprite_sheet.get_image_from_sheet(4, 0, IMAGE_SIZE, IMAGE_SIZE))
        animation.add_frame(self.sprite_sheet.get_image_from_sheet(image_number, 0, IMAGE_SIZE, IMAGE_SIZE))
        animation.add_frame(self.sprite_sheet.get_image_from_sheet(image_number, 1, IMAGE_SIZE, IMAGE_SIZE))
        animation.add_frame(self.sprite_sheet.get_image_from_sheet(image_number, 0, IMAGE_SIZE, IMAGE_SIZE))
        self.animations[direction] = animation

    def create_death_animation(self):
        animation = Animation(self.game, ONCE_ANIMATION_TYPE)
        animation.animation_speed = PACMAN_ANIMATION_SPEED // 3
        for i in range(11):
            animation.add_frame(self.sprite_sheet.get_image_from_sheet(i, 7, IMAGE_SIZE, IMAGE_SIZE))
        self.animations["death"] = animation

    def create_idle_animation(self):
        animation = Animation(self.game, STATIC_ANIMATION_TYPE)
        animation.add_frame(self.sprite_sheet.get_image_from_sheet(4, 0, IMAGE_SIZE, IMAGE_SIZE))
        self.animations["idle"] = animation
