from sprites.pacman import Pacman
from structures.nodes import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_SIZE, 0, 32)
        self.background = None
        self.set_background()
        self.clock = pg.time.Clock()
        self.dt = 0

        self.pacman = None
        self.nodes = None

    def set_background(self):
        self.background = pg.surface.Surface(SCREEN_SIZE).convert()
        self.background.fill(BLACK)

    def start(self):
        self.nodes = NodeGroup()
        self.nodes.setupTestNodes()
        self.pacman = Pacman(self)

    def update(self):
        self.dt = self.clock.tick(30) / 1000
        self.pacman.update()
        self.events()
        self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                exit()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.draw(self.screen)
        self.pacman.draw()
        pg.display.update()


if __name__ == "__main__":
    game = Game()
    game.start()
    while True:
        game.update()
