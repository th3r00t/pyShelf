# pyShelf
A simple terminal based ebook server

Frustrated with Calibre being my only option for hosting my eBook collection, I have decided to spin up my own.

Calibre is a great organizational tool for your books, however not having a terminal based option for running and maintaining
a server is cumbersome when running on a headless server. 
Calibre does have a console based server solution, However there is currently no way to create, and manage your library in a headless enviroment.

Thus I am creating pyShelf and I hope to be able to provide all the functionality required to organize and host all your ebooks.

I am open to and hoping for community help in the design and execution of this program.
## Configuration
All configuration is done in config.py.
The only currently required configuration is to set book_path to the location of your books.
## Current Features
Currently pyShelf will recursively scan your collection, extract and store some metadata in the sqlite database.
The basic template system is in place, as well as a template mockup. This can be seen hosted on port 8000

## Future Goals
* HTML Frontend for file transfers
* HTML Backend for catalogue maintenance
* Terminal Backend for catalogue maintenance
* Calculate page count from total characters 
  * (Thanks to @Fireblend for the idea) https://github.com/th3r00t/pyShelf/issues/3
* Move towards sqlAlchemy and enable user to specify desired storage system
  * (Thanks to Sarcism) over on r/opensource for this idea!
* Android app for easy integration with your catalogue
