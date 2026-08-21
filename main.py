"""Pygame front-end for the Mario-style platformer.

Usage:
    pip install pygame
    python main.py                 # play level_1
    python main.py level_2
    python main.py --simulate      # headless playthrough (no display needed)
"""

import argparse
import sys

from game import Game
from physics import Physics
from level import load, LEVELS

FPS = 60


def simulate(name: str, seconds: float = 8.0):
    game = Game(load(name))
    steps = 0
    while game.time < seconds and not game.won and steps < 10_000:
        # simple AI: run right, jump when blocked or when a pit is ahead,
        # but never gap-jump once the finish flag is close (just run into it)
        game.set_move(1)
        near_flag = game.level.finish is not None and \
            game.player.x > game.level.finish[0] - 130
        if _blocked_ahead(game) or \
                (game.player.on_ground and _gap_ahead(game) and not near_flag):
            game.jump()
        game.update(1.0 / FPS)
        steps += 1
    print(f"[simulate] {name}: time={game.time:.1f}s score={game.score} "
          f"won={game.won} steps={steps}")


def _blocked_ahead(game):
    """True if a solid tile is directly in front of the player."""
    p = game.player
    probe = (p.x + p.w + 4, p.y + 2, 4, p.h - 4)
    return any(Physics.aabb(probe, t.rect) for t in game.level.tiles)


def _gap_ahead(game):
    """True if the ground disappears just in front of the player (a pit)."""
    p = game.player
    probe = (p.x + p.w + 8, p.y + p.h + 6, 12, 6)
    return not any(Physics.aabb(probe, t.rect) for t in game.level.tiles)


def play(name: str):
    import pygame

    game = Game(load(name))
    pygame.init()
    screen = pygame.display.set_mode((960, 320))
    clock = pygame.time.Clock()
    running = True
    while running and not game.won:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        game.set_move((keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]))
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            game.jump()
        game.update(dt)
        screen.fill((135, 206, 235))
        for t in game.level.tiles:
            pygame.draw.rect(screen, (120, 72, 20), t.rect)
        for coin in game.level.coins:
            pygame.draw.rect(screen, (255, 215, 0), coin)
        if game.level.finish:
            pygame.draw.rect(screen, (0, 128, 0), game.level.finish)
        pygame.draw.rect(screen, (220, 40, 40), game.player.rect)
        pygame.display.flip()
    print(f"score={game.score} won={game.won}")
    pygame.quit()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("level", nargs="?", default="level_1", choices=list(LEVELS))
    ap.add_argument("--simulate", action="store_true")
    args = ap.parse_args()
    if args.simulate:
        simulate(args.level)
    else:
        try:
            play(args.level)
        except ImportError:
            print("pygame not installed — running headless simulation instead")
            simulate(args.level)


if __name__ == "__main__":
    main()
