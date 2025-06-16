"""Exceptions"""


class NotRegistered(Exception):
    """NotRegistered"""


class AlreadyRegistered(Exception):
    """AlreadyRegistered"""


class UnknownScene(AttributeError):
    """UnknownScene"""

    def __init__(self, *args, name=..., obj=...):
        super().__init__(*args, name=name, obj=obj)


class UnknownObject(AttributeError):
    """UnknownObject"""

    def __init__(self, *args, name=..., obj=...):
        super().__init__(*args, name=name, obj=obj)


class ObjectError(Exception):
    """ObjectError"""


class SceneError(Exception):
    """SceneError"""
