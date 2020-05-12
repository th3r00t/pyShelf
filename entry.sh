#!/bin/bash
#sh /srv/http/database.sh
sudo -u postgres pg_ctl -D /var/lib/postgres/data -l /srv/logs/pgsql.log start &&
#gunicorn pyShelf.wsgi 8000:8000
