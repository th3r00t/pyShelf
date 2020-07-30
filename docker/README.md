Use `docker-compose -f ./docker/docker-compose.yml up --build` in the project root to start both pyshelf and the database.

Use `docker build -t pyshelf -f ./docker/Dockerfile .` in the project root to build the pyshelf image.

Make sure the following files are in sync:
* config.json
* pyshelf_nginx.conf
* docker-compose.yml
* uwsgi.ini