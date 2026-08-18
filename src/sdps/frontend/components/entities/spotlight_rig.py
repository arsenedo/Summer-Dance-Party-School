from sdps.config import SPOTLIGHT_COLOR
from sdps.frontend.components.shape import Shape


class SpotlightRig:
    def __init__(self, display, width, height):
        self.display = display
        self.width = width
        self.height = height

    def draw(self, y):
        x = self.display.get_width() / 2 - self.width / 2
        shape = Shape(self.display)
        shape.draw_rectangle(x, y, self.width, self.height, SPOTLIGHT_COLOR)
