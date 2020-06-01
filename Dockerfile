FROM archlinux:latest
RUN pacman -Syy
RUN pacman -Syu --noconfirm
RUN pacman -S --noconfirm python python-pip git postgresql sudo gcc
RUN sudo -u postgres initdb --locale=en_US.UTF-8 -E UTF8 -D /var/lib/postgres/data
RUN useradd pyshelf && chpasswd pyshelf:pyshelf
#RUN mkdir -p /srv/Books && mkdir -p /srv/http && mkdir -p /srv/logs/ && mkdir -p /run/postgresql && \
#    touch /srv/logs/pgsql.log && chown postgres.postgres /run/postgresql && \
#    chown http.pyshelf /srv/Books && chown http.pyshelf /srv/http && chown postgres.postgres /srv/logs/pgsql.log
VOLUME /srv/Books ./Books
VOLUME /srv/http .
VOLUME /srv/logs ./logs
VOLUME /var/lib/postgres/data ./pgdata
RUN sudo -u postgres pg_ctl -D /var/lib/postgres/data -l /srv/logs/pgsql.log start
RUN sudo -u postgres psql -f create_db.sql
ENV PYTHONUNBUFFERED=1
WORKDIR /srv/http
RUN pip install -r requirements.txt
EXPOSE 80 8000
CMD ["sh", "-c","/srv/http/entry.sh"]
