"""pyShelf's Frontend Objects."""
from sys import exit
from shutil import which
from subprocess import run
from pathlib import Path
from ...backend.lib.config import Config


class JSInterface():
    """A class to interface with the JavaScript side of pyShelf."""

    def __init__(self, config: Config):
        """Initialize the JSInterface object."""
        self.package_json: Path = Path(config.root, "src/frontend/package.json")
        self.config: Config = config

    def install(self):
        """Install the JavaScript dependencies."""
        if which("npm"):
            self.config.logger.info("Installing JavaScript dependencies...")
            run(["npm", "install"], cwd=self.package_json.parent)

        else:
            self.config.logger.error("npm is not installed.")
            exit(1)
        if which("npx"):
            self.config.logger.info("Compiling TypeScript...")
            run(["npx", "tsc", "static/script/pyshelf.ts"], cwd=self.package_json.parent)
        else:
            self.config.logger.error("npx is not installed.")
            exit(1)
