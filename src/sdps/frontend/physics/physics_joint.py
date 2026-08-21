from sdps.frontend.physics.physics_point import PhysicsPoint
import pygame

class PhysicsJoint:
    def __init__(self, p1: PhysicsPoint, p2: PhysicsPoint, length: float):
        self.p1 = p1
        self.p2 = p2
        self.length = length
        self.is_active = True

    def update(self):
        if not self.is_active:
            return

        diff = self.p1.pos - self.p2.pos
        dist = diff.length()
        if dist == 0:
            return

        diff_factor = (self.length - dist) / dist
        offset = diff * diff_factor * 0.5

        # Only displace points that are not pinned
        if not self.p1.is_pinned and not self.p2.is_pinned:
            self.p1.pos += offset
            self.p2.pos -= offset
        elif not self.p1.is_pinned:
            self.p1.pos += offset * 2.0
        elif not self.p2.is_pinned:
            self.p2.pos -= offset * 2.0

    def draw(self, screen):
        if self.is_active:
            pygame.draw.line(screen, (220, 220, 220), self.p1.pos, self.p2.pos, 1)