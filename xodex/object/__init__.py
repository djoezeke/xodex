from xodex.object.base import DrawableObject
from xodex.object.base import EventfulObject
from xodex.object.base import LogicalObject
from xodex.object.base import Object
from xodex.object.manager import ObjectsManager
from xodex.object.manager import register

__all__ = (
    "make_xodex_object",
    "ObjectsManager",
    "DrawableObject",
    "EventfulObject",
    "LogicalObject",
    "register",
    "Object",
)


def make_xodex_object(
    cls=None,
    *,
    base_classes: tuple[type, ...] = (),
    register: bool = False,
    name: str = None,
    doc: str = None,
):
    """
    Create a Xodex object from any class, validating required methods for each base.

    Args:
        cls (type, optional): The class to convert. If None, returns a decorator.
        base_classes (tuple[type, ...], optional): Xodex base classes to inherit from.
        register (bool, optional): Whether to register the object with ObjectsManager.
        name (str, optional): Name to register the object as. Defaults to class name.
        doc (str, optional): Docstring to set on the new class.

    Returns:
        type: The new Xodex object class, or a decorator if cls is None.

    Raises:
        TypeError: If the class does not implement required methods for the selected base(s).

    Usage:
        @makeobject(base_classes=(DrawableObject,), register=True)
        class MySprite:
            ...

        # or
        MyObject = makeobject(MyClass, base_classes=(LogicalObject,), register=True)
    """

    # Map base class to required method(s)
    REQUIRED_METHODS = {
        LogicalObject: ["perform_update"],
        DrawableObject: ["perform_draw"],
        EventfulObject: ["handle_event"],
    }

    def validate_methods(object_cls, bases):
        missing = []
        for base in bases:
            reqs = REQUIRED_METHODS.get(base, [])
            for method in reqs:
                if not callable(getattr(object_cls, method, None)):
                    missing.append(method)
        if missing:
            raise TypeError(f"Class '{object_cls.__name__}' is missing required method(s): {', '.join(missing)}")

    def decorator(object_cls):
        validate_methods(object_cls, base_classes)
        bases = base_classes + (object_cls,)
        object_name = name or object_cls.__name__
        new_cls = type(object_name, bases, dict(object_cls.__dict__))
        if doc:
            new_cls.__doc__ = doc
        if register:
            ObjectsManager().register(new_cls, object_name)
        return new_cls

    if cls is None:
        return decorator
    return decorator(cls)
