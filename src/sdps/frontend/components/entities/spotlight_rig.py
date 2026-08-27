from sdps.config import LASER_COUNT_PER_SPOTLIGHT, SPOTLIGHT_COLOR, SPOTLIGHT_COLORS
from sdps.frontend.components.entities.spotlight import Spotlight
from sdps.frontend.components.shape import Shape

N_SPOTLIGHTS = 7

class SpotlightRig:
    def __init__(self, display, y, width, height, light_end_y,
                 floor_top_y=None, floor_bottom_y=None):
        """initialize a spotlight rig

        Args:
            display: display surface
            y: y-coordinate of the top of the rig bar
            width: width of the rig
            height: height of the rig
            light_end_y: y-coordinate of the light end
            floor_top_y: smallest y a beam may land on (defaults to light_end_y)
            floor_bottom_y: largest y a beam may land on (defaults to light_end_y)
        """
        self.display = display
        self.y = y
        self.width = width
        self.height = height
        self.light_end_y = light_end_y
        self.floor_top_y = light_end_y if floor_top_y is None else floor_top_y
        self.floor_bottom_y = light_end_y if floor_bottom_y is None else floor_bottom_y
        self.shape = Shape(display)
        self.spotlights = self._build_spotlights()

    def _build_spotlights(self):
        x = self.display.get_width() / 2 - self.width / 2
        spacing = self.width / N_SPOTLIGHTS
        spotlights = []
        for i in range(N_SPOTLIGHTS):
            c_x = x + spacing * (i + 0.5)
            color = SPOTLIGHT_COLORS[i % len(SPOTLIGHT_COLORS)]
            spotlight = Spotlight(self.display, c_x, self.height, 30, 45,
                                  color, self.light_end_y)
            spotlights.append(spotlight)
        return spotlights

    def turn_on(self, i):
        self.spotlights[i].turn_on()

    def turn_off(self, i):
        self.spotlights[i].turn_off()

    def toggle(self, i):
        self.spotlights[i].toggle()

    def fire_lasers(self, i):
        self.spotlights[i].fire_lasers(self.y, self.floor_top_y,
                                       self.floor_bottom_y,
                                       LASER_COUNT_PER_SPOTLIGHT)

    def draw_lasers_on(self, surface):
        for spotlight in self.spotlights:
            if spotlight.is_on:
                spotlight.draw_lasers_on(surface)

    def apply_darkness(self, surface):
        for spotlight in self.spotlights:
            if spotlight.is_on:
                lc, ell, elr = spotlight.light_points(self.y)
                self.shape.draw_triangle_on(
                    surface, lc, ell, elr, (0, 0, 0, 0)
                )

    def draw(self):
        x = self.display.get_width() / 2 - self.width / 2
        self.shape.draw_rectangle(x, self.y, self.width, self.height, SPOTLIGHT_COLOR)

        for spotlight in self.spotlights:
            spotlight.draw(self.y)
