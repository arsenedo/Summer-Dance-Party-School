import math
import pygame
from pygame import Vector2

class Point:
    def __init__(self, x, y):
        self.pos = Vector2(x, y)
        self.prev_pos = Vector2(x, y)
        self.init_pos = Vector2(x, y)
        self.is_pinned = False

    def update(self, delta_time, drag, acceleration):
        if self.is_pinned:
            self.pos = Vector2(self.init_pos)
            return

        velocity = (self.pos - self.prev_pos) * (1 - drag)
        new_pos = self.pos + velocity + acceleration * (delta_time ** 2)
        self.prev_pos = Vector2(self.pos)
        self.pos = new_pos


class Stick:
    def __init__(self, p1: Point, p2: Point, length: float):
        self.p1 = p1
        self.p2 = p2
        self.length = length
        self.is_active = True

    def update(self):
        if not self.is_active:
            return

        diff = self.p1.pos - self.p2.pos
        dist = diff.length()
        if dist == 0:
            return

        diff_factor = (self.length - dist) / dist
        offset = diff * diff_factor * 0.5

        # Only displace points that are not pinned
        if not self.p1.is_pinned and not self.p2.is_pinned:
            self.p1.pos += offset
            self.p2.pos -= offset
        elif not self.p1.is_pinned:
            self.p1.pos += offset * 2.0
        elif not self.p2.is_pinned:
            self.p2.pos -= offset * 2.0

    def draw(self, screen):
        if self.is_active:
            pygame.draw.line(screen, (220, 220, 220), self.p1.pos, self.p2.pos, 1)


class Cloth:
    def __init__(self, width: int, height: int, spacing: int, start_x: int, start_y: int):
        self.gravity = Vector2(0, 981)
        self.drag = 0.01
        self.points: list[Point] = []
        self.sticks = []

        for y in range(height):
            for x in range(width):
                point = Point(start_x + x * spacing, start_y + y * spacing)

                # Pin top corners and structural intervals along top edge
                if y == 0 and (x == 0 or x == width - 1 or x % 5 == 0):
                    point.is_pinned = True

                if x > 0:
                    left_point = self.points[-1]
                    self.sticks.append(Stick(point, left_point, spacing))

                if y > 0:
                    up_point = self.points[x + (y - 1) * width]
                    self.sticks.append(Stick(point, up_point, spacing))

                self.points.append(point)

    def update(self, delta_time):
        for point in self.points:
            point.update(delta_time, self.drag, self.gravity)

        # Run relaxation iterations to prevent stretchy rubber-band behavior
        for _ in range(5):
            for stick in self.sticks:
                stick.update()

    def draw(self, draw_surface):
        for stick in self.sticks:
            stick.draw(draw_surface)


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
cloth = Cloth(35, 25, 15, 375, 100)

cloth_pos_offset = Vector2(0, 0)

running = True
while running:
    dt = clock.tick(60) / 1000.0
    dt = min(dt, 0.033)  # Clamp delta_time to avoid physics explosions on frame lag

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    direction = 0
    if keys[pygame.K_a]:
        direction -= 300 * dt
    if keys[pygame.K_d]:
        direction += 300 * dt

    for idx, point in enumerate(cloth.points):
        if idx >= 35:
            break
        point.pos.x += direction
        point.init_pos = point.pos

    screen.fill((30, 30, 40))
    cloth.update(dt)
    cloth.draw(screen)

    pygame.display.flip()

pygame.quit()