from sprites.pacman import Pacman
from sprites.ghosts import GhostGroup
from structures.nodes import *
from structures.pellets import PelletGroup
from sprites.fruits import Fruit
from pause import Pause
from levels import LevelManager
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
        self.fruit = None

        self.eaten_pellets = 0

        self.pause = Pause(self, True)
        self.level_manager = LevelManager()

        self.game_speed = 1.0

    def set_background(self):
        self.background = pg.surface.Surface(SCREEN_SIZE).convert()
        self.background.fill(BLACK)

    def start(self):
        self.level_manager.reset_game()
        maze_map = self.level_manager.get_level_map()

        game_folder = os.path.dirname(__file__)
        self.nodes = NodeGroup(os.path.join(game_folder, "mazes", maze_map["maze_name"]))
        self.pellets = PelletGroup(os.path.join(game_folder, "mazes", maze_map["pellet_name"]))
        self.pacman = Pacman(self)
        self.ghosts = GhostGroup(self)

        self.eaten_pellets = 0
        self.fruit = None
        self.pause.force_pause(True)

    def start_new_level(self):
        level_map = self.level_manager.get_level_map()
        self.set_background()

        game_folder = os.path.dirname(__file__)
        self.nodes = NodeGroup(os.path.join(game_folder, "mazes", level_map["maze_name"]))
        self.pellets = PelletGroup(os.path.join(game_folder, "mazes", level_map["pellet_name"]))

        self.pacman.nodes = self.nodes
        self.pacman.reset()
        self.ghosts = GhostGroup(self)

        self.eaten_pellets = 0
        self.fruit = None
        self.pause.force_pause(True)

    def update(self):
        self.dt = self.clock.tick(30) / 1000

        if not self.pause.paused:
            self.pacman.update()
            self.ghosts.update()

            if self.fruit:
                self.fruit.update()

            if self.pause.pause_type:
                self.pause.settle_pause()

            self.check_ghost_events()
            self.check_fruit_events()

        self.pellets.update(self.dt)
        self.check_pellets_events()
        self.pause.update()
        self.events()
        self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.pause.change_player_pause()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.draw(self.screen)
        self.pellets.draw(self.screen)
        self.pacman.draw()
        self.ghosts.draw()

        if self.fruit:
            self.fruit.draw()

        pg.display.update()

    def check_pellets_events(self):
        pellet = self.pacman.eat_pellet()
        if pellet:
            self.score += pellet.points
            self.eaten_pellets += 1

            if self.eaten_pellets == 70 or self.eaten_pellets == 140:
                self.fruit = Fruit(self)

            if pellet.name == "powerpellet":
                self.ghosts.freight_mode()

            self.pellets.pellets.remove(pellet)

            if self.pellets.empty():
                self.pacman.visible = False
                self.ghosts.hide()
                self.pause.start_timer(3, PAUSE_CLEAR)

    def check_ghost_events(self):
        self.ghosts.release_from_home()
        ghost = self.pacman.eat_ghost()
        if ghost:
            if ghost.current_mode.name == FREIGHT_MODE:
                ghost.spawn_mode()
                self.pause.start_timer(1, PAUSE_GHOST)
                self.pacman.visible = False
                ghost.visible = False

    def check_fruit_events(self):
        if self.fruit:
            if self.pacman.eat_fruit():
                self.score += self.fruit.points
                self.fruit = None
            elif self.fruit.remove:
                self.fruit = None

    def resolve_death(self):
        pass

    def resolve_level_clear(self):
        self.level_manager.next_level()
        self.start_new_level()
        self.pause.pause_type = None
        self.game_speed = min(self.game_speed * NEXT_LEVEL_SPEED_MULTIPLICATION, MAXIMUM_CHARACTER_SPEED)
        self.pacman.speed *= self.game_speed


if __name__ == "__main__":
    game = Game()
    game.start()
    while True:
        game.update()
