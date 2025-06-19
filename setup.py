import os
from setuptools import setup, find_packages
from xodex.version import vernum


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
        exclude=['test'],
        include=["xodex", "xodex.core", "xodex.objects", "xodex.scenes", "xodex.utils", "xodex.contrib", "xodex.game", "xodex.conf"]
        ),
    py_modules=["xodex"],
    install_requires=["pygame>=2.0.0",],
    extras_require={
        "dev": ["pytest", "black","isort"],
        "docs": ["sphinx"],
    },
    python_requires=">=3.9",
    keywords=[
        "pygame", "game engine", "2d", "xodex", "games", "engine", "framework"
    ],
    platforms=["any"],
    classifiers=[
        "Development Status :: 1 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: pygame",
        "Typing :: Typed",
    ],
    setup_requires=['setuptools', "wheel"],
    options={'bdist_wheel': {'universal': False}},
    entry_points={
        'pyinstaller40': ['hook-dirs = xodex.conf.hook:get_hook_dirs'],
        "console_scripts": ["xodex=xodex.__main__:execute_from_command_line",],
    },
    zip_safe=False,
    include_package_data=True,
)
