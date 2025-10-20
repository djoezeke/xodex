---
title: Working on projects
description: A guide to using xodex to create and building apps and games.
---

# Working on projects

xodex projects follow a small, opinionated layout so the engine can find
scenes, objects, and configuration consistently. The project scaffold includes
the code and the management scripts you need to run, build, and test your game.

## Creating a new project

Scaffold a new project using the CLI:

```console
xodex init hello-world
cd hello-world
```

Or initialize the current folder:

```console
mkdir hello-world
cd hello-world
xodex init
```

After scaffolding you will typically see:

```
.
├── project
│   ├── __init__.py
│   ├── __main__.py
│   ├── objects.py      # register game objects and helper factories
│   ├── scenes.py       # scene classes for game screens
│   └── settings.py     # project-specific configuration
├── LICENSE
├── README.md
├── manage.py           # convenience script to run the project's commands
└── requirements.txt
```

Try the built-in example (scaffolded `main` or `__main__`):

```console
xodex run
# or
python -m project
```

## Key project files

- `project/settings.py` — Central configuration (window size, FPS, title, assets).
- `project/scenes.py` — Define scenes that inherit from `BaseScene`.
- `project/objects.py` — Create concrete objects (sprites, UI elements) using `DrawableObject`, `LogicalObject`, or `EventfulObject`.
- `manage.py` — Thin wrapper to call the management utility (convenience for development).

Example `settings.py` snippet:

```python
# Window & Display
FPS = 60
WIDTH = 720
HEIGHT = 560
WINDOW_SIZE = (WIDTH, HEIGHT)
TITLE = "Hello Xodex"
VERSION = "0.1.0"
FULLSCREEN = False
ICON_PATH = None
```

## Working flow

1. Scaffold with `xodex init`.
2. Implement scenes in `project/scenes.py` and objects in `project/objects.py`.
3. Run with `xodex run` during development.
4. When ready, use `xodex build` (or your own packaging workflow) to create a distributable.

For more detail on the API and object model see the [Documentation](./api/index.md).
