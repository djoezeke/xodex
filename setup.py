import os

from setuptools import find_packages
from setuptools import setup

from xodex.utils.version import vernum


def readme():
    fname = "README.md"
    if os.path.exists(fname):
        with open(fname, encoding="utf-8") as f:
            return f.read()
    return ""


setup(
    name="xodex",
    version=f"{vernum}",
    author="Sackey Ezekiel Etrue",
    author_email="sackeyetrue@gmail.com",
    maintainer="Sackey Ezekiel Etrue",
    maintainer_email="sackeyetrue@gmail.com",
    description="Python Game Development Engine (Pygame-based)",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/djoezeke/xodex",
    project_urls={
        "Homepage": "https://github.com/djoezeke/xodex",
        "Documentation": "https://github.com/djoezeke/xodex#readme",
        "Issues": "https://github.com/djoezeke/xodex/issues",
        "Release Notes": "https://github.com/djoezeke/xodex/releases",
        "Source": "https://github.com/djoezeke/xodex",
    },
    license="MIT",
    packages=find_packages(
        where=".",
        exclude=["tests"],
        include=[
            "xodex",
            "xodex.core",
            "xodex.game",
            "xodex.conf",
            "xodex.scene",
            "xodex.utils",
            "xodex.object",
            "xodex.contrib",
        ],
    ),
    py_modules=["xodex"],
    install_requires=["pygame>=2.6.1", "pillow>=11.3.0", "rich>=14.1.0"],
    extras_require={
        "dev": [
            # We add xodex[standard] so `uv sync` considers the extras.
            "xodex[standard]",
            "ruff",  # format & check
            "pytest",  # testing
            "twine",  # check dist
        ],
        "docs": [
            "mkdocs==1.6.1",
            "mkdocs-material==9.6.13",
            "mkdocstrings-python==1.16.12",
            "mkdocs-llmstxt==0.2.0",
        ],
    },
    python_requires=">=3.13",
    keywords=["pygame", "game engine", "2d", "xodex", "games", "engine", "framework"],
    platforms=["any"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    entry_points={
        "pyinstaller40": ["hook-dirs = xodex.conf.hook:get_hook_dirs"],
        "console_scripts": [
            "xodex=xodex.__main__:execute_from_command_line",
        ],
    },
    setup_requires=["setuptools", "wheel"],
    options={"bdist_wheel": {"universal": False}},
    zip_safe=False,
    include_package_data=True,
)
