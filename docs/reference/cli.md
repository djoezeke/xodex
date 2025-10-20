# CLI Reference

## xodex CLI

xodex is a small management CLI that helps you run, build, and manage xodex projects. Use the `xodex` command from a project directory to run commands from the project's `project/management/commands` or the bundled commands.

Usage

```
xodex [OPTIONS] <COMMAND> [ARGS]
```

Common commands (project may add more):

- `xodex run` — Run the current project.
- `xodex init <name>` — Create a new xodex project scaffold.
- `xodex shell` — Open an interactive shell with the project's objects loaded.
- `xodex build` — Build the project into a distributable/executable.
- `xodex version` — Print the xodex version.
- `xodex help <command>` — Show help for a specific command.

See the usage guide for examples and workflows: [Usage](../project.md)

### xodex shell

`xodex shell` opens a developer REPL. Available subcommands vary by project, an example:

```
xodex shell object    # expose registered objects into the shell
```

The CLI uses `BaseCommand` implementations (see `xodex.core.management.command.BaseCommand`) for argument parsing. Custom commands should subclass `BaseCommand` and implement `add_arguments()` and `handle()`.
