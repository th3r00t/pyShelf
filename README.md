# pyShelf 0.5.0

<p align="center"><b>Terminal based ebook server. Open source & Lightweight.</b></p>
![pyShelf 0.5.0 Collection 1](https://github.com/th3r00t/pyShelf/raw/development/preview_050.png)
![pyShelf 0.5.0 Collection 2](https://github.com/th3r00t/pyShelf/raw/development/preview_1_050.png)

Having used Calibre for hosting my eBook collection in the past, I found myself frustrated having to install X on my server, or manage my library externally, Thus I have decided to spin up my own.

### Join the discussion: Discord [https://discord.gg/H9TbNJS](https://discord.gg/H9TbNJS) | IRC freenode.net @ #pyshelf

## Current Features
* Custom Installer -- For Arch Based Distros Only
* Recursive Scanning
* Fast database access
* Django based frontend
* Basic seaching via a SearchVector of author, title, & file_name fields.
* Ebook Downloading
* Collections

## Currently Supported Formats
* epub

## Installation Example
<a href="https://vimeo.com/382292764" target="_blank">pyShelf Installation Video</a>

## Further Installation & Support Information
* [SUPPORT.md](https://github.com/th3r00t/pyShelf/blob/development/.github/SUPPORT.md)

## 0.5.0 Patch Notes.

### Additional Dependencies
* gcc -- This will be installed by the new pre-installer script if its binary
is not detected at the arch distro default of /usr/bin/gcc

All other distros should install via their systems package manager prior to
running the installer.

### New Features
* Collections
We are now categorizing your ebooks into collections based on the folder
structure used to store them. Any folder after the root book folder is now
considered as a collection.
#### books/forgotten realms/ -> Forgotten Realms Collection.
#### books/Dune/Prelude To Dune -> Dune, & Preluse To Dune Collections.

In addition to the work on the collection system, a good deal of time was spent
on the installer, and the concept of having an installer in the first place.

I mainly wanted to make this project for Network Administrators, and other home
enthusiasts whom I assume will know how to setup a Django app, and a
Postgres server. Beyond that theres nothing the user has to do to make the
system work...

The installer will only run correctly on arch based distros. This could be
easily rectified to include other package managers, Members of the community
are welcome to dig into the installer source and patch in support
for other package managers.

There is some support for detection of the aptitude package manager
installation already present in the source now, however it is not complete and
should not be relied upon to be present in future releases unless completed by
a member of the community,

## Development

* [`pre-commit`](https://pre-commit.com/)
_Before developing, run `pre-commit install` See the [documentation](https://pre-commit.com/) for more information._

* ['Doxygen'](http://www.doxygen.nl/)
_Any changes to source should be documented and have run doxygen doxygen.conf prior to commiting._

* ['sem-ver'](https://semver.org)
_Before advancing version numbers be sure to set PROJECT_NUMBER in doxygen.conf accordingly._

## Configuration

All configuration is now handled by the installer.

Running via the Django test server might be possible, albeit not recomended.

### In Progress

#### Organizational tools.
- [x] Automated Collections
- [ ] Manual Collections
- [ ] Books Removal
- [ ] Access Restrictions
- [ ] Metadata Manipulation
- [ ] Others?
#### Improved cover image storage, and acquisition.
#### OPDS Support
#### Support for other formats
- [ ] .mobi
- [ ] .pdf
- [ ] .cbz
- [ ] .zip (Zipped book folders, is this a new idea? (Consider storing your library folders zipped and retrieving a book on demand))

### Future Goals
#### Terminal Backend for catalogue maintenance
#### Calculate page count from total characters
  * (Thanks to @Fireblend for the idea) https://github.com/th3r00t/pyShelf/issues/3
