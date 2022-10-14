# freez
> *Create executables from interpreted language programs on any minimally configured system.*


`freez` takes an entry point script for a program and freezes the entire program into an executable file. `freez` has dependency resolution built in, so can be used on any system with a python interpreter' and can build any intepreted program, regardless of the dependencies within it.

> ***NOTE:** Intergrated terminals in certain programs may have to be restarted for changes to take effect.*

## Requirements

- Python >= 3.6
- Pip must be in the system `PATH`
- \*MacOS **only\***: Comamnd Line tools for Mac

## Usage

```
Usage: freez [OPTIONS] ENTRY COMMAND [ARGS]...

  Create executables from interpreted language programs. Intergrated terminals
  in certain programs may have to be restarted for changes to take effect.

  ENTRY: The entry point script of the program being built.

Options:
  --version        Show the version and exit.
  -g, --global     A flag representing if a global launch script should be
                   created for the executable.
  -n, --name TEXT  Name of the executable bundle (defaults to name of entry
                   point script).
  --help           Show this message and exit.

Commands:
  setup  Setup the Freez environment and launcher.
```

## Installation

# TODO: should we make `src` a module or should they have to cd into it to access the modules inside?
First, setup `freez` on your system:

```
> cd freez
> python -m src.setup setup

This will setup

> freez --version
freez, version 1.5.2
```

This builds `freez` as an executable, meaning it can be run without invoking `python` anywhere on the system. This also means that `freez` is now independent of Python, so python can be removed from this system if desired.

#### **Cross-Platform**
`freez` builds exectuables for the system it was called from, so for cross-platform systems (for example WSL workflows), it's recommended **not** to build `freez` but instead run it from source through the python intepreter to prevent having to simultansously maintain multiple installations across platforms.