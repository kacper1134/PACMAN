import pygame as pg
from settings import *


class Text:
    def __init__(self, game, displayed_text, color, x_position, y_position, size, visible=True):
        self.game = game
        self.displayed_text = displayed_text
        self.color = color
        self.size = size
        self.position = Vector2Dim(x_position, y_position)
        self.visible = visible
        self.label = None
        self.font = None
        self.total_time = 0
        self.life_span = 0
        self.set_up_font()
        self.create_label()

    def set_up_font(self):
        self.font = pg.font.Font(os.path.join(FONT_DIRECTORY, FONT_FILE), self.size)

    def change_text(self, new_displayed_text):
        self.displayed_text = new_displayed_text
        self.create_label()

    def create_label(self):
        self.label = self.font.render(self.displayed_text, 1, self.color)

    def update(self):
        if self.life_span > 0:
            self.total_time += self.game.dt
            if self.total_time >= self.life_span:
                self.total_time = 0
                self.life_span = 0
                self.visible = False

    def draw(self):
        if self.visible:
            self.game.screen.blit(self.label, self.position.to_tuple())


class TextGroup:
    def __init__(self, game):
        self.game = game
        self.texts = {}
        self.set_up_texts()
        self.temp_texts = []

    def set_up_texts(self):
        self.texts["score_label"] = Text(self.game, "SCORE", WHITE, 0, 5, FONT_SIZE)
        self.texts["level_label"] = Text(self.game, "LEVEL", WHITE, 368, 5, FONT_SIZE)
        self.texts["score"] = Text(self.game, "0".zfill(8), WHITE, 0, 21, FONT_SIZE)
        self.texts["level"] = Text(self.game, "0".zfill(3), WHITE, 368, 21, FONT_SIZE)
        self.texts["ready"] = Text(self.game, "READY!", YELLOW, 180, 320, FONT_SIZE, False)
        self.texts["paused"] = Text(self.game, "PAUSED!", YELLOW, 170, 320, FONT_SIZE, False)
        self.texts["game_over"] = Text(self.game, "GAMEOVER!", RED, 160, 320, FONT_SIZE, False)

    def update_score(self, new_score):
        self.texts["score"].change_text(str(new_score).zfill(8))

    def update_level(self, new_level):
        self.texts["level"].change_text(str(new_level).zfill(3))

    def show_ready_text(self):
        self.texts["ready"].visible = True
        self.texts["paused"].visible = False
        self.texts["game_over"].visible = False

    def show_paused_text(self):
        self.texts["ready"].visible = False
        self.texts["paused"].visible = True
        self.texts["game_over"].visible = False

    def show_game_over_text(self):
        self.texts["ready"].visible = False
        self.texts["paused"].visible = False
        self.texts["game_over"].visible = True

    def hide_all_messages(self):
        self.texts["ready"].visible = False
        self.texts["paused"].visible = False
        self.texts["game_over"].visible = False

    def create_temp_text(self, value, position):
        x, y = position.to_tuple()
        temp_text = Text(self.game, str(value), WHITE, x, y, FONT_SIZE // 2)
        temp_text.life_span = 1
        self.temp_texts.append(temp_text)

    def update(self):
        for text in self.texts.keys():
            self.texts[text].update()

        for text in self.temp_texts:
            text.update()

    def draw(self):
        for text in self.texts.keys():
            self.texts[text].draw()

        for text in self.temp_texts:
            text.draw()
