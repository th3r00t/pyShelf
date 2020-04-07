#!/bin/bash
sh -c sudo -u postgres pg_ctl -D /var/lib/postgres/data -l /srv/logs/pgsql.log start
sh -c sudo -u postgres psql -f create_db.sql
rm /srv/http/database.sh
echo "sudo -u postgres pg_ctl -D /var/lib/postgres/data -l /srv/logs/lgsql.log start" > /srv/http/database.sh
chmod +x /srv/http/database.sh
