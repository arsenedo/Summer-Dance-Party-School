def make_pose(arm_left, arm_right, leg_left, leg_right):
    return (arm_left, arm_right, leg_left, leg_right)

class Dance:
    def __init__(self, poses, step_duration=0.35):
        self.poses = poses
        self.step_duration = step_duration


IDLE_POSE = P(0, 0, 0, 0)

DANCES = [
    Dance([make_pose(0, 0, 0, 0), make_pose(-8, 8, 0, 0)], 0.50),
    Dance([make_pose(-170, 170, 0, 0), make_pose(-150, 150, -5, 5)], 0.35),
    Dance([make_pose(-90, 90, 0, 0), make_pose(-100, 80, -8, 8)], 0.40),
    Dance([make_pose(-150, 20, 0, 10), make_pose(-20, 150, -10, 0)], 0.30),
    Dance([make_pose(0, 0, 0, 0), make_pose(-135, 135, -30, 30)], 0.25),
    Dance([make_pose(-160, 30, 0, 0), make_pose(-120, 30, 0, 0)], 0.25),
    Dance([make_pose(-90, 0, 0, 0), make_pose(0, 90, 0, 0)], 0.30),
    Dance([make_pose(-45, 45, 0, 0), make_pose(-45, 45, -70, 0), make_pose(-45, 45, 0, 70)], 0.28), 
    Dance([make_pose(-60, 60, -25, 25), make_pose(-60, 60, 25, -25)], 0.22),
    Dance([make_pose(-30, 30, -10, 10), make_pose(30, -30, 10, -10)], 0.20),
    Dance([make_pose(-90, 90, 0, 0), make_pose(-90, 150, 0, 0), make_pose(-90, 90, -10, 10)], 0.30),
    Dance([make_pose(-120, 120, -20, 20), make_pose(-60, 60, 20, -20)], 0.30),
]
