import pygame

from sdps.config import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from sdps.frontend.curtains import Curtains
from sdps.frontend.floor import Floor


class Engine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.background = pygame.Surface(self.screen.get_size())
        pygame.display.set_caption('Summer Dance Party School')

        self._init_scene_()

    def _init_scene_(self):
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        self.floor = Floor(self.screen.get_width(), self.screen.get_height() / 3,
                            self.screen.get_height() - self.screen.get_height() / 3)
        self.curtains = Curtains(self.screen.get_height())

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.blit(self.background, (0, 0))
            self.floor.draw(self.screen)
            self.curtains.draw(self.screen, 100)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
