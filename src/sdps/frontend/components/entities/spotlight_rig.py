from sdps.config import SPOTLIGHT_COLOR, SPOTLIGHT_COLORS
from sdps.frontend.components.entities.spotlight import Spotlight
from sdps.frontend.components.shape import Shape

N_SPOTLIGHTS = 7

class SpotlightRig:
    def __init__(self, display, y, width, height, light_end_y):
        """initialize a spotlight rig

        Args:
            display: display surface
            width: width of the rig
            height: height of the rig
            light_end_y: y-coordinate of the light end
        """
        self.display = display
        self.y = y
        self.width = width
        self.height = height
        self.light_end_y = light_end_y
        self.spotlights = self._build_spotlights()

    def _build_spotlights(self):
        x = self.display.get_width() / 2 - self.width / 2
        spacing = self.width / N_SPOTLIGHTS
        spotlights = []
        for i in range(N_SPOTLIGHTS):
            c_x = x + spacing * (i + 0.5)
            spotlight = Spotlight(self.display, c_x, self.height, 30, 45,
                                  SPOTLIGHT_COLORS[i], self.light_end_y)
            spotlights.append(spotlight)
        return spotlights

    def toggle(self, i):
        self.spotlights[i].toggle()

    def apply_darkness(self, surface):
        shape = Shape(self.display)
        for spotlight in self.spotlights:
            if spotlight.is_on:
                light_coord, end_light_left, end_light_right = spotlight.light_points(self.y)
                shape.draw_triangle_on(surface, light_coord, end_light_left,
                                       end_light_right, (0, 0, 0, 0))

    def draw(self):
        x = self.display.get_width() / 2 - self.width / 2
        shape = Shape(self.display)
        shape.draw_rectangle(x, self.y, self.width, self.height, SPOTLIGHT_COLOR)

        for spotlight in self.spotlights:
            spotlight.draw(self.y)
