"""Management"""

import os
import re
import sys
import pathlib
import argparse
import platform
import subprocess

try:
    from colorama import Fore, Style, init as colorama_init

    colorama_init()
    COLOR_ENABLED = True
except ImportError:
    COLOR_ENABLED = False

from xodex.game.game import Game
from xodex.version import vernum

__all__ = ("ManagementUtility", "execute_from_command_line")


def cprint(text, color=None):
    """cprint"""
    if COLOR_ENABLED and color:
        print(getattr(Fore, color.upper(), "") + text + Style.RESET_ALL)
    else:
        print(text)


class ProjectBuilder:
    """Handles building standalone executables using PyInstaller."""

    def __init__(
        self,
        project_name: str,
        *args,
        build_name: str = None,
        onefile=True,
        console=False,
        interactive=False,
    ):
        self.project_name = project_name
        self.project_dir = os.path.abspath(project_name)
        self.build_name = build_name or self.project_name
        self.onefile = onefile
        self.console = console
        self.interactive = interactive

    def build(self):
        """Build an executable from main.py using PyInstaller."""

        current_os = platform.system().lower()  # Determine the OS

        main_py = os.path.join(self.project_name, "hello", "hello", "__main__.py")
        # if not os.path.exists(main_py):
        #     cprint(f"__main__.py not found in {main_py} {self.project_dir}.", "RED")
        #     return

        pyinstaller_cmd = [
            sys.executable,
            "-m",
            "PyInstaller",
            f"{main_py}",
            # "--distpath",
            # os.path.join(self.project_dir, "dist"),
            # "--workpath",
            # os.path.join(self.project_dir, "build"),
            # "--specpath",
            # os.path.join(self.project_dir, "build"),
        ]

        # Add OS-specific options if necessary
        # if current_os == "windows":
        #     pyinstaller_cmd.append("--windowed")  # No console window for GUI apps
        # elif current_os == "linux":
        #     # Add Linux-specific options if needed
        #     pass
        # elif current_os == "darwin":  # macOS
        #     # Add macOS-specific options if needed
        #     pass

        if self.onefile:
            pyinstaller_cmd.append("--onefile")
        if not self.console:
            pyinstaller_cmd.append("--noconsole")
        # pyinstaller_cmd.append(main_py)

        if self.build_name:
            pyinstaller_cmd.append(f"-n {self.build_name}")

        cprint(f"Building {self.build_name} executable...", "CYAN")
        cprint(f"{self.pyinstaller_cmd}", "CYAN")
        try:
            result = subprocess.run(
                pyinstaller_cmd,
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                check=True,
            )
            cprint(f"{self.build_name} executable built successfully!", "GREEN")
            exe_name = (
                f"{self.build_name}.exe" if os.name == "nt" else f"{self.build_name}"
            )
            exe_path = os.path.join(self.project_dir, "dist", exe_name)
            if os.path.exists(exe_path):
                cprint(f" {self.build_name} executable located at: {exe_path}", "CYAN")
            else:
                cprint(
                    "Build finished, but executable not found in expected location.",
                    "YELLOW",
                )
        except subprocess.CalledProcessError as e:
            cprint(f"Failed to build '{self.build_name}'.", "RED")
            cprint(e.stdout, "RED")
            cprint(e.stderr, "RED")
        except Exception as e:
            cprint(f"Unexpected error: {e}", "RED")


