from pygame import Vector2

from sdps.frontend.physics.physics_joint import PhysicsJoint
from sdps.frontend.physics.physics_point import PhysicsPoint


class Cloth:
    def __init__(self, width: int, height: int, spacing: int, start_x: int, start_y: int):
        self.gravity = Vector2(0, 981)
        self.drag = 0.01
        self.points: list[PhysicsPoint] = []
        self.joints: list[PhysicsJoint] = []

        for y in range(height):
            for x in range(width):
                point = PhysicsPoint(start_x + x * spacing, start_y + y * spacing)

                # Pin top corners and structural intervals along top edge
                if y == 0:
                    point.is_pinned = True

                if x > 0:
                    left_point = self.points[-1]
                    self.joints.append(PhysicsJoint(point, left_point, spacing))

                if y > 0:
                    up_point = self.points[x + (y - 1) * width]
                    self.joints.append(PhysicsJoint(point, up_point, spacing))

                self.points.append(point)

    def update(self, delta_time):
        # CRITICAL FIX 2: Sub-stepping
        # Divide the frame into smaller, highly stable chunks
        sub_steps = 5
        sub_dt = delta_time / sub_steps

        for _ in range(sub_steps):
            # Apply forces taking tiny steps
            for point in self.points:
                point.update(sub_dt, self.drag, self.gravity)

            # Because the steps are so small, we only need a few iterations
            # to maintain perfect rigidity
            for _ in range(3):
                for joint in self.joints:
                    joint.update()


    def draw(self, draw_surface):
        for joint in self.joints:
            joint.draw(draw_surface)

    def move_pinned_points(self, dx):
        for point in self.points:
            if point.is_pinned:
                point.init_pos.x += dx