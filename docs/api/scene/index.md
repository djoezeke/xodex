# Scene

`BaseScene` is the recommended base class for creating game screens and levels. It handles common tasks: object lifecycle, drawing, updating, event dispatch, and scene management.

Key methods and properties

- `__init__(self, *args, **kwargs)` — initializes screen size, objects manager, and sounds.
- `elapsed` (property) -> float — seconds since the scene started.
- `screen` (property) -> pygame.Surface — the scene's surface.
- `objects` (property) -> Objects — scene-local object collection.
- `setup()` / `async_setup()` — (re)generate scene objects by calling `_generate_objects_`.
- `draw_scene(*args, **kwargs)` -> pygame.Surface — draws all registered objects and returns the surface.
- `update_scene(deltatime: float, *args, **kwargs)` — updates all objects (skips if paused).
- `handle_scene(event: pygame.Event, *args, **kwargs)` — handles a single event; recognizes `VIDEORESIZE` to resize.
- `add_event(event)` / `dispatch_events()` — queue and dispatch events.
- `pause()` / `resume()` / `toggle_pause()` — control update/event flow.
- `filter_objects(predicate=None, obj_type=None)` -> list — helper to query scene objects.
- `snapshot()` -> pygame.Surface — returns a copy of the scene surface.
- `export_image(filename)` — saves the current scene surface to a file.

Implementing a scene

The required method to implement is `_generate_objects_`, a generator that yields objects:

```python
class MenuScene(BaseScene):
    def _generate_objects_(self):
        yield MyPlayer()
        yield MyButton()
```

Lifecycle hooks

Override these for scene-specific behavior:

- `on_enter()` — called when scene is entered.
- `on_exit()` — called when leaving the scene.
- `on_pause()` / `on_resume()` — called when scene is paused/resumed.

Notes and tips

- Scenes respect the global `settings.WINDOW_SIZE` from your project's settings.
- Use `draw_debug_overlay()` to provide a quick on-screen debug readout while developing.
