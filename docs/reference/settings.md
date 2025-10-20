# Project Settings Reference

This page documents the most commonly used settings available in a xodex
project's `settings.py`.

Common settings

- `FPS` (int): Target frames per second. Default: 60
- `WIDTH`, `HEIGHT` (int): Window width and height in pixels.
- `WINDOW_SIZE` (tuple): `(WIDTH, HEIGHT)` convenience tuple.
- `TITLE` (str): Window title.
- `VERSION` (str): Project version string.
- `FULLSCREEN` (bool): Whether to start in fullscreen mode.
- `ICON_PATH` (str|None): Path to the window icon image.
- `ASSETS` (dict): Optional mapping for named asset paths (images, sounds).

Example

```python
FPS = 60
WIDTH = 720
HEIGHT = 560
WINDOW_SIZE = (WIDTH, HEIGHT)
TITLE = "My Xodex Game"
VERSION = "0.1.0"
FULLSCREEN = False
ICON_PATH = "assets/icon.png"
ASSETS = {
    'player': 'assets/player.png',
    'bg': 'assets/bg.png',
}
```

Notes

- Settings are imported into scenes via `from xodex.conf import settings`.
- You can provide a `XODEX_SETTINGS_MODULE` environment variable to point to
  a different settings module for testing or CI.

See also: [Working on projects](../project.md) for how the settings
fit into a scaffolded project.
