FROM archlinux:latest
RUN pacman -Syy
RUN pacman -Syu --noconfirm
RUN pacman -S --noconfirm python python-pip git openssh postgresql sudo base-devel
RUN sudo -u postgres initdb --locale=en_US.UTF-8 -E UTF8 -D /var/lib/postgres/data
RUN useradd pyshelf && chpasswd pyshelf:pyshelf
RUN mkdir -p /srv/Books && \
    mkdir -p /srv/http && \
    mkdir -p /srv/logs/ && \
    mkdir -p /run/postgresql && \
    touch /srv/logs/pgsql.log && \
    chown postgres.postgres /run/postgresql && \
    chown http.pyshelf /srv/Books && \
    chown http.pyshelf /srv/http && \
    chown postgres.postgres /srv/logs/pgsql.log
ENV PYTHONUNBUFFERED=1
VOLUME ['/srv/Books','/srv/http','/srv/logs']
WORKDIR /srv/http
RUN git clone https://github.com/th3r00t/pyShelf.git /srv/http && \
    git checkout 0.5.0--docker && pip install -r requirements.txt
# RUN sudo -u postgres pg_ctl -D /var/lib/postgres/data -l /srv/logs/pgsql.log start
# RUN sudo -u postgres psql -f create_db.sql
# RUN gunicorn pyShelf.wsgi 8000:8000
EXPOSE 80 22 8000
CMD ["sh", "-c","/srv/http/entry.sh"]
