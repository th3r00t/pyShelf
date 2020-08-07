from pathlib import Path
from .config import Config
from .storage import Storage
from .library import Catalogue
import asyncio
import os
import websockets


class ACatalogue(Catalogue):
    """
    Aynchronous overide of library.Catalogue,
    : TODO : Complete or discard this overide
    """
    def __init__(self):
        super().__init__(Config(Paths.cwd().parent))

    async def scan_folder(self, _path=None):
        """
        Scan folder by _path, allows recurisive scanning
        """
        if _path is not None:
            folder = _path
        elif os.path.isdir(str(self.root_dir) + "/" + self.book_folder):
            folder = str(self.root_dir) + "/" + self.book_folder
        else:
            folder = self.book_folder
        for f in os.listdir(folder):
            _path = os.path.abspath(folder + "/" + f)
            if os.path.isdir(_path.strip() + "/"):
                self.file_list.append(self.scan_folder(_path))
            else:
                self.file_list.append(_path)
            await asyncio.sleep(0.001)
        print(_path+"\n")

    async def import_books(self, **kwargs):
        """
        Async overide of import_books
        """
        fsocket = kwargs['socket']
        book_list = self.compare_shelf_current()
        db = Storage(self.config)
        for book in book_list:
            book = self.process_by_filetype(book)
            with open(fsocket, 'w') as _socket:
                _socket.write(book[0])
            _socket.close()
            await db.insert_book(book)
        inserted = db.commit()
        if inserted is not True:
            print(inserted)
            if input("Continue ? y/n") == "y":
                pass
        db.close()
