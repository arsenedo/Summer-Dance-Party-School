
from sdps.config import CURTAINS_COLOR, SCREEN_HEIGHT
from sdps.frontend.components.shape import Shape


class Curtains:
    def __init__(self, height=SCREEN_HEIGHT):
        self.height = height

    def draw(self, display, width):
        w = display.get_width()
        shape = Shape(display)
        shape.draw_rectangle(0, 0, width, self.height, CURTAINS_COLOR)
        shape.draw_rectangle(w - width, 0, width, self.height, CURTAINS_COLOR)
