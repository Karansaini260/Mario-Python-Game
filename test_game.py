import sys
sys.path.insert(0, ".")

from physics import Physics
from level import load
from game import Game, MOVE_SPEED

FPS = 60


def test_aabb_overlap():
    assert Physics.aabb((0, 0, 10, 10), (5, 5, 10, 10))
    assert not Physics.aabb((0, 0, 10, 10), (20, 20, 10, 10))


def test_gravity_pulls_down():
    game = Game(load("level_1"))
    vy_before = game.player.vy
    game.update(1 / FPS)
    assert game.player.vy > vy_before


def test_player_can_run_right():
    game = Game(load("level_1"))
    x0 = game.player.x
    game.set_move(1)
    for _ in range(30):
        game.update(1 / FPS)
    assert game.player.x > x0


def test_ground_collision_stops_fall():
    game = Game(load("level_1"))
    # drop the player from above; after some frames on_ground must be True
    game.player.y = 100
    for _ in range(120):
        game.update(1 / FPS)
    assert game.player.on_ground


def test_level_2_completable_in_simulation():
    game = Game(load("level_2"))
    steps = 0
    while not game.won and steps < 5000:
        game.set_move(1)
        p = game.player
        # jump when blocked ahead or when a pit is ahead while on the ground
        blocked = any(Physics.aabb((p.x + p.w + 4, p.y + 2, 4, p.h - 4), t.rect)
                      for t in game.level.tiles)
        gap = not any(Physics.aabb((p.x + p.w + 8, p.y + p.h + 6, 12, 6), t.rect)
                      for t in game.level.tiles)
        near_flag = game.level.finish is not None and \
            p.x > game.level.finish[0] - 130
        if blocked or (p.on_ground and gap and not near_flag):
            game.jump()
        game.update(1 / FPS)
        steps += 1
    assert game.won, f"level_2 should be completable, reached step {steps}"


if __name__ == "__main__":
    import traceback
    passed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn(); passed += 1; print(f"PASS {name}")
            except AssertionError as e:
                print(f"FAIL {name}: {e}")
            except Exception as e:
                traceback.print_exc()
    print(f"\n{passed} passed")
