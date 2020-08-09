# pyShelf 0.6.0

<p align="center"><b>Terminal based ebook server. Open source & Lightweight.</b></p>
<p align="center">Having used Calibre for hosting my eBook collection in the past, I found myself frustrated having to install X on my server, or manage my library externally, Thus I have decided to spin up my own.</p>
<p align="center"><a href="https://pyshelf.com">https://pyshelf.com</a></p>

![pyShelf 0.6.0 newui](https://github.com/th3r00t/pyShelf/raw/development/src/interface/static/img/pyShelf_frontend_0_2_0.png)


### You dont need an X server to host a website, or your Movie & Tv collection, so why should you need one to host ebooks?

_Other solutiions require you to have access to an X server to at the very least generate your book database, pyShelf doesnt.We aim to provide a fully featured ebook server with minimal requirements, and no reliance on X whatsoever._

Follow or influence development @ <p align="center"><b>
    <a href="https://discord.gg/H9TbNJS">Discord</a>
    | <a href="https://webchat.freenode.net/#pyshelf">IRC</a>
    | <a href="https://app.element.io/#/room/#irc_#pyshelf:pyshelf.com">Matrix.org</a>
</b></p>

## Current Features

* Recursive Scanning
* PostgreSql Library
* [Django](https://www.djangoproject.com/) based frontend
* Basic seaching via a SearchVector of author, title, & file_name fields.
* Ebook Downloading
* Collections
* User System

## Currently Supported Formats

* epub
* mobi

## 0.6.0 Patch Notes.

# New Features

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

![pyShelf 0.6.0 navbar](https://github.com/th3r00t/pyShelf/raw/development/src/interface/static/img/navbar.png)

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

This project is targeted towards Network Administrators, and home enthusiasts whom I assume will know how to setup a [Django](https://www.djangoproject.com/) app, and a [PostgreSQL](https://www.postgresql.org/) server. For those unfamiliar with the required setup please see the docker section below.

### Pre-req Dependencies

* gcc
* python3
* pip

setup configurations as discussed in [SUPPORT.md](https://github.com/th3r00t/pyShelf/blob/development/.github/SUPPORT.md)

Once your environment is ready very little is required to get the system up and running:

From the main directory

`pip install -r requirements.txt`

`./configure`

`cd src`

`python manage.py makemigrations`

`python manage.py makemigration interface`

`python manage.py migrate`

`python manage.py migrate interface`

`cd ..`

`./importBooks`

`uwsgi --ini uwsgi.ini`

Browse to the site as defined in your apache | nginx config

Running via the [Django](https://www.djangoproject.com/) test server might be possible, albeit not recomended.

## Docker

The official Docker image for pyShelf is [`pyshelf/pyshelf`](https://hub.docker.com/r/pyshelf/pyshelf). The easiest way to get pyShelf running is through `docker-compose`. Here is an example `docker-compose.yml`:

```
version: "3.7"

services:
    db:
        image: "postgres"
        environment:
            - "POSTGRES_PASSWORD=pyshelf"
            - "POSTGRES_USER=pyshelf"
            - "POSTGRES_DB=pyshelf"
        volumes:
            - "db_data:/var/lib/postgresql/data/"

    pyshelf:
        image: "pyshelf/pyshelf"
        ports: 
            - "8080:8000"
        volumes:
            - "${LOCAL_BOOK_DIR}:/books"
        depends_on:
            - db

volumes:
    db_data:
```

You'll also need a `.env` file wich sets the `LOCAL_BOOK_DIR` variable, for example:

```
LOCAL_BOOK_DIR=/home/someone/books
```

The Docker image is still new, so there could still be some issues and missing features. Feel free to create a bug-issue when you encounter a bug. Development of the Docker image is discussed in https://github.com/th3r00t/pyShelf/pull/53 . Currently the database needs to be [PostgreSQL](https://www.postgresql.org/) with the account details shown in the example `docker-compose.yml`. It should become db agnostic in the future.

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
