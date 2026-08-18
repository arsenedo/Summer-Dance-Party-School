from sdps.config import SPOTLIGHT_COLOR
from sdps.frontend.components.shape import Shape

N_SPOTLIGHTS = 7

class SpotlightRig:
    def __init__(self, display, width, height):
        self.display = display
        self.width = width
        self.height = height

    def draw(self, y):
        x = self.display.get_width() / 2 - self.width / 2
        shape = Shape(self.display)
        shape.draw_rectangle(x, y, self.width, self.height, SPOTLIGHT_COLOR)

        spacing = self.width / N_SPOTLIGHTS
        w = 30
        h = 45
        for i in range(N_SPOTLIGHTS):
            c_x = x + spacing * (i + 0.5)
            rect_x = c_x - w / 2
            rect_y = y + self.height
            shape.draw_rectangle(rect_x, rect_y, w, h, SPOTLIGHT_COLOR)
