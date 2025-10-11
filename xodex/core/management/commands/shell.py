from __future__ import annotations

from xodex.core.management.command import BaseCommand

try:
    from colorama import Fore
    from colorama import init as colorama_init
    from colorama import Style

    colorama_init()
    COLOR_ENABLED = True
except ImportError:
    COLOR_ENABLED = False


def cprint(text, color=None):
    """cprint"""
    if COLOR_ENABLED and color:
        print(getattr(Fore, color.upper(), "") + text + Style.RESET_ALL)
    else:
        print(text)


class Command(BaseCommand):
    def __init__(self):
        super().__init__(
            description="Command description",
            usage="%(prog)s command [options]",
        )

    def add_arguments(self, parser):
        """
        Add arguments to parser.
        """

    def handle(self, options):
        """
        Handle the command.
        """
