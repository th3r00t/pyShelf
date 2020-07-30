FROM ubuntu

EXPOSE 8000

RUN apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential python3 python3-dev python3-pip python3-venv nginx-full

COPY . /pyshelf

WORKDIR /pyshelf/
RUN python3 -m pip install -r requirements.txt

COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./pyshelf_nginx.conf /etc/nginx/sites-available/pyshelf_nginx.conf
RUN ln -s /etc/nginx/sites-available/pyshelf_nginx.conf /etc/nginx/sites-enabled/

WORKDIR /pyshelf/
ENTRYPOINT cd src/ \
            && python3 manage.py makemigrations \
            && python3 manage.py makemigrations interface \
            && python3 manage.py migrate \
            && python3 manage.py migrate interface \
            && cd .. \
            && python3 importBooks \
            && python3 makeCollections \
            && nginx -g "daemon on;" \
            && uwsgi --ini uwsgi.ini