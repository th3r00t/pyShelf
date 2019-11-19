# pyShelf 0.1.0
A simple terminal based ebook server

Frustrated with Calibre being my only option for hosting my eBook collection, I have decided to spin up my own.

Calibre is a great organizational tool for your books, however not having a terminal based option for running and maintaining
a server is cumbersome when running on a headless server.
Calibre does have a console based server solution, However there is currently no way to create, and manage your library in a headless enviroment.

Thus I am creating pyShelf and I hope to be able to provide all the functionality required to organize and host all your ebooks.

I am open to and hoping for community help in the design and execution of this program.

## Development

pyShelf uses [`pre-commit`](https://pre-commit.com/) to automate some tasks.
Before developing, run `pre-commit install`.
See the [documentation](https://pre-commit.com/) for more information.

pyShelf uses ['Doxygen'](http://www.doxygen.nl/) for source code documentation.
Any changes to source should be documented and have run doxygen doxygen.conf prior to commiting.

pyShelf follows ['sem-ver'](https://semver.org) standards. Before advancing version numbers be sure to set PROJECT_NUMBER in doxygen.conf accordingly.

## Configuration
All pyShelf configuration is done in config.py.

### Nginx configuration
I have included a default nginx config file pyshelf_nginx.conf. This file should be sufficient to get you up and running. You are required to change the location alias's to reflect your pyshelf install folder leaving everything after /frontend intact.

Further resources for nginx setup may be found @ [This nginx, django, & uwsgi, guide](https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html)

### uwsgi configuration
Inside uwsgi.ini you should make changes to reflect your install directory, and the port you wish uwsgi to listen on. Alternativly you can make the requisite changes to listen on a socket instead. This change would also require a change to the pyshelf_nginx.conf file as well.

### pyShelf configuration
User configuration is contained within config.json in the project root. The only currently required configuration is to set book_path to the location of your books.

## Current Features
Currently pyShelf will recursively scan your collection, extract and store some metadata in the sqlite database. It will also provide you with a web based frontend to view and download your books. Note that this is a very early alpha and lacking the ability to sort and search your collection. This feature is coming however.

Django has been implemented to power the frontend experience, and web based database maintenance. The first steps of which are included in this commit. Also the book database has been switched over to reflect this. A properly configured web server is required for hosting the frontend, configuration of which is outside of the scope of this readme. Running via the Django test server might be possible, albeit not recomended.

## In Progress

* UI/UX tweaks, including making the book display responsive. and not so ugly.
* Searching, & further organizational tools.
* Improved cover image storage, and acquisition.

## Future Goals
* Support for other book formats (Currently on supporting EPUBS)
* Terminal Backend for catalogue maintenance
* Calculate page count from total characters
  * (Thanks to @Fireblend for the idea) https://github.com/th3r00t/pyShelf/issues/3
* Move towards sqlAlchemy and enable user to specify desired storage system
  * (Thanks to Sarcism) over on r/opensource for this idea!
* Android app for easy integration with your catalogue
