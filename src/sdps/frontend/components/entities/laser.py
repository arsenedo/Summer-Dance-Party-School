import random

import pygame

from sdps.config import (
    LASER_ALPHA,
    LASER_GLOW_ALPHA,
    LASER_GLOW_HALF_WIDTH,
    LASER_HALF_WIDTH,
    SCREEN_WIDTH,
)


class Laser:
    def __init__(self, coord, floor_top_y, floor_bottom_y, color):
        self.coord = pygame.math.Vector2(coord)
        self.floor_top_y = floor_top_y
        self.floor_bottom_y = floor_bottom_y
        self.color = color
        self.target = self._pick_target()

    def _pick_target(self):
        return pygame.math.Vector2(
            random.uniform(0, SCREEN_WIDTH),
            random.uniform(self.floor_top_y, self.floor_bottom_y),
        )

    def _triangle(self, half_width):
        direction = self.target - self.coord
        if direction.length() == 0:
            return None
        direction = direction.normalize()
        perpendicular = pygame.math.Vector2(-direction.y, direction.x)
        base_left = self.target + perpendicular * half_width
        base_right = self.target - perpendicular * half_width
        return (
            (self.coord.x, self.coord.y),
            (base_left.x, base_left.y),
            (base_right.x, base_right.y),
        )

    def draw_on(self, surface, shape):
        glow = self._triangle(LASER_GLOW_HALF_WIDTH)
        if glow is not None:
            shape.draw_triangle_on(
                surface, glow[0], glow[1], glow[2],
                (self.color[0], self.color[1], self.color[2], LASER_GLOW_ALPHA),
            )
        core = self._triangle(LASER_HALF_WIDTH)
        if core is not None:
            shape.draw_triangle_on(
                surface, core[0], core[1], core[2],
                (self.color[0], self.color[1], self.color[2], LASER_ALPHA),
            )
