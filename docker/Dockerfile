# docker build -t ubuntu1604py36
FROM ubuntu:18.04

RUN apt-get update && apt-get install -y software-properties-common 
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update -y

RUN apt-get install -y build-essential python3.8 python3.8-dev python3-pip python3.8-venv && apt-get install -y git

# update pip
RUN python3 -m pip install wheel
RUN git clone https://github.com/hat/pyShelf.git /usr/src/app/
RUN python3 -m pip install -r /usr/src/app/requirements.txt
#CMD [""]
#RUN python3 manage.py migrate
#RUN python3 manage.py migrate interface
WORKDIR /usr/src/app/src/
CMD ["python3", "manage.py", "runserver"]
