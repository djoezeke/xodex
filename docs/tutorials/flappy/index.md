---
title: Build Flappy
description: A step-by-step tutorial building a minimal Flappy Bird clone with xodex
---

# Flappy Bird tutorial (improved)

This tutorial shows how to build a minimal Flappy Bird clone using the xodex
engine. It expands the existing step-by-step guide with clearer contracts,
complete code sketches (based on the reference flappy clone), common edge
cases, and practical "how to run" instructions.

Target audience: developers comfortable with Python and basic game loops.

What you'll get from this tutorial

- A small contract describing the objects and their responsibilities.
- Complete, corrected examples for the bird, pipes, scoring and scenes.
- Notes about edge cases and testing.
- Quick steps to create a runnable project skeleton using the xodex template.

Quick contract (inputs/outputs)

- Inputs: keyboard (space/up) or mouse/touch for flap; window size from
  settings.
- Outputs: rendered game frame, sounds (wing/point/hit), score integer.
- Data shapes: objects expose methods perform_update(deltatime), perform_draw(surface),
  handle_event(event) and a `rect` (pygame.Rect) for collision.

Edge cases to consider

- Running at variable FPS: use delta-time in physics calculations.
- Window resize: choose fixed game coordinate system (WIDTH/HEIGHT in
  settings) or scale contents explicitly.
- Audio unavailable: guard sound playback so missing files don't crash.
- Asset paths: prefer project-relative paths and provide helpful error messages.

Checklist (what we'll cover)

1. Project scaffold and settings
2. Implement objects: Background, Floor, Pipe, Pipes manager, Bird/Flappy, Score
3. Implement scenes: MainScene (menu), GameScene (play), OverScene (game over)
4. Collision detection, scoring and sound hooks
5. Run instructions and optional testing notes

Minimal project scaffold

Scaffold a new project from the xodex template (recommended):

1. Create a folder and use the xodex template shipped with this repo:

   - Copy the `xodex/template/project/` directory into a new folder `flappy/`.
   - Edit `flappy/settings.py` and `flappy/objects.py` per the examples below.

Should get you will typically see:

```
.
├── flappy
│   ├── __init__.py
│   ├── __main__.py
│   ├── settings.py
│   ├── objects
│   │	├── __init__.py
│   │	├── score.py
│   │	├── flappy.py
│   │	└── background.py
│   └── scenes
│    	├── __init__.py
│    	├── mainscene.py
│    	├── gamescene.py
│    	└── overscene.py
├── Assets
│   ├── sounds
│   │	├── die.wav
│   │	├── hit.wav
│   │	├── wing.wav
│   │	├── point.wav
│   │	└── swoosh.wav
│   └── images
│    	├── 0.png
│    	├── 1.png
│    	├── 2.png
│    	├── 3.png
│    	├── 4.png
│    	├── 5.png
│    	├── 6.png
│    	├── 7.png
│    	├── 8.png
│    	├── 9.png
│    	├── base.png
│    	├── message.png
│    	├── gameover.png
│    	├── pipe-red.png
│    	├── pipe-green.png
│    	├── background-day.png
│    	├── background-night.png
│    	├── redbird-downflap.png
│    	├── redbird-midflap.png
│    	├── redbird-upflap.png
│    	├── bluebird-downflap.png
│    	├── bluebird-midflap.png
│    	├── bluebird-upflap.png
│    	├── yellowbird-downflap.png
│    	├── yellowbird-midflap.png
│    	├── yellowbird-upflap.png
│    	└── overscene.py
├── LICENSE
├── README.md
├── manage.py
└── requirements.txt
```

2. A minimal `settings.py` useful for the tutorial:

```python
# --- Window & Display ---
FPS = 30
WIDTH = 288
HEIGHT = 512
WINDOW_SIZE = (WIDTH, HEIGHT)
TITLE = "Flappy - xodex tutorial"
MAIN_SCENE = "MainScene"
```

Run tips

- Install dependencies from the provided `requirements.txt` (pygame, xodex
  dependencies).
- Start the game with your project `manage.py` or the CLI command from the
  template (for a scaffolded project this is `xodex run` or `python -m flappy`).

If you'd like, I can now:

- Update the three tutorial pages in `docs/tutorials/flappy/` with full
  corrected examples and clearer explanations (objects.md, scenes.md and this
  index). (recommended)
- Or generate a runnable `project/` sample using the xodex template with
  complete source and lightweight placeholder assets.

Which should I do next? (I'll proceed to update the docs if you don't say otherwise.)
