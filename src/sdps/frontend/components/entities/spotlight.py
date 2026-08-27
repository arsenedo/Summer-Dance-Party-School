import pygame

from sdps.config import SPOTLIGHT_ALPHA, SPOTLIGHT_COLOR, SPOTLIGHT_LIGHT_HALF_WIDTH
from sdps.frontend.components.entities.laser import Laser
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
        self.particles_group = pygame.sprite.Group()
        self.shape = Shape(display)
        self.lasers = []

    def emitter_point(self, bar_y):
        return (self.x, bar_y + self.y_offset + self.height)

    def light_points(self, bar_y):
        light_coord = self.emitter_point(bar_y)
        end_light_left = (self.x - SPOTLIGHT_LIGHT_HALF_WIDTH, self.light_end_y)
        end_light_right = (self.x + SPOTLIGHT_LIGHT_HALF_WIDTH, self.light_end_y)
        return light_coord, end_light_left, end_light_right

    def draw(self, bar_y):
        x = self.x - self.width / 2
        y = bar_y + self.y_offset
        if self.is_on:
            light_coord, end_light_left, end_light_right = self.light_points(bar_y)
            self.shape.draw_triangle_alpha(light_coord, end_light_left, end_light_right,
                                       self.color, SPOTLIGHT_ALPHA)
        self.shape.draw_rectangle(x, y, self.width, self.height, SPOTLIGHT_COLOR)

    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False
        self.clear_lasers()
        for particle in self.particles_group.sprites():
            particle.kill()

    def toggle(self):
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()

    def fire_lasers(self, bar_y, floor_top_y, floor_bottom_y, count):
        apex = self.emitter_point(bar_y)
        self.lasers = [
            Laser(apex, floor_top_y, floor_bottom_y, self.color)
            for _ in range(count)
        ]

    def clear_lasers(self):
        self.lasers = []

    def draw_lasers_on(self, surface):
        for laser in self.lasers:
            laser.draw_on(surface, self.shape)
