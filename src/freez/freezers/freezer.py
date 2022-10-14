import utils


class Freezer:
    def __init__(self, name: str) -> None:
        self.name = name
        self.__cleanup_paths: list[str] = []

    def freeze(self, entry: str) -> None:
        pass

    def cleanup(self) -> None:
        for path in self.__cleanup_paths:
            utils.general.delete(path)

    def install(self) -> None:
        utils.logging.log("Installing...")
        launcher_path = utils.general.app_path(self.name + utils.platform.SCRIPT_EXT)

        with open(launcher_path, "w") as file:
            launcher_script = utils.general.app_path(
                self.name,
                self.name,
            )
            file.write(launcher_script)
        utils.logging.log("Installation complete.", color="green")

    def _add_cleanup_path(self, path: str) -> None:
        if not self.__cleanup_paths:
            self.__cleanup_paths = [path]
        else:
            self.__cleanup_paths.append(path)
