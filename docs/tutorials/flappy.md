---
title: Build Flappy
description: A step-by-step tutorial building a minimal Flappy Bird clone with xodex
---

# Flappy Bird Tutorial

This tutorial walks through building a minimal Flappy Bird-style game using
xodex's scene and object model. It focuses on the essential game loop: drawing,
updating, and event handling.

Sections:

- Project scaffold
- Game assets and settings
- Implementing the `GameScene`
- Creating the `Bird` and `Pipe` objects
- Simple collision detection and scoring
- Packaging and next steps

Prerequisites:

- Python 3.11+
- pygame installed
- Basic familiarity with Python and game loops

## 1 — Scaffold the project

Create a new xodex project or use the template shipped with xodex:

```console
xodex init flappy
cd flappy
```

Place assets (images/sounds) under `project/assets/` and configure paths in
`project/settings.py`.

## 2 — Settings example

Add or adapt the following in `project/settings.py`:

```python
FPS = 60
WIDTH = 288
HEIGHT = 512
WINDOW_SIZE = (WIDTH, HEIGHT)
TITLE = "Flappy - xodex tutorial"
ASSETS = {
	'bird': 'assets/bird.png',
	'pipe': 'assets/pipe.png',
}
```

## 3 — Implement GameScene

Create a `GameScene` that yields objects in `_generate_objects_` and manages
pause/resume and snapshotting:

```python
from xodex.scene.base import BaseScene

class GameScene(BaseScene):
	def _generate_objects_(self):
		from project.objects import Bird, PipeManager
		yield Bird()
		yield PipeManager()

	def on_enter(self):
		# reset timers, score or preload sounds
		pass
```

## 4 — Bird object (Drawable + Logical + Eventful)

Create a `Bird` by combining responsibilities. Implement draw, update and
event handling (jump on key press):

```python
from xodex.object.base import DrawableObject, LogicalObject, EventfulObject
import pygame

class Bird(DrawableObject, LogicalObject, EventfulObject):
	def __init__(self):
		self.y = 200
		self.vy = 0
		self.image = pygame.image.load('project/assets/bird.png')

	def perform_update(self, deltatime, *args, **kwargs):
		self.vy += 900 * deltatime
		self.y += self.vy * deltatime

	def perform_draw(self, surface, *args, **kwargs):
		surface.blit(self.image, (50, int(self.y)))

	def handle_event(self, event, *args, **kwargs):
		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			self.vy = -250
```

## 5 — Pipes and collision

Implement a simple `PipeManager` that yields pipe pairs, moves them left, and
checks collision with the `Bird`. On collision, call scene's `pause()` or
transition to a Game Over scene.

## 6 — Scoring and polish

- Count pipes passed for score.
- Add sound effects using `xodex.game.sounds.Sounds`.
- Use `Scene.export_image()` to create screenshots for debugging.

## 7 — Run and iterate

Start the game during development with:

```console
xodex run
```

That's a compact plan. The full example is a good follow-up if you want me to
generate a runnable `project/` sample (code + assets placeholders + tests).
