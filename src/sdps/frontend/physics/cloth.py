from pygame import Vector2
from pygame.draw_py import Point
from sklearn import neighbors

from sdps.frontend.components import Shape
from sdps.frontend.physics.physics_joint import PhysicsJoint
from sdps.frontend.physics.physics_point import PhysicsPoint


class Cloth:
    iterations = 1
    drag = 0.25 * (10 ** -iterations)

    def __init__(self, width: int, height: int, spacing: int, start_x: int, start_y: int):
        self.gravity = Vector2(0, 5000)
        self.points: list[PhysicsPoint] = []
        self.joints: list[PhysicsJoint] = []
        self.width = width
        self.height = height

        for y in range(height):
            for x in range(width):
                point = PhysicsPoint(start_x + x * spacing, start_y + y * spacing)

                # Pin top corners and structural intervals along top edge
                if y == 0:
                    point.is_pinned = True

                if x > 0:
                    left_point = self.points[-1]
                    point.l_neighbor = left_point
                    self.joints.append(PhysicsJoint(point, left_point, spacing))

                if y > 0:
                    up_point = self.points[x + (y - 1) * width]
                    point.r_neighbor = up_point
                    self.joints.append(PhysicsJoint(point, up_point, spacing))

                self.points.append(point)

    def update(self, delta_time):
        sub_delta = min(0.005, delta_time) / self.iterations

        for _ in range(self.iterations):
            for point in self.points:
                point.update(sub_delta, self.drag, self.gravity)
            for joint in self.joints:
                joint.update()

    def draw(self, draw_surface):
        shape = Shape(draw_surface)
        for y in range(self.height - 1):
            for x in range(self.width - 1):
                point = self.points[x + y * self.width]
                neighbors = [
                    self.points[x + 1 + y * self.width],
                    self.points[x + (y + 1) * self.width]
                ]
                shape.draw_triangle(
                    Point(point.pos.x, point.pos.y),
                    Point(neighbors[0].pos.x, neighbors[0].pos.y),
                    Point(neighbors[1].pos.x, neighbors[1].pos.y),
                    (150, 0, 0)
                )


        for y in range(1, self.height):
            for x in range(1, self.width):
                point = self.points[x + y * self.width]
                neighbors = [
                    self.points[x - 1 + y * self.width],
                    self.points[x + (y - 1) * self.width]
                ]
                shape.draw_triangle(
                    Point(point.pos.x, point.pos.y),
                    Point(neighbors[0].pos.x, neighbors[0].pos.y),
                    Point(neighbors[1].pos.x, neighbors[1].pos.y),
                    (200, 50, 0)
                )

    def move_pinned_points(self, dx):
        for point in self.points:
            if point.is_pinned:
                point.init_pos.x += dx