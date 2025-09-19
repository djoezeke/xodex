"""Management"""

import argparse
import importlib
import os
import pkgutil
import sys

from rich.console import Console
from rich.table import Table
from rich.theme import Theme

from xodex.core.management.command import BaseCommand
from xodex.core.management.command import handle_default_options
from xodex.version import vernum

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


__all__ = ("ManagementUtility",)


def cprint(text, style=None):
    """Rich colored print"""
    if style:
        console.print(text, style=style)
    else:
        console.print(text)


class ManagementUtility:
    """Discovers and runs management commands for Xodex.

    Encapsulate the logic of the manage.py utilities.
    """

    def __init__(self, argv=None, commands_package="xodex.core.management.commands"):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        if self.prog_name == "__main__.py":
            self.prog_name = "python -m xodex"
        self.commands_package = commands_package
        self.commands: dict[str, BaseCommand] = self.discover_commands()
        self.settings_exception = None

    def discover_commands(self):
        """
        Discover all command modules in the commands package.
        Returns a dict: {command_name: CommandClass}
        """
        commands = {}
        try:
            package = importlib.import_module(self.commands_package)
        except ImportError:
            console.print(f"[error]Could not import commands package: {self.commands_package}")
            return commands

        package_path = package.__path__
        for _, name, is_pkg in pkgutil.iter_modules(package_path):
            if is_pkg:
                continue
            module_name = f"{self.commands_package}.{name}"
            try:
                module = importlib.import_module(module_name)
                for attr in dir(module):
                    obj = getattr(module, attr)
                    if isinstance(obj, type) and issubclass(obj, BaseCommand) and obj is not BaseCommand:
                        commands[name] = obj
            except Exception as e:
                console.print(f"[error]Error importing command '{name}': {e}")
        return commands

    def main_help(self):
        """
        Print help for all available commands using rich formatting.
        """
        console.print("'[bold]xodex help <subcommand>[/bold]' for help on a specific subcommand.", style="help")
        table = Table(show_header=True, box=None, header_style="bold magenta")
        table.add_column("Commands:", style="cyan", no_wrap=True)
        table.add_column("", style="desc")
        for name, cmd in self.commands.items():
            desc = getattr(cmd, "description", "")
            table.add_row(f"  {name}", f"  {desc}")
        console.print(table)

    def fetch_command(self, name) -> BaseCommand:
        """
        Return the command class for the given name.
        """
        if name in self.commands:
            return self.commands[name]()

    def execute(self):
        """Given the command-line arguments, figure out which command and run it."""

        parser = argparse.ArgumentParser(
            prog=self.prog_name,
            usage="%(prog)s <subcommand> [options] [args]",
            description="Xodex Management Utility",
            epilog="Use `xodex help <command>` for more options",
            add_help=False,
        )

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
            help=("The path to a `uv.toml` file to use for configuration [env: XODEX_SETTINGS_FILE=]"),
        )
        parser.add_argument(
            "-V",
            "--version",
            action="version",
            version=str(vernum),
            help="Show the xodex version number and exit.",
        )
        parser.add_argument("command", nargs="?")

        try:
            options, args = parser.parse_known_args(self.argv[2:])
            handle_default_options(options)
            print(options)
        except argparse.ArgumentError:
            pass

        try:
            command = self.argv[1]
        except IndexError:
            command = "help"

        if command in ["help", "-h", "--help"]:
            command_obj = self.fetch_command(options.command)
            if command_obj:
                command_obj.print_help(self.argv[1])
            else:
                self.main_help()
        if command in ["version", "-V", "--version"]:
            console.print(f"[success]{vernum}")
        else:
            command_obj = self.fetch_command(command)
            if command_obj:
                command_obj.execute(self.argv)


def execute_from_command_line(argv=None):
    """Run Management Utility."""
    os.environ["XODEX_VERSION"] = str(vernum)
    utility = ManagementUtility(argv)
    utility.execute()
