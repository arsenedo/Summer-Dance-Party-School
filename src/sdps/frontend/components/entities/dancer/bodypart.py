import math

import pygame

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
        clothing=None,
        footwear=None,
    ):
        """part anchored to a pivot

        Args:
            width: width
            length: length
            color: skin tone of the dancer (always drawn first)
            pivot: (x, y) joint position the body part rotates around
            direction: direction the body part
                        (1: down for limbs, -1: up for torso/head)
            angle (int, optional): rotation angle in degrees, 0 = straight
                                   in the ``direction``.
            clothing: optional garment painted ON TOP of the bare part
            footwear: optional shoe painted at the lower end of the part,
                      only used for leg parts
        """
        self.width = width
        self.length = length
        self.color = color
        self.pivot = pivot
        self.direction = direction
        self.angle = angle
        self.clothing = clothing
        self.footwear = footwear

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
        w = max(1, int(self.width))
        h = max(1, int(self.length))

        canvas = pygame.Surface((w, h), pygame.SRCALPHA)

        Shape(canvas).draw_rectangle(0, 0, w, h, self.color)

        if self.clothing is not None:
            self.clothing.design(
                Shape(canvas),
                w,
                h,
                self.clothing.main_color,
                self.clothing.detail_color,
            )

        if self.footwear is not None:
            shoe_h = max(2, int(h * self.footwear.height_ratio))
            shoe_canvas = pygame.Surface((w, shoe_h), pygame.SRCALPHA)
            self.footwear.design(
                Shape(shoe_canvas),
                w,
                shoe_h,
                self.footwear.main_color,
                self.footwear.detail_color,
            )
            canvas.blit(shoe_canvas, (0, h - shoe_h))

        rotated = pygame.transform.rotate(canvas, self.angle)
        surface.blit(
            rotated,
            (
                cx + offset[0] - rotated.get_width() / 2,
                cy + offset[1] - rotated.get_height() / 2,
            ),
        )
