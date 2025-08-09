# pyShelf 0.8.0

<p align="center"><b>Terminal based ebook server. Open source & Lightweight.</b></p>
<p align="center"><b><a href="https://discord.gg/H9TbNJS">Discord</a></b></p>
<p align="center">
	Having used Calibre for hosting my eBook collection in the 
	past, I found myself frustrated having to install X on my server, or manage my
	library externally, Thus I have decided to spin up my own.
</p>


### You dont need an X server to host a website, Movies or Tv, so why should you need one to host ebooks?

_Other solutions require you to have access to an X server to at the very least
generate your book database, pyShelf doesnt. We aim to provide a fully featured
ebook server with minimal requirements, and no reliance on X whatsoever._


## Features

* Recursive Scanning
* Cover Image Aggregation
* Fuzzy Search with optional specifiers
	- tag:fiction
	- author:Clancy
	- title:"The Hunt for Red October"
	- The Expanse
* Download System
* Automated Collections based on folder structure

## Currently Supported Formats

* epub
* mobi
* pdf

# Installation
curl -fsSL https://raw.githubusercontent.com/th3r00t/pyShelf/refs/heads/0.8.0--dev-zipapp/install.sh | sudo bash
pyShelf is installed as a systemd service and is enabled by default, you can control it with the following commands:
```bash`
systemctl start pyShelf
systemctl restart pyshelf
systemctl stop pyshelf
systemctl disable pyshelf
systemctl enable pyshelf
````
* if your books are not in the default location (/mnt/books) edit the config file at /etc/pyShelf/config.json

# Coming Soon
- [ ] Manual Collections
- [ ] Books Removal
- [ ] Access Restrictions
- [ ] Metadata Manipulation
- [ ] UiUx Improvements
- [ ] Expanded book information view
- [ ] Improved Cover Image System
- [ ] OPDS Support

## Development

* [`pre-commit`](https://pre-commit.com/)
_Before developing, run `pre-commit install` See the [documentation](https://pre-commit.com/) for more information._
* ['sem-ver'](https://semver.org)
_Before advancing version numbers be sure to set PROJECT_NUMBER in doxygen.conf accordingly._

| Branch | Support | Feature set |
| --- | --- | --- |
| <b>Master<b> | Bugs get priority | Most stable branch, may be behind in the core feature set |
 | <b>Development</b>| Please report all bugs | Most active branch, this branch is a rolling release, containing the latest features. There will be bugs here hopefully nothing service killing |
 | <b>Others</b> | Here there be dragons | These branches are used for day to day development, nothing here should be considered stable.
