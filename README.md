# freez

Create single-file executables from python programs ony any python-running system. `freez` takes the entry point script for a program and freezes the entire program it into a single-file executable using [PyInstaller](https://github.com/pyinstaller/pyinstaller). `freez` has no external dependencies, so can be used on any system with a python interpreter and can build any python program, regardless of the dependencies within it. `freez` requries an internet connection to build programs so that dependencies can be fetched from external locations. `freez` uses to freeze programs, providing the main functionality of the program.

> The entry point script of the program being built should be away from the `freez` directory.

## Why not use normal PyInstaller?

PyInstaller will fail if you try to build a program that uses external dependencies which you do not have installed on your system. All `freez` does is collect these dependencies and install them into a virtual environment, allowing PyInstaller to build in that environment and also allowing the installed dependencies to be easily cleaned off the system as if they were never there. This way any python program can be built into an executable from it's source code without the build machine having any of the program's dependencies pre-installed.

## Requirements

- Python >= 3.6
- Pip must be in the system `PATH`
- \*MacOS **only\***: Comamnd Line tools for Mac

## Usage

```
Usage: [python] freez [OPTIONS] ENTRY

  Create single-file executables from python scripts.

  ENTRY: The entry point script of the program being built.

Options:
  -o, --output DIRECTORY  Output folder of the built executable.  [default:
                          ./]
  -n, --name TEXT         Name of the built executable (defaults to name of
                          entry point script).
  -g, --global            Install the executable into the python script path
                          to make it globally accessible across the system
                          (this will ignore the path set by --output).
  --help                  Show this message and exit.
```

> Global installations require 'sudo' on Unix.

## Installation

Since `freez` is a python program, it can actually be used to install itself globally across the system:

```
> cd freez
> python main.py -g -n freez main.py
> freez --version
freez, version 1.4.0
```

This builds `freez` as an executable, meaning it can be run without invoking `python` anywhere on the system.
