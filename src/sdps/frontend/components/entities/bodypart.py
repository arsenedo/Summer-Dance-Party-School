import math

from sdps.frontend.components.shape import Shape


class BodyPart:
    def __init__(
        self,
        width,
        length,
        color,
        pivot,
        direction,
        angle=0,
    ):
        """part anchored to a pivot

        Args:
            width: width
            length: length
            color: color
            pivot: (x, y) joint position the body part rotates around
            direction: direction the body part
                        (1: down for limbs, -1: up for torso/head)
            angle (int, optional): rotation angle in degrees, 0 = straight
                                   in the ``direction``.
        """
        self.width = width
        self.length = length
        self.color = color
        self.pivot = pivot
        self.direction = direction
        self.angle = angle

    def center(self):
        rad = math.radians(self.angle)
        half = self.length / 2
        x = self.pivot[0]
        y = self.pivot[1]
        return (
            x + math.sin(rad) * half * self.direction,
            y + math.cos(rad) * half * self.direction,
        )

    def corners(self):
        cx, cy = self.center()
        return Shape(None).rotated_rectangle_points(
            cx, cy, self.width, self.length, self.angle
        )

    def draw(self, surface, offset=(0, 0)):
        cx, cy = self.center()
        Shape(surface).draw_rotated_rectangle(
            cx + offset[0],
            cy + offset[1],
            self.width,
            self.length,
            self.angle,
            self.color,
        )
