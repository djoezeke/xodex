# xodex Concepts

This page explains the main ideas used across xodex. Use these as a mental
model when designing scenes and objects.

Core concepts

- Object model: xodex separates responsibilities into three orthogonal roles:

  - `DrawableObject` — objects that render to a `pygame.Surface`.
  - `LogicalObject` — objects that have updatable logic (physics, AI).
  - `EventfulObject` — objects that respond to Pygame events (input).

- Scene: a `BaseScene` composes objects and manages lifecycle, drawing,
  updating, and event dispatch. Scenes yield objects via `_generate_objects_`.

- ObjectsManager / SceneManager: utilities that register, query, and manage
  collections of objects and scenes for an application.

- Settings: a central `settings.py` configuration declares window size,
  resources, and other project-specific values.

Design tips

- Favor small objects with a single responsibility (draw/update/event).
- Use `make_xodex_object` to adapt existing classes when migrating code.
- Keep scene logic (state and transitions) in scenes and object logic inside
  objects — this makes testing and reuse easier.

See the API reference and guides for concrete examples.
