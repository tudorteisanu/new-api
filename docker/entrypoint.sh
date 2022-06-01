#!/bin/bash
set -eo pipefail
cd /var/www/html && python3 server.py --perms
cd /var/www/html && python3 flask db upgrade
/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf

exit 0
