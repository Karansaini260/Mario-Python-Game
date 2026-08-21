"""Game engine wiring physics + levels together (headless-runnable)."""

from physics import Physics
from level import Level

GRAVITY = 900.0        # px/s^2
JUMP_VELOCITY = -520.0  # px/s (≈150px jump height)
MOVE_SPEED = 220.0     # px/s
PLAYER_W, PLAYER_H = 26, 30


class Player:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.vx, self.vy = 0.0, 0.0
        self.on_ground = False
        self.w, self.h = PLAYER_W, PLAYER_H

    @property
    def rect(self):
        return (self.x, self.y, self.w, self.h)


class Game:
    """Headless game engine: update(dt) advances the simulation."""

    def __init__(self, level: Level):
        self.level = level
        self.player = Player(*level.spawn)
        self.physics = Physics(GRAVITY, JUMP_VELOCITY)
        self.time = 0.0
        self.score = 0
        self.won = False

    def jump(self):
        if self.player.on_ground:
            self.player.vy = self.physics.jump_velocity

    def set_move(self, direction: float):
        self.player.vx = MOVE_SPEED * direction

    def update(self, dt: float):
        self.time += dt
        p = self.player
        p.vy += self.physics.gravity * dt
        p.x += p.vx * dt
        self._resolve_axis("x")
        p.y += p.vy * dt
        p.on_ground = False
        self._resolve_axis("y")
        self._collect_coins()
        if self.level.is_finished(p.rect):
            self.won = True

    def _resolve_axis(self, axis: str):
        p = self.player
        for tile in self.level.tiles:
            if Physics.aabb(p.rect, tile.rect):
                if axis == "x":
                    if p.vx > 0:
                        p.x = tile.x - p.w
                    elif p.vx < 0:
                        p.x = tile.x + tile.w
                    p.vx = 0
                else:
                    if p.vy > 0:
                        p.y = tile.y - p.h
                        p.on_ground = True
                    elif p.vy < 0:
                        p.y = tile.y + tile.h
                    p.vy = 0

    def _collect_coins(self):
        p = self.player
        kept = []
        for coin in self.level.coins:
            if Physics.aabb(p.rect, coin):
                self.score += 100
            else:
                kept.append(coin)
        self.level.coins = kept
