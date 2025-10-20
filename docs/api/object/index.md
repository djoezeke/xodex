# Object

xodex provides a small object system optimized for games. The core types are:

- `DrawableObject` — implement `perform_draw(self, surface, *args, **kwargs)` to render.
- `LogicalObject` — implement `perform_update(self, deltatime, *args, **kwargs)` to update logic.
- `EventfulObject` — implement `handle_event(self, event, *args, **kwargs)` to react to events.

All classes provide hooks and helpers:

Contract / method summary

- DrawableObject.perform_draw(surface, \*args, \*\*kwargs) -> None

  - surface: pygame.Surface to draw on
  - Should not return a value; draw directly to the surface.

- DrawableObject.before_draw() -> None
- DrawableObject.after_draw() -> None
- DrawableObject.set_visible(visible: bool) -> None

- LogicalObject.perform_update(deltatime: float, \*args, \*\*kwargs) -> None

  - deltatime: float seconds since last update.

- LogicalObject.before_update() -> None
- LogicalObject.after_update() -> None

- EventfulObject.handle_event(event: pygame.Event, \*args, \*\*kwargs) -> None

Helpers

- `make_xodex_object(cls=None, base_classes=(), register=False, name=None, method_map=None, hooks=None, **kwargs)`
  - Adapts your class to Xodex object bases. Useful when migrating plain classes.
  - Example:

```python
from xodex.object.base import make_xodex_object, DrawableObject

@make_xodex_object(base_classes=(DrawableObject,))
class MyLegacySprite:
    def draw(self, surface):
        # user's draw method will be renamed to perform_draw
        pass
```

Edge cases

- If a required method is missing for the chosen base classes, `make_xodex_object` will raise `TypeError`.
- The adapt function can optionally register the new class with the global ObjectsManager if `register=True` (project-dependent).
