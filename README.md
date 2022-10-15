# freez
> *Build executables from interpreted language programs.*


`freez` takes an entry point script for a program and freezes the entire program into an executable file. `freez` has automatic dependency resolution built in, so can be used on any system with a python interpreter and can build any intepreted program, regardless of the dependencies within it.

## Requirements
- Python >= 3.6
- *MacOS **only***: Comamnd Line tools for Mac

## Initialisation
All you need to do to get running is, clone the `freez` repository, then initialise `freez` on your system:

```
> git clone https://www.github.com/thendg/freez.git
> cd freez
> python -m src.init
```

This final command will output a the path to the freez `apps` directory, where `freez` itself (and all the executables built by it) can be accessed. If you add this directory path to your system's PATH environment variable, you'll be able to globally execute `freez` (and all the executables built by it) from anywhere on your system. After doing this you can restart your shell and run `freez --version`  to test the installation. At this point `freez` is still dependent on the installed Python environment, but can be invoked by it's name `freez` from anywhere on the system (and the launcher will figure out the rest).

#### **Installation**
If you so desire, you could even get `freez` to *build and install itself*, with:

```
> git clone https://www.github.com/thendg/freez.git
> cd freez
> python -m src.freez -n freez "src/freez/__main__.py"
```

However, this will build `freez` as an executable specific to the build system so, for cross-platform systems (for example WSL workflows), it's recommended **not** to do this. Since the launcher runs `freez` inside the currently installed Python environment, `freez` is actually cross-platform in it's default configuration since the execution process is delegated to the Python executable.

## Usage
```
Usage: freez [OPTIONS] ENTRY COMMAND [ARGS]...

  Create executables from interpreted language programs. Intergrated shells
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

## How does it work?
Good question. Organisationally, the `freez` project is split into three Python packages, all located in the `src` subdirectory.

#### **`init`**
The `init` package is used when initialising `freez`. This package is invoked as a module and contains the code required to setup `freez` and its dependencies on a system. 

#### **`freez`**
The `freez` package contains the actual `freez` application. This package is split into two sub-packages. `commands` contains the logic for the commands used by the `freez` application, `freezers` is a suite of *"freezer classes"* that can be used to build applications.

A "**freezer classes**" is a Python class defining some methods that describe how a source repository should be "frozen" into an executable. More infomration can be found on them [here](src/freez/freezers/README.md)

#### **`utils`**
The `utils` package contains utilities used across the other packages.