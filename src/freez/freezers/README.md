# Freezers
A "**freezer class**" is a Python class inheriting from the class `Freezer` defined in `freezer.py`. These classes cotain methods that build ("freeze") repositories into executable applications.

## Contribution
Freezer classes only need to implement the `freez` method declared in the `freezer.Freezer` class and if you have an idea for a new freezer class, or an improvement on an existing one, please submit a pull request with your feature at Freez's [Github repository](https://github.com/thendg/freez).

The `freezer.Freezer` base class defines a constructor taking a single argument which is used to set the `name` field of the object - the only public field of the class. This name is the name given to the applciation, for example "`freez`".

The public interface of the class consits of the methods `freeze`, `install` and `cleanup`.

### **`freez`**
`freez` is an abstract method that should be overridden to implement the freezing functionality of the freezer class. This is the only method that needs to be overwritten to implement a `Freezer`. The method provides the absolute file path to the entry point in the parameter `entry`, along with an abosulte path to the output directory in the parameter `output`. This method is responsible for creating an executable for build system in the `output` directory (this is where the application's launcher will expect the executable to be).

### **`install`**
`install` is fully implemented and is responsible for creating the application launchers for frozen applications. These launchers live in the Freez application directory so are accessible on the system's `PATH` environment variable. This allows all of the executables to be run globally from their launcher. Despite their own application directories not being on the `PATH`. All the launcher does is forward execution from the launcher into the executable, however this means we don't have to add each executable to the system's `PATH` individually making the installation (and uninstallation) process much easier to manage.

### **`cleanup`**
`cleanup` simply deletes anything that is found on the freezer's "cleanup paths". You can add something to the freezer's cleanup paths by calling `_add_cleanup_path` from within one of your freezer's methods (probably `freez`). This is used to ensure that the freezers don't leave mess all over the user's system.

## [`PythonFreezer`](python_freezer.py)
This class creates freezers for Python applications using [PyInstaller](https://pyinstaller.org/en/stable/). The main functionality is esentially a wrapper around PyInstaller, adding support for automatic dependency resolution.

TODO: explain