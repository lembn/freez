# Freezers
A "**freezer class**" is a Python class inheriting from the class `Freezer` defined in `freezer.py`. These classes cotain methods that build ("freeze") repositories into executable applications.

## Contribution
Freezer classes only need to implement the `freez` method declared in the `freezer.Freezer` class and if you have an idea for a new freezer class, or an improvement on an existing one, please submit a pull request with your feature at Freez's [Github repository](https://github.com/thendg/freez).

TODO: what is does my freezer have to do?

## [`PythonFreezer`](python_freezer.py)
This class creates freezers for Python applications using [PyInstaller](https://pyinstaller.org/en/stable/). The main functionality is esentially a wrapper around PyInstaller, adding support for automatic dependency resolution.