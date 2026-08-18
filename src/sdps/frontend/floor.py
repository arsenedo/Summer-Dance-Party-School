import pygame

from sdps.config import FLOOR_COLOR


class Floor:
    def __init__(self, width=1920, height=540, y_offset=540):
        self.width = width
        self.height = height
        self.y_offset = y_offset

    def draw(self, display):
        pygame.draw.rect(display, FLOOR_COLOR, (0, self.y_offset, self.width,
                                                 self.height))
