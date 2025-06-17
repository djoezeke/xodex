"""Values"""


class Values:
    """Class to store Attributes"""

    def __init__(self, defaults=None):
        if defaults:
            for attr, val in defaults.items():
                setattr(self, attr, val)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def __eq__(self, other):
        if isinstance(other, Values):
            return self.__dict__ == other.__dict__
        elif isinstance(other, dict):
            return self.__dict__ == other
        else:
            return False
