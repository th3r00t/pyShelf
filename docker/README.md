Use `docker build -t pyshelf/pyshelf -f ./docker/Dockerfile .` in the project root to build the pyshelf image.

Make sure the following files are in sync:
* config.json
* docker/pyshelf_nginx.conf
* uwsgi.ini