#!/bin/bash
sudo -u postgres pg_ctl -D /var/lib/postgres/data -l /srv/logs/pgsql.log start &&
sudo -u postgres psql -f create_db.sql &&
rm /srv/http/database.sh &&
echo "sudo -u postgres pg_ctl -D /var/lib/postgres/data -l /srv/logs/lgsql.log start" > /srv/http/database.sh &&
chmod +x /srv/http/database.sh &&
cd src && \
    python manage.py makemigrations && \
    python manage.py makemigrations interface && \
    python manage.py migrate && \
    python manage.py migrate interface && \
cd ..
echo "pyShelf Env Started"
