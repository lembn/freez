# freez

Create single-file executables from python scripts ony any python-running system. `freez` takes the entry point script for a program and freezes it into a single-file executable. The entry point script of the program being built should be in a different directory to `freez`'s `main.py`. `freez` has no external dependencies, so can be used on any system with a python interpreter and can build any python program, regardless of the dependencies within it, wihtout requiring the dependencies being installed on the machine. ``freez` requries an internet connection to build programs so that dependencies can be fetched from external locations.

`freez` uses [PyInstaller](https://github.com/pyinstaller/pyinstaller) to freeze programs, providing the main functionality of the program.

## Usage

```
Usage: freez [OPTIONS] ENTRY

  ENTRY: The entry point script of the program being built.

Options:
  -o, --output DIRECTORY  Output folder of the built executable.  [default:
                          ./]
  -n, --name TEXT         Name of the built executable (defaults to name of
                          entry point script).
  --help                  Show this message and exit.
```
