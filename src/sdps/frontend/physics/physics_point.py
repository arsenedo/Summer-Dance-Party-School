from pygame import Vector2
from pygame import draw
from pygame.draw_py import Point

from sdps.frontend.components import Shape


class PhysicsPoint:
    l_neighbor = None
    r_neighbor = None
    def __init__(self, x, y):
        self.pos = Vector2(x, y)
        self.prev_pos = Vector2(x, y)
        self.init_pos = Vector2(x, y)
        self.is_pinned = False

    def update(self, delta_time, drag, acceleration):
        if self.is_pinned:
            self.pos = Vector2(self.init_pos)
            return

        velocity = (self.pos - self.prev_pos) * (1 - drag)
        new_pos = self.pos + velocity + acceleration * (delta_time ** 2)
        self.prev_pos = Vector2(self.pos)
        self.pos = new_pos
