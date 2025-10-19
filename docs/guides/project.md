---
title: Working on projects
description: A guide to using xodex to create and building apps and games.
---

# Working on projects

xodex supports managing project, which define their configurations in a `settings.py` file.

## Creating a new project

You can create a new Python project using the `xodex init` command:

```console
$ xodex init hello-world
$ cd hello-world
```

Alternatively, you can initialize a project in the working directory:

```console
$ mkdir hello-world
$ cd hello-world
$ xodex init
```

xodex will create the following files:

```text
├── LICENSE
├── README.md
├── manage.py
├── .gitignore
└── requirements.txt
```

The `main.py` file contains a simple "Hello world" program. Try it out with `xodex run`:

```console
$ xodex run main.py
Hello from hello-world!
```

## Project structure

A project consists of a few important parts that work together and allow xodex to manage your project.

A complete listing would look like:

```text
.
├── project
│   ├── __init__.py
│   ├── __main__.py
│   ├── objects.py
│   ├── scenes.py
│   └── settings.py
├── LICENSE
├── README.md
├── manage.py
├── .gitignore
└── requirements.txt
```

### `settings.py`

The `settings.py` contains metadata about your project:

```python title="settings.py"
# --- Window & Display ---
FPS = 60  # Target frames per second
WIDTH = 720  # Window width in pixels
HEIGHT = 560  # Window height in pixels
WINDOW_SIZE = (WIDTH, HEIGHT)
TITLE = "Xodex Game Engine"  # Window title
VERSION = "0.1.0"  # Game version string
FULLSCREEN = False  # Set to True for fullscreen mode
ICON_PATH = None  # Set to a path to your window icon, e.g. "asset/icon.png"
```

### `objects.py`

### `scenes.py`

### `manage.py`
