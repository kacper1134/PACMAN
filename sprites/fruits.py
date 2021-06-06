from sprites.character import Character
from settings import *


class Fruit(Character):
    def __init__(self, game):
        Character.__init__(self, game)
        self.name = "fruit"
        self.color = GREEN
        self.image = self.image = self.sprite_sheet.get_image_from_sheet(8, 2, IMAGE_SIZE, IMAGE_SIZE)
        self.set_start_position()
        self.life_span_seconds = 5
        self.timer = 0
        self.remove = False
        self.points = 100

    def set_start_position(self):
        self.node = self.find_start_node()
        self.direction = LEFT
        self.target = self.node.neighbors[self.direction]
        self.set_position()
        self.position.x -= (self.node.position.x - self.target.position.x) // 2

    def find_start_node(self):
        for node in self.game.nodes.nodes:
            if node.fruit_start_position:
                return node
        return None

    def update(self):
        self.timer += self.game.dt
        if self.timer >= self.life_span_seconds:
            self.remove = True
