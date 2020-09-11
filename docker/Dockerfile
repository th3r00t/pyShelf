
# This file is used to build the Dockerhub image. To host pyShelf yourself for 
# production, please use the official pyShelf image on 
# https://hub.docker.com/r/pyshelf/pyshelf

# Use the following commands to build and push the docker image to Dockerhub:
#
#   docker build -t pyshelf/pyshelf -f ./docker/Dockerfile .
#   docker login
#   docker push pyshelf/pyshelf

FROM ubuntu

EXPOSE 8000

RUN apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential python3 python3-dev python3-pip python3-venv nginx-full

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y cron
RUN echo "* * * * * cd /pyshelf/ && python3 importBooks >> /var/log/cron.log 2>&1" > import_books_scheduler.cron && crontab import_books_scheduler.cron

COPY ./docker/pyshelf_nginx.conf /etc/nginx/sites-available/pyshelf_nginx.conf
RUN ln -s /etc/nginx/sites-available/pyshelf_nginx.conf /etc/nginx/sites-enabled/

COPY . /pyshelf
COPY ./docker/config.json /pyshelf/config.json

WORKDIR /pyshelf/
RUN python3 -m pip install -r requirements.txt

WORKDIR /pyshelf/
ENTRYPOINT cron start \
            && python3 configure \
            # && python3 importBooks \
            && nginx -g "daemon on;" \
            && uwsgi --ini uwsgi.ini
