import json
import os

from ..lib.config import Config
from ..lib.library import Catalogue


class Test_Config(Config):
    def __init__(self):
        Config.__init__(self, 'config.json')
        _data = self.open_file()

    def open_file(self, root='config.json'):
        with open('config.json') as read_file:
            data = json.load(read_file)
        return data


class Test_Catalogue(Catalogue):

    def __init__(self):
        Catalogue.__init__(self, root=os.path.abspath('.'))

    def filter_books(self):
        self.book_shelf = 'app/'+self.book_shelf
        return super().filter_books()


class TestCatalogue:
    root = os.path.abspath(os.path.curdir)
    config = Test_Config()

    def test_filter_books(self):
        book_list = Test_Catalogue().filter_books()
        assert len(book_list) > 0
