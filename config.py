class Config:
   """Main System Configuration"""
   def __init__(self):
      self.book_path = "/home/raelon/Books/"
      self.book_shelf = "data/shelf.json"
      self.catalogue_db = "data/catalogue.db"
      self.file_array = [
         "data/catalogue.json",
         self.book_shelf,
         self.catalogue_db,
         "conf/settings.json"
         ]
      self.auto_scan = True
