from sprites.pacman import Pacman
from sprites.ghosts import GhostGroup
from structures.nodes import *
from structures.pellets import PelletGroup
import os


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_SIZE, 0, 32)
        self.background = None
        self.set_background()
        self.clock = pg.time.Clock()
        self.dt = 0

        self.score = 0

        self.pacman = None
        self.nodes = None

    def set_background(self):
        self.background = pg.surface.Surface(SCREEN_SIZE).convert()
        self.background.fill(BLACK)

    def start(self):
        game_folder = os.path.dirname(__file__)
        self.nodes = NodeGroup(os.path.join(game_folder, "mazes", "first_maze.txt"))
        self.pellets = PelletGroup(os.path.join(game_folder, "mazes", "pellets_first_maze.txt"))
        self.pacman = Pacman(self)
        self.ghosts = GhostGroup(self)

    def update(self):
        self.dt = self.clock.tick(30) / 1000
        self.pacman.update()
        self.ghosts.update()
        self.pellets.update(self.dt)
        self.check_pellets_events()
        self.check_ghost_events()
        self.events()
        self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                exit()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.draw(self.screen)
        self.pellets.draw(self.screen)
        self.pacman.draw()
        self.ghosts.draw()
        pg.display.update()

    def check_pellets_events(self):
        pellet = self.pacman.eat_pellet()
        if pellet:
            self.score += pellet.points

            if pellet.name == "powerpellet":
                self.ghosts.freight_mode()

            self.pellets.pellets.remove(pellet)

    def check_ghost_events(self):
        ghost = self.pacman.eat_ghost()
        if ghost:
            if ghost.current_mode.name == FREIGHT_MODE:
                ghost.spawn_mode()


if __name__ == "__main__":
    game = Game()
    game.start()
    while True:
        game.update()
