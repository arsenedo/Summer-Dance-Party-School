import pygame

from sdps.config import CURTAINS_TIME, FPS, SCREEN_HEIGHT, SCREEN_WIDTH
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
        self.spotlight_rig = SpotlightRig(self.screen, self.screen.get_width(), 20)

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

            self.screen.blit(self.background, (0, 0))
            self.floor.draw(self.screen)
            self.shape.draw_rectangle(100, 100, 200, 150, (0, 255, 0))
            self.shape.draw_circle(300, 300, 50, (0, 0, 255))
            self.shape.draw_triangle((400, 250), (450, 300), (350, 300), (255, 255, 0))

            self.spotlight_rig.draw(20)

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
