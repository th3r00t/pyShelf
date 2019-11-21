import os

from ..lib.config import Config


class TestConfig:
    config = Config(os.path.abspath(os.path.curdir))

    def test_book_dir(self):
        assert os.path.isdir(self.config.book_path)

    def test_title(self):
        assert "pyShelf" in self.config.TITLE

    def test_version(self):
        assert self.config.VERSION is not None
