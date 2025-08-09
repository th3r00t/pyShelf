# pyShelf 0.8.0

<p align="center"><b>Terminal based ebook server. Open source & Lightweight.</b></p>
<p align="center">Having used Calibre for hosting my eBook collection in the past, I found myself frustrated having to install X on my server, or manage my library externally, Thus I have decided to spin up my own.</p>


![pyShelf 0.6.0 newui](https://github.com/th3r00t/pyShelf/raw/master/src/interface/static/img/pyShelf_frontend_0_2_0.png)

### You dont need an X server to host a website, or your Movie & Tv collection, so why should you need one to host ebooks?

_Other solutions require you to have access to an X server to at the very least generate your book database, pyShelf doesnt. We aim to provide a fully featured ebook server with minimal requirements, and no reliance on X whatsoever._

Follow or influence development @ <p align="center"><b>
    <a href="https://discord.gg/H9TbNJS">Discord</a>
</b></p>

## 0.8.0 Patch Notes.

## Features

* Recursive Scanning
* Fuzzy Search with optional specifiers
	- tag:fiction
	- author:Clancy
	- title:"The Hunt for Red October"
	- The Expanse
* Download System
* Automated Collections based on folder structure
* Expanded book information view

| Branch | Support | Feature set |
| --- | --- | --- |
| <b>Master<b> | Bugs get priority | Most stable branch, may be behind in the core feature set |
 | <b>Development</b>| Please report all bugs | Most active branch, this branch is a rolling release, containing the latest features. There will be bugs here hopefully nothing service killing |
 | <b>Others</b> | Here there be dragons | These branches are used for day to day development, nothing here should be considered stable.

## Currently Supported Formats

* epub
* mobi
* pdf

## Installation & Support Information

# Installation
	- curl -fsSL https://raw.githubusercontent.com/th3r00t/pyShelf/refs/heads/0.8.0--dev-zipapp/install.sh | sudo bash


## In Progress

### Organizational tools.

- [x] Automated Collections $id{29fda2fe-4134-4905-8682-aab074acfdb2}
- [ ] Manual Collections $id{c541949c-2e21-46c9-8089-a62fb6d043f6}
- [ ] Books Removal $id{6b577a16-ac19-4f95-bf84-47938d966adf}
- [ ] Access Restrictions $id{b6cf99a7-700b-46dd-9e75-5bc9fc7c4981}
- [ ] Metadata Manipulation $id{35652d34-5d76-4496-92e5-67617a3226ad}
- [ ] UiUx Improvements $id{9dd7c416-8919-40ed-a9a5-9503ad737e97}
- [ ] Others? $id{da6e44b4-312f-43b2-883d-3355a70464e8}

### Improved cover image storage, and acquisition.

### OPDS Support


## Development

* [`pre-commit`](https://pre-commit.com/)
_Before developing, run `pre-commit install` See the [documentation](https://pre-commit.com/) for more information._
* ['sem-ver'](https://semver.org)
_Before advancing version numbers be sure to set PROJECT_NUMBER in doxygen.conf accordingly._
