import pygame

from sdps.config import DANCER_SIZE
from sdps.frontend.components.shape import Shape


class Dancer(pygame.sprite.Sprite):
    def __init__(
        self,
        groups,
        pos,
        color,
        size = DANCER_SIZE,
    ):
        super().__init__(groups)
        self.pos = pos
        self.color = color
        self.size = size

        self.create_surf()

    def create_surf(self):
        self.image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.image.set_colorkey("black")
        Shape(self.image).draw_rectangle(0, 0, self.size, self.size, self.color)
        self.rect = self.image.get_rect(center=self.pos)
