# pyShelf 0.6.0

<p align="center"><b>Terminal based ebook server. Open source & Lightweight.</b></p>
<p align="center">Having used Calibre for hosting my eBook collection in the past, I found myself frustrated having to install X on my server, or manage my library externally, Thus I have decided to spin up my own.</p>


<p align="center"><a href="https://pyshelf.com">https://pyshelf.com</a></p>

![pyShelf 0.6.0 newui](https://github.com/th3r00t/pyShelf/raw/master/src/interface/static/img/pyShelf_frontend_0_2_0.png)

### You dont need an X server to host a website, or your Movie & Tv collection, so why should you need one to host ebooks?

_Other solutiions require you to have access to an X server to at the very least generate your book database, pyShelf doesnt.We aim to provide a fully featured ebook server with minimal requirements, and no reliance on X whatsoever._

Follow or influence development @ <p align="center"><b>
    <a href="https://discord.gg/H9TbNJS">Discord</a>
    | <a href="https://webchat.freenode.net/#pyshelf">IRC</a>
</b></p>


## Current Features

* Recursive Scanning
* [Django](https://www.djangoproject.com/) based frontend
* Seach via author, title, & file name fields.
* Download System
* Automated Collections
    * A work in progress, the collections are based on your folder structure.
* User System
* Per User Favorites
* Expanded book information view
* Websocket server
    * currently only responds to ping, and importBooks, more responders are planned.
* Full Docker integration.
* On Demand Importing

| Branch | Support | Feature set |
| --- | --- | --- |
| <b>Master<b> | Bugs get priority | Most stable branch, may be behind in the core feature set |
 | <b>Development</b>| Please report all bugs | Most active branch, this branch is a rolling release, containing the latest features. There will be bugs here hopefully nothing service killing |
 | <b>Others</b> | Here there be dragons | These branches are used for day to day development, nothing here should be considered stable.

## Currently Supported Formats

* epub
* mobi

## 0.6.0 Patch Notes.

# New Features

* Automated Collections
    * A work in progress, the collections are based on your folder structure.
* User System
* Per User Favorites
* Expanded book information view
* Websocket server
    * currently only responds to ping, and importBooks, more responders are planned.
* Full <b>Docker</b> integration.
* On Demand Importing
* .mobi Support 
* Result set ordering
    * You can now choose to order your results:
        * Title
        * Author
        * Categories
        * & Tags
* Reworked UI/UX
    * More intuitive, less intrusive, & stays out of the way. <i>caveat: I need to rework the placement of the next & previous page controls. While they do remain usable, I intend to have them follow the users</i>
        position on the page in future releases.

![pyShelf 0.6.0 navbar](https://github.com/th3r00t/pyShelf/raw/master/src/interface/static/img/navbar.png)

* New controls
    * Sort
    * Ascending / Descending result set
    * Display of the result set count, and your current position in the set.
    * A pop over layer to hold things like
        * [x] User login & Registration
        * [x] Control panel
        * [x] Book details

## Installation & Support Information

# Installation

## Docker

The official Docker image for pyShelf is [`pyshelf/pyshelf`](https://hub.docker.com/r/pyshelf/pyshelf). The easiest way to get pyShelf running is through `docker-compose`. An example docker-compose.yml is included in the repo

You'll need a `.env` file wich sets the `LOCAL_BOOK_DIR` variable, for example:

```
LOCAL_BOOK_DIR=/home/someone/books
```

The Docker image is still new, so there could still be some issues and missing features. Feel free to create a bug-issue when you encounter a bug. Development of the Docker image is discussed in https://github.com/th3r00t/pyShelf/pull/53 . Currently the database needs to be [PostgreSQL](https://www.postgresql.org/) with the account details shown in the example `docker-compose.yml`.

## Self Hosted
This is targeted towards Network Administrators, and home enthusiasts whom I assume will know how to setup a [Django](https://www.djangoproject.com/) app, and a [PostgreSQL](https://www.postgresql.org/) server. For those unfamiliar with the required setup please use the included docker-compose.yml

### Pre-req Dependencies

* gcc
* python3
* pip
* postgresql

Once your database is ready very little is required to get the system up and running:

From the main directory

`pip install -r requirements.txt`

`./configure`

`cd src/ && daphne frontend.asgi:application` add -b 0.0.0.0 -p 8000 as required to specify which interface\'s and port to bind too

As of 0.6.0 Django is being served up via Daphne, and the static files are served up via whitenoise.

## Import Books
The first step is to login, after logging in the button whill show your username, click on it once again, and a new menu will pop up with the option to logout, or import books.

## In Progress

### Organizational tools.

- [x] Automated Collections
- [ ] Manual Collections
- [ ] Books Removal
- [ ] Access Restrictions
- [ ] Metadata Manipulation
- [ ] Others?

### Improved cover image storage, and acquisition.

### OPDS Support

### Support for other formats

- [x] .mobi
- [ ] .pdf
- [ ] .cbz
- [ ] .zip (Zipped book folders, is this a new idea? (Consider storing your library folders zipped and retrieving a book on demand))

## Future Goals

### Terminal Backend for catalogue maintenance

## Development

* [`pre-commit`](https://pre-commit.com/)
_Before developing, run `pre-commit install` See the [documentation](https://pre-commit.com/) for more information._
* ['Doxygen'](http://www.doxygen.nl/)
_Any changes to source should be documented and have run doxygen doxygen.conf prior to commiting._
* ['sem-ver'](https://semver.org)
_Before advancing version numbers be sure to set PROJECT_NUMBER in doxygen.conf accordingly._
