# With the help of this tutorial: https://www.youtube.com/watch?v=ZiPWN39mGM0

import pygame

from sdps.config import SCREEN_HEIGHT, SCREEN_WIDTH
from sdps.frontend.components.shape import Shape


class Particle(pygame.sprite.Sprite):
    def __init__(self,
                 groups: pygame.sprite.Group,
                 pos: list[int],
                 color: str,
                 direction: pygame.math.Vector2,
                 speed: int):
        super().__init__(groups)
        self.pos = pos
        self.color = color
        self.direction = direction
        self.speed = speed
        self.alpha = 255
        self.fade_speed = 200
        self.size = 4
        self.velocity_vector = self.direction * self.speed
        self.gravity = 1000

        self.create_surf()

    def create_surf(self):
        self.image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.image.set_colorkey("black")
        Shape(self.image).draw_circle(self.size / 2, self.size / 2, self.size / 2,
                                      self.color)
        self.rect = self.image.get_rect(center=self.pos)

    def move(self, dt):
        self.velocity_vector.y += self.gravity * dt
        self.pos += self.velocity_vector * dt
        self.rect.center = self.pos

    def fade(self, dt):
        self.alpha -= self.fade_speed * dt
        self.image.set_alpha(self.alpha)

    def check_pos(self):
        if (
            self.pos[0] < -50 or
            self.pos[0] > SCREEN_WIDTH + 50 or
            self.pos[1] < -50 or
            self.pos[1] > SCREEN_HEIGHT + 50
        ):
            self.kill()

    def check_alpha(self):
        if self.alpha <= 0:
            self.kill()

    def update(self, dt):
        self.move(dt)
        self.fade(dt)
        self.check_pos()
        self.check_alpha()


class FloatingParticle(Particle):
    def __init__(self,
                 groups: pygame.sprite.Group,
                 pos: list[int],
                 color: str,
                 direction: pygame.math.Vector2,
                 speed: int):
        super().__init__(groups, pos, color, direction, speed)
