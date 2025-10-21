"""
Objects Registration for {{ project_name_upper }} project.

Register your custom game objects here using the @register decorator.

Example:

Registering Object On Creation.

    ```python
    from xodex.object import register
    from xodex.object import LogicalObject, DrawableObject, EventfulObject

    # Register a button object with default name (class name)
    @register
    class Button(LogicalObject, DrawableObject, EventfulObject):
        ...

    # Register a text object with a custom name
    @register(name="text")
    class Text(DrawableObject, EventfulObject):
        ...
    ```

Registering Existing Objects.

    ```python
    from xodex.object import register
    from .mytext import MyText

    # Register a text object with default name (class name)
    register(MyText)

    # Register a text object with a custom name
    register(MyText,name="mytext")
    ```

How it works:
- The @register decorator adds your object class to the global registry.
- You can then instantiate or reference these objects by name in your scenes or game logic.
- Use multiple inheritance to combine logic, drawing, and event features as needed.

See the Xodex documentation for more advanced usage and patterns.
"""

from xodex.contrib.objects import XodexText
from xodex.object import register

# Register your {{ project_name }} Objects here.

register(XodexText, "XodexText")
