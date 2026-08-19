import random

import pygame

from sdps.backend import InstrumentType
from sdps.config import (
    CONFETTI_PADDING_POS,
    CURTAINS_TIME,
    DANCER_COLORS,
    DANCER_X_PADDING,
    DANCER_Y_PADDING,
    DARKNESS_ALPHA,
    FPS,
    MAX_DANCERS,
    MP3_FILENAME,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from sdps.frontend.components.entities.confetti_cannon import ConfettiCannon
from sdps.frontend.components.entities.dancer import Dancer
from sdps.frontend.components.entities.particles import (
    FloatingParticle,
    Particle,
)
from sdps.frontend.components.entities.spotlight_rig import SpotlightRig
from sdps.frontend.components.scene.curtains import Curtains
from sdps.frontend.components.scene.floor import Floor


class Engine:
    dt = 0

    def __init__(self, note_list):
        try:
            pygame.mixer.init()
        # wsl drivers problems
        except pygame.error:
            import os
            for driver in ("pulse", "alsa", "sdl", "dummy"):
                try:
                    os.environ["SDL_AUDIODRIVER"] = driver
                    pygame.mixer.init()
                    break
                except pygame.error:
                    continue
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.opening = True
        self.background = pygame.Surface(self.screen.get_size())
        self.curtains_speed = 150
        self.curtains_offset = 0
        self.music_ended = False
        self.max_curtain_offset = (SCREEN_WIDTH / 2 ) - 100
        self.note_list = note_list

        self.note_events = self._build_note_events(note_list)
        self.next_event_index = 0
        self.active_note_counts = {}

        self.particle_group = pygame.sprite.Group()
        self.dancer_group = pygame.sprite.Group()
        self.floating_particle_timer = pygame.event.custom_type()
        pygame.time.set_timer(self.floating_particle_timer, 10)

        pygame.display.set_caption('Summer Dance Party School')

        self._init_scene()

    def _init_scene(self):
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((0, 0, 0))
        self.floor = Floor(self.screen.get_width(), self.screen.get_height() / 3,
                            self.screen.get_height() - self.screen.get_height() / 3)
        self.curtains = Curtains(self.screen.get_width(), self.screen.get_height())
        self.spotlight_rig = SpotlightRig(self.screen, 20, self.screen.get_width(), 20,
                                          self.floor.y_offset + self.floor.height / 2,
                                          self.floor.y_offset,
                                          self.floor.y_offset + self.floor.height)
        self.darkness = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.laser_layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT),
                                          pygame.SRCALPHA)
        self.left_cannon = ConfettiCannon(self.screen, CONFETTI_PADDING_POS,
         SCREEN_HEIGHT - CONFETTI_PADDING_POS, 135)
        self.right_cannon = ConfettiCannon(self.screen,
                                           SCREEN_WIDTH - CONFETTI_PADDING_POS,
                                           SCREEN_HEIGHT - CONFETTI_PADDING_POS, 45)

    def run(self):

        self.opening_timer = pygame.event.custom_type()
        self.closing_timer = pygame.event.custom_type()

        self.music_end_event = pygame.event.custom_type()
        pygame.mixer.music.set_endevent(self.music_end_event)
        pygame.time.set_timer(self.opening_timer, 5000)

        self.clock.tick(FPS)

        pygame.mixer.music.load(f"./assets/sounds/{MP3_FILENAME}")

        time = random.randrange(0, 50, 1)
        curtains_moove = False

        while self.running:
            if self.opening or self.music_ended:
                time = time - 1
                if time <=0:
                    curtains_moove = not curtains_moove
                    if curtains_moove :
                        time = random.randrange(25, 70, 1)
                    else:
                        time = random.randrange(50, 250, 1)
                if not curtains_moove and self.opening:
                    self._update_curtains(self.dt, "open")
                elif self.music_ended:
                    self._update_curtains(self.dt, "close")
            else:
                elapsed_time = pygame.mixer.music.get_pos() / 1000
                self._check_notes(elapsed_time)
                self._update_curtains(self.dt, "")


            self._iterate_events()
            self.screen.blit(self.background, (0, 0))
            self.floor.draw(self.screen)
            self.spotlight_rig.draw()

            self.darkness.fill((0, 0, 0, DARKNESS_ALPHA))
            self.spotlight_rig.apply_darkness(self.darkness)
            self.screen.blit(self.darkness, (0, 0))

            self.laser_layer.fill((0, 0, 0, 0))
            self.spotlight_rig.draw_lasers_on(self.laser_layer)
            self.screen.blit(self.laser_layer, (0, 0))

            self.left_cannon.draw()
            self.right_cannon.draw()

            self._update_curtains(self.dt, "")

            self.particle_group.update(self.dt)
            self.particle_group.draw(self.screen)

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
                    self.active_note_counts[i] = 0
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
            elif event.type == pygame.QUIT:
                self.opening = False
                self.running = False
            elif event.type == self.music_end_event:
                print("Music ended !")
                self.music_ended = True
            elif event.type == self.opening_timer:
                print("Pre-start")
                pygame.time.set_timer(self.opening_timer, 0)
                pygame.mixer.music.play()
                self.opening = False

    def _manage_lights(self, note, turn_on):
        index = note.index
        if not 0 <= index < len(self.spotlight_rig.spotlights):
            return

        count = self.active_note_counts.get(index, 0)
        if turn_on:
            self.active_note_counts[index] = count + 1
            if count == 0:
                self.spotlight_rig.turn_on(index)
            if note.is_half_note:
                self.spotlight_rig.fire_lasers(index)
        else:
            count = max(0, count - 1)
            self.active_note_counts[index] = count
            if count == 0:
                self.spotlight_rig.turn_off(index)

    def _manage_dancers(self, note, turn_on):
        pass

    def _manage_notes_event(self, note, turn_on):
        if note.instrument == InstrumentType.PIANO:
            self._manage_lights(note, turn_on)
        else:
            self._manage_dancers(note, turn_on)

    def _build_note_events(self, note_list):
        events = []
        for note in note_list:
            events.append((note.start, note, True))
            events.append((note.end, note, False))
        events.sort(key=lambda e: (e[0], e[2]))
        return events

    def _check_notes(self, elapsed_time):
        while self.next_event_index < len(self.note_events):
            event_time, note, turn_on = self.note_events[self.next_event_index]
            if event_time > elapsed_time:
                break
            self._manage_notes_event(note, turn_on)
            self.next_event_index += 1

    def _spawn_dancer(self):
        if len(self.dancer_group) >= MAX_DANCERS:
            self.dancer_group.sprites()[0].kill()

        x = randint(DANCER_X_PADDING, SCREEN_WIDTH - DANCER_X_PADDING)
        floor_top = self.floor.y_offset + DANCER_Y_PADDING
        floor_bottom = SCREEN_HEIGHT - DANCER_Y_PADDING
        y = randint(floor_top, floor_bottom)
        color = choice(DANCER_COLORS)
        Dancer(self.dancer_group, (x, y), color)

    def _shoot_confetti(self, n: int, pos: tuple[int, int], side: int):
        """shoot confettis from a position

        Args:
            n (int): number of particles to spawn
            pos (tuple[int, int]): position to spawn particles
            side (int): direction to throw particles (-1: to the left, 1: to the right)
        """
        for _ in range(n):
            color = random.choice(("red", "green", "blue"))
            direction = pygame.math.Vector2(random.gauss(side, 0.25),
                                            random.gauss(-1, 0.25))
            direction = direction.normalize()
            speed = random.gauss(1200, 300)
            Particle(self.particle_group, pos, color, direction, speed)

    def _spawn_floating_particle(self):
        spotlights = self.spotlight_rig.spotlights
        for spotlight in spotlights:
            if spotlight.is_on and random.randint(0, 100) > 99:
                init_pos = spotlight.emitter_point(self.spotlight_rig.y)
                jx = random.randint(-10, 10)
                jy = random.randint(-10, 10)
                pos = init_pos[0] + jx, init_pos[1] + jy
                color = "white"
                direction = pygame.math.Vector2(0, 1)
                speed = random.randint(50, 100)
                particle = FloatingParticle(
                    self.particle_group, pos, color, direction, speed
                )
                spotlight.particles_group.add(particle)

    def _update_curtains(self, dt, state):
        dt_adjusted_speed = self.curtains_speed * dt
        keys = pygame.key.get_pressed()

        if state == "open" and self.curtains_offset < self.max_curtain_offset:
            self.curtains.move_curtains((-dt_adjusted_speed, dt_adjusted_speed))
            move = min(dt_adjusted_speed, self.max_curtain_offset - self.curtains_offset)
            self.curtains.move_curtains((-move, move))
            self.curtains_offset += move

        if state == "close" and self.curtains_offset > 0:
            self.curtains.move_curtains((dt_adjusted_speed, -dt_adjusted_speed))
            move = min(dt_adjusted_speed, self.curtains_offset)
            self.curtains.move_curtains((move, -move))
            self.curtains_offset -= move
        if state == "close" and self.curtains_offset <= 0:
            self.running = False

        if keys[pygame.K_UP]:
            self.curtains.move_curtains((-dt_adjusted_speed, dt_adjusted_speed))
        if keys[pygame.K_DOWN]:
            self.curtains.move_curtains((dt_adjusted_speed, -dt_adjusted_speed))
        self.curtains.update(dt)
        self.curtains.draw(self.screen)
