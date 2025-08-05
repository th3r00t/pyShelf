
# This file is used to build the Dockerhub image. To host pyShelf yourself for
# production, please use the official pyShelf image on
# https://hub.docker.com/r/pyshelf/pyshelf

# Use the following commands to build and push the docker image to Dockerhub:
#
#   docker build -t pyshelf/pyshelf -f ./docker/Dockerfile .
#   docker login
#   docker push pyshelf/pyshelf

FROM ubuntu:latest

EXPOSE 8080
EXPOSE 1337

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev \
libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget \
libbz2-dev curl -y
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
RUN export NVM_DIR="$HOME/.nvm" ; \
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" ; nvm install 14 npm
WORKDIR /tmp
RUN wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz
RUN tar -xf Python-3.12.0.tgz
WORKDIR /tmp/Python-3.12.0/
RUN ./configure --enable-optimizations
RUN make -j 4
RUN make install

COPY . /pyshelf
COPY ./docker/config.json /pyshelf/config.json
COPY ./docker/requirements.txt /pyshelf/requirements.txt
WORKDIR /pyshelf/
RUN python3 -m pip install --no-cache-dir -r requirements.txt
ENTRYPOINT hatch run ./pyShelf.py
