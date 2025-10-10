from __future__ import annotations

from xodex.core.management.command import BaseCommand


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