class ProjectGenerator:
    """
    ProjectGenerator handles rendering and copying a project template with variable substitution and extra features.

    Advanced Features:
    - Renders template files with {{ variable }} placeholders.
    - Supports skipping, overwriting, or renaming existing files.
    - Allows custom context variables.
    - Excludes unwanted files/directories.
    - Can add a .gitignore and README.md automatically.
    - Supports file renaming via a mapping.
    - Supports template file extension (e.g., .tpl) and output renaming.
    - Interactive mode for conflict resolution.
    - Dry-run mode to preview changes.
    - Custom hooks for post-processing.
    """

    def __init__(
        self,
        name,
        context=None,
        extra_files=True,
        rename_map=None,
        template_ext=".tpl",
        interactive=False,
        dry_run=False,
        post_hooks=None,
    ):
        self.name = name
        self.context = context or {}
        self.context.setdefault("project_name", name)
        self.extra_files = extra_files
        self.rename_map = rename_map or {}
        self.template_ext = template_ext
        self.interactive = interactive
        self.dry_run = dry_run
        self.post_hooks = post_hooks or []

        self.cwd = os.getcwd()
        self.main_dir = os.path.join(self.cwd, name)
        self.xodex_dir = pathlib.Path(__file__).parent.parent
        self.template_dir = os.path.join(self.xodex_dir, "conf", "template")
        self.excluded_directories = [".git", "__pycache__"]
        self.excluded_files = [".pyo", ".pyc", ".py.class"]

    def render_template(self, content):
        """Render {{ var }} placeholders in the template content."""

        def replacer(match):
            key = match.group(1).strip()
            return str(self.context.get(key, match.group(0)))

        return re.sub(r"\{\{\s*(\w+)\s*\}\}", replacer, content)

    def resolve_filename(self, filename):
        """Rename files based on mapping or remove template extension."""
        if filename in self.rename_map:
            return self.rename_map[filename]
        if self.template_ext and filename.endswith(self.template_ext):
            return filename[: -len(self.template_ext)]
        return filename

    def copy_template(self):
        """Copy and render the template directory structure."""
        prefix_length = len(self.template_dir) + 1

        for root, dirs, files in os.walk(self.template_dir):
            path_rest = root[prefix_length:]
            relative_dir = path_rest
            if relative_dir:
                target_dir = os.path.join(self.main_dir, relative_dir)
                if not self.dry_run:
                    os.makedirs(target_dir, exist_ok=True)
            else:
                target_dir = self.main_dir

            # Exclude unwanted directories
            for dirname in dirs[:]:
                if dirname.startswith(".") or dirname in self.excluded_directories:
                    dirs.remove(dirname)

            for filename in files:
                if any(filename.endswith(ext) for ext in self.excluded_files):
                    continue
                old_path = os.path.join(root, filename)
                new_filename = self.resolve_filename(filename)
                new_path = os.path.join(target_dir, new_filename)

                if os.path.exists(new_path):
                    if self.interactive:
                        resp = (
                            input(f"{new_path} exists. Overwrite [y/N/rename]? ")
                            .strip()
                            .lower()
                        )
                        if resp == "y":
                            pass
                        elif resp == "rename":
                            new_path = input("Enter new filename: ").strip()
                        else:
                            cprint(f"Skipped {new_path}", "YELLOW")
                            continue
                    else:
                        cprint(f"{new_path} already exists. Skipping.", "YELLOW")
                        continue

                with open(old_path, encoding="utf-8") as template_file:
                    content = template_file.read()
                rendered = self.render_template(content)
                if self.dry_run:
                    cprint(f"[DRY RUN] Would create: {new_path}", "CYAN")
                else:
                    with open(new_path, "w", encoding="utf-8") as new_file:
                        new_file.write(rendered)

    def post_process(self):
        """Rename 'project' dir to project name and add extra files if needed."""
        project_dir = os.path.join(self.main_dir, "project")
        if os.path.exists(project_dir):
            os.renames(project_dir, os.path.join(self.main_dir, self.name))

        if self.extra_files:
            # Add a .gitignore if not present
            gitignore_path = os.path.join(self.main_dir, ".gitignore")
            if not os.path.exists(gitignore_path) and not self.dry_run:
                with open(gitignore_path, "w", encoding="Utf-8") as f:
                    f.write("__pycache__/\n*.pyc\n*.pyo\n*.log\nsave/\n")

        # Run custom post-generation hooks
        for hook in self.post_hooks:
            hook(self)

    def generate(self):
        """Main entry: generate the project."""
        if self.dry_run:
            cprint(f"[DRY RUN] Would create directory: {self.main_dir}", "CYAN")
        else:
            try:
                os.makedirs(self.main_dir)
            except FileExistsError:
                cprint(f"'{self.main_dir}' already exists", "YELLOW")
        self.copy_template()
        self.post_process()
        cprint(f"App '{self.name}' created successfully!", "GREEN")


