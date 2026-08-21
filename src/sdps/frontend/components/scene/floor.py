from sdps.config import FLOOR_COLOR, SCREEN_WIDTH
from sdps.frontend.components.shape import Shape


class Floor:
    def __init__(self, width=SCREEN_WIDTH, height=540, y_offset=540):
        self.width = width
        self.height = height
        self.y_offset = y_offset

    def draw(self, display):
        shape = Shape(display)
        shape.draw_rectangle(0, self.y_offset, self.width, self.height, FLOOR_COLOR)
