"""
Xodex Game Engine Command-Line Entrypoint

This module allows you to run Xodex management commands directly from the command line.

Usage Examples:
    python -m xodex startapp MyGame
    python -m xodex run
    python -m xodex help

How it works:
- This script delegates command-line arguments to the Xodex management utility.
- You can use it to scaffold new projects, run your game, or perform other management tasks.

See the Xodex documentation for a full list of available commands and options.
"""

from xodex.core import management

if __name__ == "__main__":
    management.execute_from_command_line()
