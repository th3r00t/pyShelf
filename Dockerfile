FROM archlinux:latest
RUN pacman -Syy
RUN pacman -Syu
RUN pacman -S python python-pip git
RUN mkdir -p /srv/Books && mkdir -p /srv/http && \
    chown -R http.http /srv/Books && chown -R http.http /srv/http
RUN systemctl enable sshd
VOLUME ['/srv/Books','/srv/http']
ENV nginx_conf /etc/nginx/nginx.conf
ENV PYTHONUNBUFFERED 1
WORKDIR /srv/http
RUN git clone https://github.com/th3r00t/pyShelf.git /srv/http && \
    pip install -r requirements.txt
EXPOSE 80 22 8000
