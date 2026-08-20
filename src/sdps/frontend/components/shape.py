import math

import pygame
from pygame.draw_py import Point


class Shape:
    def __init__(self, display, n_triangles=20):
        """Generate shapes with triangles

        Args:
            display: surface to draw on
            n_triangles (int, optional): More triangles -> cleaner circle.
                                         Defaults to 20.
        """
        self.display = display
        self.n_triangles = n_triangles

    def draw_rectangle(self, x, y, w, h, color=(255, 0, 0)):
        pygame.draw.polygon(self.display, color, [(x, y), (x + w, y), (x, y + h)])
        pygame.draw.polygon(
            self.display, color, [(x + w, y + h), (x + w, y), (x, y + h)]
        )

    def draw_circle(self, x, y, r, color):
        for i in range(self.n_triangles):
            theta1 = (2 * math.pi * i) / self.n_triangles
            theta2 = (2 * math.pi * (i + 1)) / self.n_triangles
            x1 = x + r * math.cos(theta1)
            y1 = y + r * math.sin(theta1)
            x2 = x + r * math.cos(theta2)
            y2 = y + r * math.sin(theta2)
            pygame.draw.polygon(self.display, color, [(x, y), (x1, y1), (x2, y2)])

    def draw_triangle(self, p1: Point, p2: Point, p3: Point, color):
        pygame.draw.polygon(self.display, color, [p1, p2, p3])

    # https://stackoverflow.com/questions/36510795/rotating-a-rectangle-not-image-in-pygame
    def draw_rotated_rectangle(self, x, y, width, height, angle_deg, color):
        points = self.rotated_rectangle_points(x, y, width, height, angle_deg)
        pygame.draw.polygon(self.display, color, points)

    def rotated_rectangle_points(self, x, y, width, height, angle_deg):
        radius = math.sqrt((height / 2) ** 2 + (width / 2) ** 2)
        angle = math.atan2(height / 2, width / 2)
        angles = [angle, -angle + math.pi, angle + math.pi, -angle]
        rot_radians = (math.pi / 180) * angle_deg
        points = []
        for a in angles:
            y_offset = -1 * radius * math.sin(a + rot_radians)
            x_offset = radius * math.cos(a + rot_radians)
            points.append((x + x_offset, y + y_offset))
        return points

    # https://stackoverflow.com/questions/6339057/draw-transparent-rectangles-and-polygons-in-pygame
    def draw_triangle_alpha(self, p1, p2, p3, color, alpha):
        points = [p1, p2, p3]

        # we search a surface that only covers the triangle
        min_x = min(p[0] for p in points)
        max_x = max(p[0] for p in points)
        min_y = min(p[1] for p in points)
        max_y = max(p[1] for p in points)

        surface = pygame.Surface((max_x - min_x, max_y - min_y), pygame.SRCALPHA)
        pygame.draw.polygon(
            surface,
            (color[0], color[1], color[2], alpha),
            [(p[0] - min_x, p[1] - min_y) for p in points],
        )
        self.display.blit(surface, (min_x, min_y))

    def draw_triangle_on(self, surface, p1, p2, p3, color):
        pygame.draw.polygon(surface, color, [p1, p2, p3])
