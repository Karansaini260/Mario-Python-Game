# 🍄 Mario Python Game

A classic side-scrolling **Mario-style platformer** built in pure Python —
no game engine required.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
[![Pygame optional](https://img.shields.io/badge/Pygame-optional-2EA44F)](https://www.pygame.org/)

## 🎮 Features
- 🕹️ **Physics engine** — gravity, jumping, AABB collision (headless-testable)
- 🗺️ **Tile-map levels** — design your own with `#`, `@`, `P` and `F`
- 🪙 **Coin collection** & finish flags
- 🤖 **Built-in demo AI** — watch it play through both levels headlessly
- 🧪 **5 unit tests** covering physics, collisions and level completion

## 🚀 Getting Started

### Option A — headless simulation (no dependencies)
```bash
python3 main.py --simulate          # watch the AI play level_1
python3 main.py --simulate level_2
```

### Option B — play it yourself (needs pygame)
```bash
pip install pygame
python3 main.py                     # play level_1
python3 main.py level_2
```
Controls: **← →** move · **Space/↑** jump · **Esc/close** quit

### Run the tests
```bash
python3 test_game.py
```

## 🧩 Project Structure
```
├── main.py        # pygame front-end + demo AI (headless capable)
├── game.py        # Game engine: physics + level interactions
├── physics.py     # AABB collision & gravity helpers
├── level.py       # tile-map level definitions ('#' solid, '@' coin, 'P' spawn, 'F' finish)
└── test_game.py   # 5 unit tests
```

## 🛠️ Built With
- Python (stdlib) · pygame (optional, display only)

## 📄 License
MIT
