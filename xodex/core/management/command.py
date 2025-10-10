from __future__ import annotations

import argparse
import os
import sys

from rich.console import Console
from rich.theme import Theme

from xodex.utils.version import vernum

console = Console(
    theme=Theme(
        {
            "help": "bold cyan",
            "desc": "dim white",
            "error": "bold red",
            "success": "bold green",
            "warning": "yellow",
        }
    )
)


def handle_default_options(options):
    """
    Include any default options that all commands should accept here
    so that ManagementUtility can handle them before searching for
    user commands.
    """
    # if options.settings:
    #     os.environ["XODEX_SETTINGS_MODULE"] = options.settings
    # if options.pythonpath:
    #     sys.path.insert(0, options.pythonpath)


class BaseCommand:
    """
    Several attributes affect behavior at various steps along the way:

    ``help``
        A short description of the command, which will be printed in
        help messages.
    """

    def __init__(self, description, usage=None):
        self.usage = usage or "%(prog)s <command> [options] [args]"
        self.description = description
        self.version = str(vernum)

    def parser(self, prog_name, **kwargs):
        """Create and return the ``ArgumentParser`` which will be used toparse the arguments to this command."""

        parser = argparse.ArgumentParser(
            prog=os.path.basename(prog_name),
            usage=self.usage,
            description=self.description,
            epilog="Use `xodex help <command>` for more options",
        )

        self.add_arguments(parser)

        parser.add_argument(
            "-q",
            "--quiet",
            action="store_true",
            help="Use quiet output.",
        )
        parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Use verbose output.",
        )
        parser.add_argument(
            "--no-color",
            action="store_true",
            help="Don't colorize the command output.",
        )
        parser.add_argument(
            "--directory",
            help=("Change to the given directory prior to running the command."),
        )
        parser.add_argument(
            "--project",
            help=("Run the command within the given project directory [env: XODEX_PROJECT=]."),
        )
        parser.add_argument(
            "--settings",
            help=("The path to a `settings.py` configuration [env: XODEX_SETTINGS=]"),
        )
        parser.add_argument(
            "-V",
            "--version",
            action="version",
            version=self.version,
            help="Show the xodex version number and exit.",
        )
        return parser

    def print_help(self, prog_name):
        """Print the help message for this command."""
        parser = self.parser(prog_name)
        console.print(parser.format_help())

    def execute(self, argv):
        """execute"""
        parser = self.parser(argv[0])
        options, _ = parser.parse_known_args(argv[2:])
        handle_default_options(options)
        try:
            print(options)
            self.handle(options)
        except argparse.ArgumentError as e:
            if options.traceback:
                raise
            print(e)
            sys.exit(1)

    def add_arguments(self, parser):
        """Entry point for subclassed commands to add custom arguments."""
        raise NotImplementedError("subclasses of BaseCommand must provide a add_arguments() method")

    def handle(self, options):
        """The actual logic of the command. Subclasses must implementthis method."""
        raise NotImplementedError("subclasses of BaseCommand must provide a handle() method")
