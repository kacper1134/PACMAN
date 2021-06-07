from sprites.pacman import Pacman
from sprites.ghosts import GhostGroup
from structures.nodes import *
from structures.pellets import PelletGroup
from structures.text import TextGroup
from structures.sprite import SpriteSheet
from structures.maze import Maze
from structures.sound_manager import SoundManager

from sprites.fruits import Fruit
from pause import Pause
from levels import LevelManager
import os


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_SIZE, 0, 32)
        self.background = None
        self.flash_background = None

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
        self.text_manager = TextGroup(self)
        self.sprite_sheet = SpriteSheet()
        self.maze = Maze(self)
        self.background_flash_on = False
        self.sound_manager = SoundManager(self)

        self.game_speed = 1.0

    def set_background(self):
        self.background = pg.surface.Surface(SCREEN_SIZE).convert()
        self.flash_background = pg.surface.Surface(SCREEN_SIZE).convert()
        self.background.fill(BLACK)

    def start(self):
        self.level_manager.reset_game()
        maze_map = self.level_manager.get_level_map()

        self.maze.get_maze(maze_map["maze_name"].split(".")[0])
        self.maze.create_maze()

        game_folder = os.path.dirname(__file__)
        self.nodes = NodeGroup(os.path.join(game_folder, "mazes", maze_map["maze_name"]))
        self.pellets = PelletGroup(os.path.join(game_folder, "mazes", maze_map["pellet_name"]))
        self.pacman = Pacman(self)
        self.ghosts = GhostGroup(self)

        self.eaten_pellets = 0
        self.fruit = None
        self.pause.force_pause(True)
        self.game_over = False

        self.score = 0
        self.text_manager.show_ready_text()
        self.text_manager.update_level(self.level_manager.level + 1)

        self.maze.reset_maze()
        self.background_flash_on = False

        self.sound_manager.play_beginning_sound()

    def start_new_level(self):
        level_map = self.level_manager.get_level_map()
        self.set_background()

        maze_map = self.level_manager.get_level_map()
        self.maze.get_maze(maze_map["maze_name"].split(".")[0])
        self.maze.create_maze()

        game_folder = os.path.dirname(__file__)
        self.nodes = NodeGroup(os.path.join(game_folder, "mazes", level_map["maze_name"]))
        self.pellets = PelletGroup(os.path.join(game_folder, "mazes", level_map["pellet_name"]))

        self.pacman.nodes = self.nodes
        self.pacman.reset()
        self.ghosts = GhostGroup(self)

        self.eaten_pellets = 0
        self.fruit = None
        self.pause.force_pause(True)

        self.text_manager.update_level(self.level_manager.level + 1)
        self.maze.reset_maze()
        self.background_flash_on = False

    def reset_level_after_pacman_dies(self):
        self.sound_manager.play_beginning_sound()
        self.pacman.reset()
        self.ghosts = GhostGroup(self)
        self.fruit = None
        self.pause.force_pause(True)
        self.text_manager.show_ready_text()
        self.maze.reset_maze()
        self.background_flash_on = False

    def update(self):
        if not self.game_over:
            self.dt = self.clock.tick(FPS) / 1000

            if (self.pause.pause_type == PAUSE_CLEAR or self.pause.pause_type == PAUSE_DIE) and not self.pause.paused:
                self.pause.settle_pause()
            elif not self.pause.paused:
                self.pacman.update()
                self.ghosts.update()

                if self.fruit:
                    self.fruit.update()

                self.check_pellets_events()
                self.check_ghost_events()
                self.check_fruit_events()

                if self.pacman.lives == 0:
                    self.text_manager.show_game_over_text()

            self.text_manager.update()
            self.pause.update()
            self.pellets.update(self.dt)

        if self.pacman.death_animation:
            self.pacman.update_death()

        if self.background_flash_on:
            self.maze.flash_maze()

        self.sound_manager.update()
        self.text_manager.update_score(self.score)
        self.events()
        self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                if self.game_over:
                    self.start()
                else:
                    if self.pacman.lives != 0:
                        self.pause.change_player_pause()
                        if self.pause.paused:
                            self.text_manager.show_paused_text()
                        else:
                            self.text_manager.hide_all_messages()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        # self.nodes.draw(self.screen)
        self.pellets.draw(self.screen)
        self.pacman.draw()
        self.ghosts.draw()
        self.text_manager.draw()

        if self.fruit:
            self.fruit.draw()

        self.pacman.draw_lives()

        pg.display.update()

    def check_pellets_events(self):
        pellet = self.pacman.eat_pellet()
        if pellet:
            self.score += pellet.points
            self.eaten_pellets += 1

            if self.eaten_pellets == 70 or self.eaten_pellets == 140:
                self.fruit = Fruit(self)

            if pellet.name == "powerpellet":
                self.ghosts.reset_points_for_eating()
                self.ghosts.freight_mode()

            self.pellets.pellets.remove(pellet)

            if self.pellets.empty():
                self.pacman.visible = False
                self.ghosts.hide()
                self.pause.start_timer(3, PAUSE_CLEAR)
                self.background_flash_on = True

            self.sound_manager.play_chomp_sound()

    def check_ghost_events(self):
        self.ghosts.release_from_home()
        ghost = self.pacman.eat_ghost()
        if ghost:
            if ghost.current_mode.name == FREIGHT_MODE:
                self.score += ghost.points
                self.text_manager.create_temp_text(ghost.points, ghost.position)
                self.ghosts.update_points_for_eating()

                ghost.spawn_mode()
                self.sound_manager.play_eatghost_sound()
                self.pause.start_timer(1, PAUSE_GHOST)
                self.pacman.visible = False
                ghost.visible = False
            elif ghost.current_mode.name == SCATTER_MODE or ghost.current_mode.name == CHASE_MODE:
                self.pacman.lose_live()
                self.sound_manager.play_death_sound()
                self.ghosts.hide()
                self.pause.start_timer(3, PAUSE_DIE)

    def check_fruit_events(self):
        if self.fruit:
            if self.pacman.eat_fruit():
                self.score += self.fruit.points
                self.text_manager.create_temp_text(self.fruit.points, self.fruit.position)
                self.fruit = None
                self.sound_manager.play_eatfruit_sound()
            elif self.fruit.remove:
                self.fruit = None

    def resolve_death(self):
        if self.pacman.lives == 0:
            self.game_over = True
            self.text_manager.show_game_over_text()
        else:
            self.reset_level_after_pacman_dies()
        self.pause.pause_type = None

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
