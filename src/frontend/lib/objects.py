"""pyShelf's Frontend Objects."""
from subprocess import run
from pathlib import Path
from backend.lib.config import Config


class JSInterface():
    """A class to interface with the JavaScript side of pyShelf."""

    def __init__(self, config: Config):
        """Initialize the JSInterface object."""
        self.package_json: Path = Path(config.root, "src/frontend/package.json")
        self.config: Config = config

    def install(self):
        """Install the JavaScript dependencies."""
        run(["npm", "install"], cwd=self.package_json.parent)
        run(["npx", "tsc", "static/script/pyshelf.ts"], cwd=self.package_json.parent)
