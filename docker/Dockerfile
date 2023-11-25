
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
EXPOSE 1337

RUN apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential python3.12 python3.12-dev python3.12-pip python3.12-venv python3.12-hatch

COPY . /pyshelf
COPY ./docker/config.json /pyshelf/config.json

WORKDIR /pyshelf/
RUN python3.12 -m hatch shell

ENTRYPOINT python3.12 pyshelf.py