class ManagementUtility:
    """Encapsulate the logic of the manage.py utilities."""

    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        if self.prog_name == "__main__.py":
            self.prog_name = "python -m xodex"
        self.settings_exception = None

    def execute(self):
        """Given the command-line arguments, figure out which command and run it."""

        parser = argparse.ArgumentParser(
            prog=self.prog_name,
            usage="%(prog)s <subcommand> [options] [args]",
            description="Xodex Management Utility",
            add_help=False,
        )

        subparsers = parser.add_subparsers(dest="subcommand", help="Subcommands")

        # Parser Arguments
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=str(vernum),
            help="Show program version info and exit.",
        )
        parser.add_argument(
            "-h", "--help", dest="help", nargs="?", help="Show this help message"
        )

        # Running Project Parser & Arguments.
        parser_run = subparsers.add_parser("run", help="Run the project")
        parser_run.add_argument(
            "--debug", action="store_true", help="Create a single executable"
        )
        parser_run.add_argument(
            "--verbose",
            "-v",
            dest="verbosity",
            action="count",
            default=1,
            help="increase verbosity",
        )

        # Building Project Parser & Arguments.
        parser_build = subparsers.add_parser(
            "build", help="Build the game using PyInstaller"
        )
        parser_build.add_argument(
            "--name",
            "-n",
            type=str,
            nargs="?",
            dest="name",
            help="Name to assign to the bundled app (defaults to Project Name)",
            metavar="-NAME",
        )

        build_group = parser.add_argument_group("Building Project")
        build_group.add_argument(
            "-i",
            "--icon",
            type=str,
            dest="icon_file",
            metavar="<FILE.ico>",
            help="FILE.ico: apply the icon to a bundled app."
            "some default (default: apply Xodex's icon). This option can be used multiple times.",
        )

        build_group.add_argument(
            "--onefile", action="store_true", help="Create a single executable"
        )
        build_group.add_argument(
            "--noconsole", action="store_true", help="Hide Console"
        )
        build_group.add_argument(
            "--interactive", action="store_true", help="Interactivity"
        )

        # Creating Project Parser & Arguments.
        create_parser = subparsers.add_parser("startgame", help="Create a new project.")
        create_parser.add_argument(
            "--name",
            "-n",
            type=str,
            nargs="?",
            dest="name",
            help="Name of Executable (defaults to Project Name)",
            metavar="NAME",
        )

        create_parser.add_argument(
            "--template",
            "-t",
            type=str,
            nargs="?",
            dest="template",
            help="Template to Generate Project From",
            metavar="PATH",
        )

        create_parser.add_argument(
            "--interactive", action="store_true", help="Run the game"
        )
        create_parser.add_argument("--dryrun", action="store_true", help="Run the game")
        create_parser.add_argument(
            "--extra", action="store_true", help=" Add extra files ie .gitignore"
        )

        # Project Help Parser & Arguments.
        parser_help = subparsers.add_parser("help", help="Shows Help Menu.")
        parser_help.add_argument(
            "--name",
            "-n",
            type=str,
            nargs="?",
            dest="name",
            help="What to help with.",
        )

        # Add new subcommands
        parser_pause = subparsers.add_parser("pause", help="Pause the game")
        parser_resume = subparsers.add_parser("resume", help="Resume the game")
        parser_reload = subparsers.add_parser("reloadscene", help="Reload current scene")
        parser_debug = subparsers.add_parser("toggledebug", help="Toggle debug overlay")
        parser_fps = subparsers.add_parser("showfps", help="Toggle FPS display")
        parser_list = subparsers.add_parser("listscenes", help="List all registered scenes")

        # Parse the CLI arguments
        args = parser.parse_args(self.argv[1:])

        if args.help == "help":
            self.print_help()
            return

        # Starting Project
        if args.subcommand == "startgame":
            name = args.name
            if not name:
                name = input("Enter the name for your game: ").strip()
            if not name:
                cprint("Error: Game name is required.", "RED")
                return
            self.generate(name=name, interactive=args.interactive, dry_run=args.dryrun)
            return

        # Running Project
        if args.subcommand == "run":
            self.run_game()
            return

        # Building Project
        if args.subcommand == "build":
            name = args.name
            if not name:
                name = input("Enter the name of the game to build: ").strip()
            if not name:
                cprint("Error: Game name is required.", "RED")
                return

            self.build(
                project_name="",
                build_name=name,
                onefile=not args.onefile,
                console=args.noconsole,
                interactive=args.interactive,
            )
            return

        # Handle new subcommands
        if args.subcommand == "pause":
            self.pause_game()
            return
        if args.subcommand == "resume":
            self.resume_game()
            return
        if args.subcommand == "reloadscene":
            self.reload_scene()
            return
        if args.subcommand == "toggledebug":
            self.toggle_debug()
            return
        if args.subcommand == "showfps":
            self.toggle_fps()
            return
        if args.subcommand == "listscenes":
            self.list_scenes()
            return

        # Help Utilities

    def run_game(self, name=None):
        """Run the main game loop."""

        # cwd = os.getcwd()

        # if name:
        #     app_dir = os.path.join(cwd, name, "manage.py")
        #     if not os.path.exists(app_dir):
        #         cprint(f"Game '{name}' does not exist.", "RED")
        #         return
        # else:
        #     name = os.environ.setdefault("XODEX_SETTINGS_MODULE", "hello.settings")
        #     app_dir = os.path.join(cwd, "manage.py")
        #     if not os.path.exists(app_dir):
        #         cprint("No Game to Run.", "RED")
        #         return

        # cprint("Starting the game...", "GREEN")
        Game().main_loop()

    def build(self, project_name, build_name, onefile, console, interactive):
        """build"""
        builder = ProjectBuilder(
            project_name=project_name,
            build_name=build_name,
            onefile=onefile,
            console=console,
            interactive=interactive,
        )
        builder.build()

    def generate(self, name:str, interactive, dry_run):
        """Generate a new game/project from template using ProjectGenerator."""
        context = {
            "project_name": name,
            "year": "2025",
            "project_name_upper": name.upper(),
            "xodex_argv": f"startgame {name}",
            "xodex_version": vernum,
            "pygame_version": "2.6.1",
            "pygameui_version": vernum,
            "author": os.getenv("USERNAME") or os.getenv("USER") or "Unknown",
        }
        generator = ProjectGenerator(
            name,
            context=context,
            extra_files=True,
            interactive=interactive,  # Ask user on file conflicts
            dry_run=dry_run,  # Set to True for preview only
            post_hooks=[self.after_generate_hook],
        )
        generator.generate()

    def after_generate_hook(self, generator):
        """Custom post-generation hook example."""
        # You could add more automation here (e.g., git init, open in editor, etc.)

    def print_help(self):
        """Print available commands."""
        help_text = """
Xodex Management Utility

Available commands:
  startgame <name>     Create a new game/project from template
  run                  Run the game
  build                Build the game
  help                 Show this help message
  version              Show version information
"""
        print(help_text)

    def pause_game(self):
        Game().toggle_pause()
        cprint("Game paused.", "CYAN")

    def resume_game(self):
        Game().toggle_pause()
        cprint("Game resumed.", "CYAN")

    def reload_scene(self):
        Game().reload_scene()
        cprint("Scene reloaded.", "CYAN")

    def toggle_debug(self):
        Game().toggle_debug_overlay()
        cprint("Toggled debug overlay.", "CYAN")

    def toggle_fps(self):
        game = Game()
        game._show_fps = not game._show_fps
        cprint(f"Show FPS: {game._show_fps}", "CYAN")

    def list_scenes(self):
        from xodex.scenes.manager import SceneManager
        scenes = SceneManager().list_scenes()
        cprint("Registered scenes:", "CYAN")
        for scene in scenes:
            cprint(f"  {scene}", "CYAN")


def execute_from_command_line(argv=None):
    """Run Management Utility."""
    utility = ManagementUtility(argv)
    utility.execute()
