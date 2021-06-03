from settings import *


class Pause:
    def __init__(self, game, paused=False):
        self.game = game
        self.paused = paused
        self.timer = 0
        self.pause_time = 0
        self.player_pause = paused
        self.pause_type = None

    def update(self):
        if not self.player_pause:
            if self.paused:
                self.timer += self.game.dt

                if self.timer >= self.pause_time:
                    self.timer = 0
                    self.paused = False

    def start_timer(self, pause_time, pause_type):
        self.pause_time = pause_time
        self.pause_type = pause_type
        self.timer = 0
        self.paused = True

    def change_player_pause(self):
        self.player_pause = not self.player_pause
        self.paused = self.player_pause

    def force_pause(self, pause):
        self.paused = pause
        self.player_pause = pause
        self.timer = 0
        self.pause_time = 0

    def settle_pause(self):
        if self.pause_type == PAUSE_DIE:
            self.game.resolve_death()
        elif self.pause_type == PAUSE_CLEAR:
            self.game.resolve_level_clear()
