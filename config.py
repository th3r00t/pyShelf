class Config:
   """Main System Configuration"""
   def __init__(self):
      self.book_path = "books/"
      self.book_shelf = "data/shelf.json"
      self.file_array = [
         "data/catalogue.json",
         "data/shelf.json",
         "conf/settings.json"
         ]
      self.auto_scan = True