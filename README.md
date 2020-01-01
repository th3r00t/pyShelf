# pyShelf 0.4.0

<p align="center"><b>Terminal based ebook server. Open source & Lightweight.</b></p>

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/D1D51ALZH)

Having used Calibre for hosting my eBook collection in the past, I found myself frustrated having to install X on my server, or manage my library externally, Thus I have decided to spin up my own.

## Current Features
* Custom Installer
* Recursive Scanning
* Fast database access
* Django based frontend
* Basic seaching via a SearchVector of author, title, & file_name fields.
* Ebook Downloading

## Currently Supported Formats
* epub

## Installation Example
<a href="https://vimeo.com/382292764" target="_blank">pyShelf Installation Video</a>

## Further Installation & Support Information
* [SUPPORT.md](https://github.com/th3r00t/pyShelf/blob/development/.github/SUPPORT.md)

## 0.4.0 Patch Notes.
### The Installer Initiative

All work this time around was centered on creating an installer simple and inclusive enough to hopefully enable all
users to simply set it and forget it. I have debugged as much as I can with my setup. I am performing some simple file finding to determine which system installer is present, and setting it as the installer used by pyShelf.

This setup has been tested and is working flawlessly on arch based distros, and i have done what I can for debian, and centos based distros, If you do encounter installer issues please let me know if it isnt finding the system installer, or possibly isnt passing command line arguments to your installer.

Also it should be noted that I am determining the presence of your postgresql, and nginx servers based on whether or not the
process is listed in the process list.

At this time I would suggest stopping both your postgresql and nginx servers should you already have them and allowing the installer to do its work generating custom configurations and putting the nginx config files in place (/etc/nginx/sites-available, and symlinked to /etc/nginx/sites-enabled/) None of your existing configurations will be overwritten.

## 0.3.0 Patch Notes.
### "And now we search."

Just about all the changes in this release were in some way related to implementing the search features.
There is one new requirement
* Requirement: **PostgreSQL**
*This is what I believe to be the last infrastructure requirement, users with larger libraries should notice an increase in access speed.*
* Feature: **Searching**
*The search feature is now implemented. In its current incarnation you will by default search the author, title, & file_name fields. More defined search options will be available in future releases. Searches are paginated @ 20 results per page.*
* Discord [https://discord.gg/H9TbNJS](https://discord.gg/H9TbNJS)
* IRC find us on freenode.net @ #pyshelf

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

## In Progress

* Organizational tools.
* Docker image for those who need it.
* Improved cover image storage, and acquisition.

## Future Goals
* Support for other book formats (Currently only supporting EPUBS)
* Terminal Backend for catalogue maintenance
* Calculate page count from total characters
  * (Thanks to @Fireblend for the idea) https://github.com/th3r00t/pyShelf/issues/3
* Reader for easy integration with your catalogue
