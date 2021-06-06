from settings import *


class Animation:
    def __init__(self, game, animation_type):
        self.game = game
        self.animation_type = animation_type
        self.frames = []
        self.current_frame_number = 0
        self.animation_finished = False
        self.animation_speed = 0
        self.dt = 0

    def reset_animation(self):
        self.current_frame_number = 0
        self.animation_finished = False

    def add_frame(self, frame):
        self.frames.append(frame)

    def update(self):
        if self.animation_type == STATIC_ANIMATION_TYPE:
            self.current_frame_number = 0
        elif self.animation_type == ONCE_ANIMATION_TYPE:
            self.animate_once()
        elif self.animation_type == LOOP_ANIMATION_TYPE:
            self.animate_in_loop()

        return self.frames[self.current_frame_number]

    def animate_once(self):
        if not self.animation_finished:
            self.get_next_frame()

            if self.current_frame_number == len(self.frames) - 1:
                self.animation_finished = True

    def animate_in_loop(self):
        self.get_next_frame()
        if self.current_frame_number == len(self.frames):
            self.current_frame_number = 0

    def get_next_frame(self):
        self.dt += self.game.dt

        if self.dt >= (1.0 / self.animation_speed):
            self.current_frame_number += 1
            self.dt = 0
