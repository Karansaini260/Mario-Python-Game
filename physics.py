"""Pure-physics helpers for the platformer (testable without a display)."""


class Physics:
    def __init__(self, gravity=900.0, jump_velocity=-420.0):
        self.gravity = gravity
        self.jump_velocity = jump_velocity

    @staticmethod
    def aabb(a, b):
        """Axis-aligned bounding box overlap test. Boxes are (x, y, w, h)."""
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by

    @staticmethod
    def frame_independent_velocity(v, dt, gravity):
        """Euler integration of vertical velocity under constant gravity."""
        return v + gravity * dt
