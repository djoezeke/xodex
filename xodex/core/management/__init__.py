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
from xodex.utils.version import vernum

console = Console(
    theme=Theme(
        {
            "help": "bold cyan",
            "usage": "bold cyan",
            "group": "underline",
            "option": "bold cyan",
            "description": "bold white",
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


def find_commands(management_dir: str) -> list[str]:
    """
    Given a path to a management directory, return a list of all the command
    names that are available.
    """
    command_dir = os.path.join(management_dir, "commands")
    return [name for _, name, is_pkg in pkgutil.iter_modules([command_dir]) if not is_pkg and not name.startswith("_")]


def load_command_class(app_name, name):
    """
    Given a command name and an application name, return the Command
    class instance. Allow all errors raised by the import process
    (ImportError, AttributeError) to propagate.
    """
    module = importlib.import_module(f"{app_name}.management.commands.{name}")
    return module.Command()


class ManagementUtility:
    """Discovers and runs management commands for Xodex.

    Encapsulate the logic of the manage.py utilities.
    """

    def __init__(self, argv: list[str] = None, commands_package="xodex.core.management.commands"):
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

    def call_command(self, command_name: tuple[str] | BaseCommand | str, *args, **options) -> str:
        """
        Call the given command, with the given options and args/kwargs.

        This is the primary API you should use for calling specific commands.

        `command_name` may be a string or a command object. Using a string is
        preferred unless the command object is required for further processing or
        testing.

        Some examples:
            call_command('run')
            call_command('shell', plain=True)
            call_command('build', 'myapp')

            from xodex.core.management.commands import run
            cmd = flush.Command()
            call_command(cmd, verbosity=0, interactive=False)
            # Do something with cmd ...
        """
        if isinstance(command_name, BaseCommand):
            # Command object passed in.
            command = command_name
            command_name = command.__class__.__module__.split(".")[-1]
        else:
            # Load the command object by name.
            try:
                app_name = self.commands[command_name]
            except KeyError(f"Unknown command: {command_name}") as err:
                raise err

            if isinstance(app_name, BaseCommand):
                # If the command is already loaded, use it directly.
                command = app_name
            else:
                command = load_command_class(app_name, command_name)

        return command.execute(*args)

    def main_help(self):
        """
        Print help for all available commands using rich formatting.
        """
        console.print(
            "'[bold]xodex help <subcommand>[/bold]' for help on a specific subcommand.",
            style="help",
        )
        commands = Table(box=None)
        commands.add_column("Commands:", header_style="group", style="option")
        commands.add_column(style="description")
        commands.add_row("start", "")
        commands.add_row("build", "")
        commands.add_row("serve", "")
        commands.add_row("shell", "")
        commands.add_row("version", "Display xodex version")
        commands.add_row("help", "")

        options = Table(show_header=True, box=None)
        options.add_column("Global Options:", header_style="group", style="option")
        options.add_column(style="description")
        options.add_row("-q, --quiet", "Use quiet output.")
        options.add_row("-v, --verbose", "Use verbose output.")
        options.add_row("    --no-color", "Don't colorize the command output.")
        options.add_row(
            "    --directory",
            "Change to the given directory prior to running the command.",
        )
        options.add_row(
            "    --project",
            "Run the command within the given project directory [env: XODEX_PROJECT=].",
        )
        options.add_row(
            "    --settings",
            "The path to a `settings.py` configuration [env: XODEX_SETTINGS=].",
        )
        options.add_row("-h, --help", "Display the concise help for this command.")
        options.add_row("-V, --version", "Show the xodex version number and exit.")

        print()
        console.print(commands)
        print()
        console.print(options)

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
            help="The path to a `settings.py` configuration [env: XODEX_SETTINGS=]",
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


def execute_from_command_line(argv: list[str] = None):
    """Run Management Utility."""
    os.environ["XODEX_VERSION"] = str(vernum)
    utility = ManagementUtility(argv)
    utility.execute()
