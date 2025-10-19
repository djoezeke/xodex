# Getting help

## Help menus

The `--help` flag can be used to view the help menu for a command, e.g., for `xodex`:

```console
$ xodex --help
```

To view the help menu for a specific command, e.g., for `xodex init`:

```console
$ xodex init --help
```

When using the `--help` flag, xodex displays a condensed help menu. To view a longer help menu for a
command, use `xodex help`:

```console
$ xodex help
```

To view the long help menu for a specific command, e.g., for `xodex init`:

```console
$ xodex help init
```

When using the long help menu, xodex will attempt to use `less` or `more` to "page" the output so it is
not all displayed at once. To exit the pager, press `q`.

## Displaying verbose output

The `-v` flag can be used to display verbose output for a command, e.g., for `xodex build`:

```console
$ xodex build -v
```

The `-v` flag can be repeated to increase verbosity, e.g.:

```console
$ xodex build -vv
```

Often, the verbose output will include additional information about why xodex is behaving in a certain
way.

## Viewing the version

When seeking help, it's important to determine the version of xodex that you're using — sometimes the
problem is already solved in a newer version.

To check the installed version:

```console
$ xodex version
```

The following are also valid:

```console
$ xodex --version      # Same output as `xodex version`
$ xodex -V             # Will not include the build commit and date
```

!!! note

    use `xodex --version` instead of `xodex version`.

## Open an issue on GitHub

The [issue tracker](https://github.com/djoezeke/xodex/issues) on GitHub is a good place to report bugs
and request features. Make sure to search for similar issues first, as it is common for someone else
to encounter the same problem.
