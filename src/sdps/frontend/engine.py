import pygame

from sdps.config import CONFETTI_PADDING_POS, CURTAINS_TIME, DARKNESS_ALPHA, FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from sdps.frontend.components.entities.confetti_cannon import ConfettiCannon
from sdps.frontend.components.entities.spotlight_rig import SpotlightRig
from sdps.frontend.components.scene.curtains import Curtains
from sdps.frontend.components.scene.floor import Floor
from sdps.frontend.components.shape import Shape


class Engine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.shape = Shape(self.screen, 20)
        self.background = pygame.Surface(self.screen.get_size())
        self.curtains_speed = (SCREEN_WIDTH / 2) / (CURTAINS_TIME * 1000)
        pygame.display.set_caption('Summer Dance Party School')

        self._init_scene()

    def _init_scene(self):
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        self.floor = Floor(self.screen.get_width(), self.screen.get_height() / 3,
                            self.screen.get_height() - self.screen.get_height() / 3)
        self.curtains = Curtains(self.screen.get_height())
        self.spotlight_rig = SpotlightRig(self.screen, self.screen.get_width(), 20,
                                          self.floor.y_offset + self.floor.height / 2)
        self.darkness = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.left_cannon = ConfettiCannon(self.screen, CONFETTI_PADDING_POS, SCREEN_HEIGHT - CONFETTI_PADDING_POS, 135)
        self.right_cannon = ConfettiCannon(self.screen, SCREEN_WIDTH - CONFETTI_PADDING_POS, SCREEN_HEIGHT - CONFETTI_PADDING_POS, 45)

    def run(self):
        start_ticks = pygame.time.get_ticks()

        while self.running:
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
                    elif key == pygame.K_w:
                        self.right_cannon.shoot()

            self.screen.blit(self.background, (0, 0))
            self.floor.draw(self.screen)
            self.spotlight_rig.draw(20)

            self.darkness.fill((0, 0, 0, DARKNESS_ALPHA))
            self.spotlight_rig.apply_darkness(self.darkness, 20)
            self.screen.blit(self.darkness, (0, 0))
            self.left_cannon.draw()
            self.right_cannon.draw()

            elapsed_ms = pygame.time.get_ticks() - start_ticks
            if elapsed_ms < CURTAINS_TIME * 1000:
                distance_moved = self.curtains_speed * elapsed_ms

                # Open curtains
                x = (SCREEN_WIDTH / 2) - distance_moved
                # Close curtains
                # x = distance_moved

                self.curtains.draw(self.screen, x)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
