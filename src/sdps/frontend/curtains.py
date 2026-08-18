import pygame

from sdps.config import CURTAINS_COLOR

class Curtains:
    def __init__(self, height=1080):
        self.height = height

    def draw(self, display, width):
        w = display.get_width()
        pygame.draw.rect(display, CURTAINS_COLOR, (0, 0, width, self.height))
        pygame.draw.rect(display, CURTAINS_COLOR, (w - width, 0, w, self.height))
        