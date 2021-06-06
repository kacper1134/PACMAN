import pygame as pg
from settings import *


class SpriteSheet:
    def __init__(self):
        self.sprite_sheet = pg.image.load(os.path.join(IMAGE_DIRECTORY, SPRITE_SHEET_FILE)).convert()
        self.sprite_sheet.set_colorkey(TRANSPARENT_COLOR)

    def get_image_from_sheet(self, x, y, width, height):
        x *= width
        y *= height

        self.sprite_sheet.set_clip(pg.Rect(x, y, width, height))
        return self.sprite_sheet.subsurface(self.sprite_sheet.get_clip())
