# Using xodex

This page shows common usage patterns for the xodex game engine: installing, running a project, creating scenes and objects, and using the management commands.

## Quickstart

1. Install xodex (from PyPI or source)

   pip install xodex

2. Create a new project

   xodex init mygame

3. Run your project

   cd mygame
   xodex run

## Running via python -m

You can also run management commands using Python's -m switch:

    python -m xodex run
    python -m xodex start

## Project layout

A typical xodex project contains:

- a `project/` package with `__main__.py`, `objects.py`, `scenes.py`, and `settings.py`.
- assets and configuration under `project/` and `project/templates/`.

## Creating a Scene

Example minimal scene using xodex's `BaseScene`:

```python
from xodex.scene.base import BaseScene
from xodex.object import DrawableObject
import pygame

class HelloScene(BaseScene):
    def _generate_objects_(self):
        # yield objects to be managed by the scene
        yield

    def on_enter(self):
        # called when scene is entered
        pass
```

Add the scene to your project's scene manager and run the project to see it.

## Creating an Object

xodex separates object responsibilities. Use `DrawableObject`, `LogicalObject`, `EventfulObject` or combine them.

```python
from xodex.object.base import DrawableObject

class MySprite(DrawableObject):
    def perform_draw(self, surface, *args, **kwargs):
        # draw logic
        pass
```

For more API details see the API Reference pages.
