
from sdps.config import CURTAINS_COLOR, SCREEN_HEIGHT, SCREEN_WIDTH
from sdps.frontend.components.shape import Shape
from sdps.frontend.physics.cloth import Cloth

class Curtains:
    spacing = 15
    def __init__(self, screen_width = SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        self.curtain_width = screen_width // 2
        self.curtain_height = screen_height // 2

        start_x = 200
        start_y = 200

        self.left_curtain = Cloth(
            self.curtain_width // self.spacing,
            self.curtain_height // self.spacing,
            self.spacing,
            10,
            start_y,
        )

        self.right_curtain = Cloth(
            self.curtain_width // self.spacing,
            self.curtain_height // self.spacing,
            self.spacing,
            screen_width // 2,
            start_y
        )

    def update(self, dt):
        self.left_curtain.update(dt)
        self.right_curtain.update(dt)

    def draw(self, display):
        self.left_curtain.draw(display)
        self.right_curtain.draw(display)

    def move_curtains(self, dx):
        self.left_curtain.move_pinned_points(dx[0])
        self.right_curtain.move_pinned_points(dx[1])