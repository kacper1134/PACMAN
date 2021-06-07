import pygame as pg
from settings import *
import os


class SoundManager:
    def __init__(self, game):
        pg.mixer.init()
        self.game = game

        self.beginning_sound = self.get_sound(BEGINNING_SOUND_FILE)
        self.chomp_sound = self.get_sound(CHOMP_SOUND_FILE)
        self.death_sound = self.get_sound(DEATH_SOUND_FILE)
        self.eatfruit_sound = self.get_sound(EAT_FRUIT_SOUND_FILE)
        self.eatghost_sound = self.get_sound(EAT_GHOST_SOUND_FILE)

        self.background_sound_on = False
        self.timer = 0

    def get_sound(self, sound_name):
        return pg.mixer.Sound(os.path.join(SOUND_DIRECTORY, sound_name))

    def update(self):
        self.timer += self.game.dt

        if self.timer >= 4.0 and not self.background_sound_on:
            self.background_sound_on = True
            self.__play_background_sound()

    def play_beginning_sound(self):
        self.background_sound_on = False
        self.timer = 0
        pg.mixer.Sound.play(self.beginning_sound)

    def play_chomp_sound(self):
        if pg.mixer.get_busy() == 0:
            pg.mixer.Sound.play(self.chomp_sound)

    def play_death_sound(self):
        pg.mixer.music.stop()
        pg.mixer.Sound.play(self.death_sound)

    def play_eatfruit_sound(self):
        pg.mixer.Sound.play(self.eatfruit_sound)

    def play_eatghost_sound(self):
        pg.mixer.Sound.play(self.eatghost_sound)

    def __play_background_sound(self):
        pg.mixer.music.load(os.path.join(SOUND_DIRECTORY, BACKGROUND_SOUND_FILE))
        pg.mixer.music.play(-1)
