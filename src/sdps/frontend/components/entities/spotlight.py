from sdps.config import SPOTLIGHT_COLOR
from sdps.frontend.components.shape import Shape


class Spotlight:
    def __init__(self, display, x, y_offset, width, height):
        self.display = display
        self.x = x
        self.y_offset = y_offset
        self.width = width
        self.height = height
        self.is_on = False

    def draw(self, bar_y):
        shape = Shape(self.display)
        x = self.x - self.width / 2
        y = bar_y + self.y_offset
        shape.draw_rectangle(x, y, self.width, self.height, SPOTLIGHT_COLOR)

    def toggle(self):
        self.is_on = not self.is_on