"""Management"""

import os
import sys
import pathlib
import argparse
import re
import subprocess

try:
    from colorama import Fore, Style, init as colorama_init

    colorama_init()
    COLOR_ENABLED = True
except ImportError:
    COLOR_ENABLED = False

from xodex.game.game import Game

__all__ = ("ManagementUtility", "execute_from_command_line")


def cprint(text, color=None):
    """cprint"""
    if COLOR_ENABLED and color:
        print(getattr(Fore, color.upper(), "") + text + Style.RESET_ALL)
    else:
        print(text)


class ProjectBuilder:
    """
    Handles creation of new projects, including directory structure, initial files,
    and building standalone executables using PyInstaller.
    """

    def __init__(self, project_name):
        self.project_name = project_name
        self.project_dir = os.path.abspath(project_name)

    def create_project_structure(self):
        try:
            os.makedirs(self.project_name, exist_ok=False)
            with open(os.path.join(self.project_name, "main.py"), "w") as f:
                f.write(
                    "# Entry point for the project\n\n"
                    "if __name__ == '__main__':\n"
                    "    print('Hello, Xodex!')\n"
                )
            with open(os.path.join(self.project_name, "__init__.py"), "w") as f:
                f.write("# Init file for project package\n")
            cprint(f"Project '{self.project_name}' created successfully.", "GREEN")
        except FileExistsError:
            cprint(f"Error: Project '{self.project_name}' already exists.", "RED")
        except Exception as e:
            cprint(f"Error creating project: {e}", "RED")

    def build_exe(self, onefile=True, console=True):
        """
        Build an executable from main.py using PyInstaller.
        """
        main_py = os.path.join(self.project_dir, "main.py")
        if not os.path.exists(main_py):
            cprint(f"main.py not found in {self.project_dir}.", "RED")
            return

        pyinstaller_cmd = [
            sys.executable,
            "-m",
            "PyInstaller",
            "--distpath",
            os.path.join(self.project_dir, "dist"),
            "--workpath",
            os.path.join(self.project_dir, "build"),
            "--specpath",
            os.path.join(self.project_dir, "build"),
        ]
        if onefile:
            pyinstaller_cmd.append("--onefile")
        if not console:
            pyinstaller_cmd.append("--noconsole")
        pyinstaller_cmd.append(main_py)

        cprint("Building executable with PyInstaller...", "CYAN")
        try:
            result = subprocess.run(
                pyinstaller_cmd,
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                check=True,
            )
            cprint("Executable built successfully!", "GREEN")
            exe_name = "main.exe" if os.name == "nt" else "main"
            exe_path = os.path.join(self.project_dir, "dist", exe_name)
            if os.path.exists(exe_path):
                cprint(f"Executable located at: {exe_path}", "CYAN")
            else:
                cprint(
                    "Build finished, but executable not found in expected location.",
                    "YELLOW",
                )
        except subprocess.CalledProcessError as e:
            cprint("PyInstaller failed to build the executable.", "RED")
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

            # # Add a README.md if not present
            # readme_path = os.path.join(self.main_dir, "README.md")
            # if not os.path.exists(readme_path) and not self.dry_run:
            #     with open(readme_path, "w", encoding="utf-8") as f:
            #         f.write(f"# {self.name}\n")

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
        )
        parser.add_argument("--version", action="version", version="0.0.1")

        subparsers = parser.add_subparsers(dest="subcommand", help="Subcommands")

        # startgame
        parser_startgame = subparsers.add_parser(
            "startgame", help="Create a new game/project from template"
        )
        parser_startgame.add_argument(
            "name", nargs="?", help="Name of the game to create"
        )

        # run
        subparsers.add_parser("run", help="Run the game")

        # help
        subparsers.add_parser("help", help="Show this help message")

        # rungame
        parser_rungame = subparsers.add_parser(
            "rungame", help="Run a specific game game"
        )
        parser_rungame.add_argument("name", nargs="?", help="Name of the game to run")

        args = parser.parse_args(self.argv[1:])

        if not args.subcommand or args.subcommand == "help":
            self.print_help()
            return

        if args.subcommand == "startgame":
            name = args.name
            if not name:
                name = input("Enter the name for your game: ").strip()
            if not name:
                cprint("Error: Game name is required.", "RED")
                return
            self.generate(name)
            return

        if args.subcommand == "rungame":
            name = args.name
            if not name:
                name = input("Enter the name of game to Run: ").strip()
            if not name:
                cprint("Error: Game name is required.", "RED")
                return
            self.run_game(name)
            return

        if args.subcommand == "run":
            self.run_game()
            return

    def run_game(self, name=None):
        """Run the main game loop."""

        cwd = os.getcwd()

        if name:
            app_dir = os.path.join(cwd, name, "manage.py")
            if not os.path.exists(app_dir):
                cprint(f"Game '{name}' does not exist.", "RED")
                return
        else:
            app_dir = os.path.join(cwd, "manage.py")
            if not os.path.exists(app_dir):
                cprint("No Game to Run.", "RED")
                return

        cprint("Starting the game...", "GREEN")
        Game().main_loop()

    def generate(self, name):
        """Generate a new game/project from template using ProjectGenerator."""
        # Example: add more context, enable interactive mode, dry-run, or custom hooks
        context = {
            "project_name": name,
            "xodex_argv": f"startgame {name}",
            "xodex_version": "0.0.1",
            "author": os.getenv("USERNAME") or os.getenv("USER") or "Unknown",
        }
        generator = ProjectGenerator(
            name,
            context=context,
            extra_files=True,
            interactive=True,  # Ask user on file conflicts
            dry_run=False,  # Set to True for preview only
            post_hooks=[self.after_generate_hook],
        )
        generator.generate()

    def after_generate_hook(self, generator):
        """Custom post-generation hook example."""
        # cprint(
        #     f"Custom hook: Project '{generator.name}' generated at {generator.main_dir}",
        #     "CYAN",
        # )

        # You could add more automation here (e.g., git init, open in editor, etc.)

    def print_help(self):
        """Print available commands."""
        help_text = """
Xodex Management Utility

Available commands:
  startgame <name>     Create a new game/project from template
  rungame <name>       Run a Specific Game.
  run                  Run the game
  help                 Show this help message
  version              Show version information
"""
        print(help_text)


def execute_from_command_line(argv=None):
    """Run Management Utility."""
    utility = ManagementUtility(argv)
    utility.execute()
