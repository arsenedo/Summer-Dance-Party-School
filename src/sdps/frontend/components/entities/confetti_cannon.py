from sdps.config import CONFETTI_CANNON_COLOR
from sdps.frontend.components.shape import Shape


class ConfettiCannon:
    def __init__(self, display, x, y, angle, color=CONFETTI_CANNON_COLOR):
        self.display = display
        self.x = x
        self.y = y
        self.angle = angle
        self.color = color
        self.body_size = 60
        self.barrel_width = 18
        self.barrel_length = 70

    def draw(self):
        shape = Shape(self.display)
        body_x = self.x - self.body_size / 2
        body_y = self.y - self.body_size
        shape.draw_rectangle(body_x, body_y, self.body_size, self.body_size, self.color)
        shape.draw_rotated_rectangle(
            self.x,
            self.y - self.body_size / 2 - self.barrel_length / 2,
            self.barrel_width,
            self.barrel_length,
            self.angle,
            self.color,
        )

    def shoot(self):
        print("Boom")
