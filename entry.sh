#!/bin/bash
sudo -u postgres pg_ctl -D /var/lib/postgres/data -l /srv/logs/pgsql.log start
sudo -u postgres psql -f create_db.sql
rm /srv/http/entry.sh
echo "sudo -u postgres pg_ctl -D /var/lib/postgres/data -l /srv/logs/lgsql.log start" > /srv/http/entry.sh
chmod +x /srv/http/entry.sh
