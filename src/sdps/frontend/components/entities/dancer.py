import pygame

from sdps.config import (
    DANCER_ARM_LENGTH,
    DANCER_ARM_WIDTH,
    DANCER_BODY_LENGTH,
    DANCER_BODY_WIDTH,
    DANCER_HEAD_SIZE,
    DANCER_LEG_LENGTH,
    DANCER_LEG_WIDTH,
)
from sdps.frontend.components.entities.bodypart import BodyPart


class Dancer(pygame.sprite.Sprite):
    def __init__(
        self,
        groups,
        pos,
        color,
    ):
        super().__init__(groups)
        self.pos = pos
        self.color = color

        self.body = None
        self.head = None
        self.arm_left = None
        self.arm_right = None
        self.leg_left = None
        self.leg_right = None

        self._build_body()
        self.render()

    def _build_body(self):
        x, y = self.pos
        body_top = y - DANCER_BODY_LENGTH
        leg_gap = DANCER_BODY_WIDTH / 4
        arm_gap = DANCER_BODY_WIDTH / 2

        self.body = BodyPart(
            DANCER_BODY_WIDTH, DANCER_BODY_LENGTH, self.color, (x, y), -1
        )
        self.head = BodyPart(
            DANCER_HEAD_SIZE, DANCER_HEAD_SIZE, self.color, (x, body_top), -1
        )
        self.leg_left = BodyPart(
            DANCER_LEG_WIDTH, DANCER_LEG_LENGTH, self.color, (x - leg_gap, y), 1
        )
        self.leg_right = BodyPart(
            DANCER_LEG_WIDTH, DANCER_LEG_LENGTH, self.color, (x + leg_gap, y), 1
        )
        self.arm_left = BodyPart(
            DANCER_ARM_WIDTH, DANCER_ARM_LENGTH, self.color, (x - arm_gap, body_top), 1
        )
        self.arm_right = BodyPart(
            DANCER_ARM_WIDTH, DANCER_ARM_LENGTH, self.color, (x + arm_gap, body_top), 1
        )

    def _parts(self):
        return [
            self.arm_left,
            self.leg_left,
            self.leg_right,
            self.body,
            self.arm_right,
            self.head,
        ]

    def render(self):
        corners = []
        for part in self._parts():
            for point in part.corners():
                corners.append(point)

        min_x = 9999
        max_x = -9999
        min_y = 9999
        max_y = -9999

        for point in corners:
            x = point[0]
            y = point[1]

            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x

            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

        width = max_x - min_x
        height = max_y - min_y
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        for part in self._parts():
            part.draw(self.image, offset=(-min_x, -min_y))
        self.rect = self.image.get_rect(topleft=(min_x, min_y))
