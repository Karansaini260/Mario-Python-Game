"""Tile-map levels: '#' solid ground, '@' coin, 'P' player spawn, 'F' finish flag."""

from physics import Physics  # noqa: F401 (re-export convenience)


class Tile:
    def __init__(self, x, y, w=32, h=32):
        self.x, self.y, self.w, self.h = x, y, w, h

    @property
    def rect(self):
        return (self.x, self.y, self.w, self.h)


class Level:
    def __init__(self, rows):
        self.tiles = []
        self.coins = []
        self.spawn = (0, 0)
        self.finish = None
        self._parse(rows)

    def _parse(self, rows):
        tile = 32
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                x, y = i * tile, j * tile
                if ch == "#":
                    self.tiles.append(Tile(x, y, tile, tile))
                elif ch == "@":
                    self.coins.append((x + 6, y + 6, 20, 20))
                elif ch == "P":
                    self.spawn = (x, y)
                elif ch == "F":
                    # tall flag pole (3 tiles) so passing jumps still register
                    self.finish = (x, y - 2 * tile, tile, 3 * tile)

    def is_finished(self, player_rect):
        return self.finish is not None and Physics.aabb(player_rect, self.finish)


LEVELS = {
    "level_1": [
        "........................................",
        "........................................",
        "........................................",
        "........................................",
        "........................................",
        "..............@@@....@@@.................",
        "....@@.......#####...#####...@...........",
        "...P...@@....#####...#####..#####........",
        "##################################F......",
        "########################################",
    ],
    "level_2": [
        "........................................",
        "........................................",
        "........................................",
        "........................................",
        "........................................",
        ".............@@@.......@@@......@@@......",
        "...........####........####......####....",
        "..@........####...@....####......####..@.",
        "..##...P...####........####......####.F..",
        "########################################",
    ],
}


def load(name):
    if name not in LEVELS:
        raise KeyError(f"unknown level: {name}")
    return Level(LEVELS[name])
