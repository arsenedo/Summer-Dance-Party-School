from sdps.config import SPOTLIGHT_ALPHA, SPOTLIGHT_LIGHT_HALF_WIDTH, SPOTLIGHT_COLOR
from sdps.frontend.components.shape import Shape


class Spotlight:
    def __init__(self, display, x, y_offset, width, height, color, light_end_y):
        self.display = display
        self.x = x
        self.y_offset = y_offset
        self.width = width
        self.height = height
        self.color = color
        self.light_end_y = light_end_y
        self.is_on = False

    def beam_points(self, bar_y):
        y = bar_y + self.y_offset
        light_coord = (self.x, y + self.height)
        end_light_left = (self.x - SPOTLIGHT_LIGHT_HALF_WIDTH, self.light_end_y)
        end_light_right = (self.x + SPOTLIGHT_LIGHT_HALF_WIDTH, self.light_end_y)
        return light_coord, end_light_left, end_light_right

    def draw(self, bar_y):
        shape = Shape(self.display)
        x = self.x - self.width / 2
        y = bar_y + self.y_offset
        if self.is_on:
            light_coord, end_light_left, end_light_right = self.beam_points(bar_y)
            shape.draw_triangle_alpha(light_coord, end_light_left, end_light_right, self.color, SPOTLIGHT_ALPHA)
        shape.draw_rectangle(x, y, self.width, self.height, SPOTLIGHT_COLOR)

    def toggle(self):
        self.is_on = not self.is_on