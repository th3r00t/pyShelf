class Config:
    """Main System Configuration"""
    def __init__(self):
        self.book_path = "books/"
        self.TITLE = "pyShelf E-Book Server"
        self.book_shelf = "data/shelf.json"
        self.catalogue_db = "data/catalogue.db"
        self.file_array = [
           self.book_shelf,
           self.catalogue_db,
           ]
        self.auto_scan = True
