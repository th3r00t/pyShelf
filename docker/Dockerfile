
# This file is used to build the Dockerhub image. To host pyShelf yourself for
# production, please use the official pyShelf image on
# https://hub.docker.com/r/pyshelf/pyshelf

# Use the following commands to build and push the docker image to Dockerhub:
#
#   docker build -t pyshelf/pyshelf -f ./docker/Dockerfile .
#   docker login
#   docker push pyshelf/pyshelf

FROM python:3

EXPOSE 8000
EXPOSE 1337

# RUN apt-get update -y
# RUN DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential python312 python312-dev python312-pip python312-venv python312-hatch

COPY . /pyshelf
COPY ./docker/config.json /pyshelf/config.json
COPY ./docker/requirements.txt /pyshelf/requirements.txt
WORKDIR /pyshelf/
RUN python -m pip install --no-cache-dir -r requirements.txt
ENTRYPOINT hatch run ./pyShelf.py
