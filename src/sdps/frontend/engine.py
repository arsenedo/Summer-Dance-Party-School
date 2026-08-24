import random
from random import choice, randint

import pygame

from sdps.config import (
    CONFETTI_PADDING_POS,
    CURTAINS_TIME,
    DARKNESS_ALPHA,
    FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from sdps.frontend.components.entities.confetti_cannon import ConfettiCannon
from sdps.frontend.components.entities.particles import (
    FloatingParticle,
    Particle,
)
from sdps.frontend.components.entities.spotlight_rig import SpotlightRig
from sdps.frontend.components.scene.curtains import Curtains
from sdps.frontend.components.scene.floor import Floor
from sdps.frontend.components.shape import Shape


class Engine:
    dt = 0

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.shape = Shape(self.screen, 20)
        self.background = pygame.Surface(self.screen.get_size())
        self.curtains_speed = 500

        self.particle_group = pygame.sprite.Group()
        self.floating_particle_timer = pygame.event.custom_type()
        pygame.time.set_timer(self.floating_particle_timer, 10)

        pygame.display.set_caption('Summer Dance Party School')

        self._init_scene()

    def _init_scene(self):
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        self.floor = Floor(self.screen.get_width(), self.screen.get_height() / 3,
                            self.screen.get_height() - self.screen.get_height() / 3)
        self.curtains = Curtains(self.screen.get_width(), self.screen.get_height())
        self.spotlight_rig = SpotlightRig(self.screen, 20, self.screen.get_width(), 20,
                                          self.floor.y_offset + self.floor.height / 2)
        self.darkness = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.left_cannon = ConfettiCannon(self.screen, CONFETTI_PADDING_POS,
         SCREEN_HEIGHT - CONFETTI_PADDING_POS, 135)
        self.right_cannon = ConfettiCannon(self.screen,
                                           SCREEN_WIDTH - CONFETTI_PADDING_POS,
                                           SCREEN_HEIGHT - CONFETTI_PADDING_POS, 45)

    def run(self):
        start_ticks = pygame.time.get_ticks()

        while self.running:
            self._iterate_events()
            self.screen.blit(self.background, (0, 0))
            self.floor.draw(self.screen)
            self.spotlight_rig.draw()

            self.darkness.fill((0, 0, 0, DARKNESS_ALPHA))
            self.spotlight_rig.apply_darkness(self.darkness)
            self.screen.blit(self.darkness, (0, 0))
            self.left_cannon.draw()
            self.right_cannon.draw()

            self._update_curtains(self.dt)

            self.particle_group.draw(self.screen)
            self.particle_group.update(self.dt)

            pygame.display.flip()
            self.dt = self.clock.tick(FPS) / 1000

        pygame.quit()

    def _iterate_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                key = event.key
                if pygame.K_1 <= key <= pygame.K_7:
                    i = key - pygame.K_1
                    self.spotlight_rig.toggle(i)
                elif key == pygame.K_q:
                    self.left_cannon.shoot()
                    x = self.left_cannon.x + self.left_cannon.body_size / 2
                    y = (self.left_cannon.y - self.left_cannon.body_size
                         - self.left_cannon.barrel_length / 2)
                    self._shoot_confetti(1000, (x, y), 1)
                elif key == pygame.K_w:
                    self.right_cannon.shoot()
                    x = self.right_cannon.x - self.right_cannon.body_size / 2
                    y = (self.right_cannon.y - self.right_cannon.body_size
                         - self.right_cannon.barrel_length / 2)
                    self._shoot_confetti(1000, (x, y), -1)
            elif event.type == self.floating_particle_timer:
                self._spawn_floating_particle()

    def _shoot_confetti(self, n: int, pos: tuple[int, int], side: int):
        """shoot confettis from a position

        Args:
            n (int): number of particles to spawn
            pos (tuple[int, int]): position to spawn particles
            side (int): direction to throw particles (-1: to the left, 1: to the right)
        """
        for _ in range(n):
            color = choice(("red", "green", "blue"))
            direction = pygame.math.Vector2(random.gauss(side, 0.25),
                                            random.gauss(-1, 0.25))
            direction = direction.normalize()
            speed = random.gauss(1200, 300)
            Particle(self.particle_group, pos, color, direction, speed)

    def _spawn_floating_particle(self):
        spotlights = self.spotlight_rig.spotlights
        for spotlight in spotlights:
            if spotlight.is_on and random.randint(0, 100) > 99:
                init_pos = (spotlight.x,
                            self.spotlight_rig.y * 2 + spotlight.y_offset
                            + spotlight.height)
                pos = init_pos[0] + randint(-10, 10), init_pos[1] + randint(-10, 10)
                color = "white"
                direction = pygame.math.Vector2(0, 1)
                speed = randint(50, 100)
                particle = FloatingParticle(self.particle_group, pos, color, direction, speed)
                spotlight.particles_group.add(particle)

    def _update_curtains(self, dt):
        dt_adjusted_speed = self.curtains_speed * dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.curtains.move_curtains((-dt_adjusted_speed, dt_adjusted_speed))
        if keys[pygame.K_DOWN]:
            self.curtains.move_curtains((dt_adjusted_speed, -dt_adjusted_speed))
        self.curtains.update(dt)
        self.curtains.draw(self.screen)
