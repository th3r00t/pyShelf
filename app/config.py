class Config:
    """Main System Configuration"""
    def __init__(self):
        self.book_path = "books/"
        self.TITLE = "pyShelf E-Book Server"
        self.VERSION = "0.1.0"
        self.TITLE = self.TITLE + " ver" + self.VERSION
        self.book_shelf = "data/shelf.json"
        # self.catalogue_db = "data/catalogue.db"
        self.catalogue_db = "../frontend/db.sqlite3"
        self.file_array = [
           self.book_shelf,
           self.catalogue_db,
           ]
        self.auto_scan = True
