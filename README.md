# pyShelf
A simple terminal based ebook server

Frustrated with Calibre being my only option for hosting my eBook collection, I have decided to spin up my own.

Calibre is a great organizational tool for your books, however not having a terminal based option for running and maintaining
a server is cumbersome when running on a headless server. Thus I am creating pyShelf and I hope to be able to provide all
the functionality required to organize and host all your local ebooks.

I am open to and hoping for community help in the design and execution of this program.

## Current Features
Currently pyShelf will recursively scan your collection, extract and store some metadata in the sqlite database.

## Future Goals
* HTML Frontend for file transfers
* HTML Backend for catalogue maintenance
* Terminal Backend for catalogue maintenance
* Calculate page count from total characters
* Move towards sqlAlchemy and enable user to specify desired storage system
* Android app for easy integration with your catalogue
