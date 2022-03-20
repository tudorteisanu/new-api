#!/bin/bash
set -eo pipefail
cd /var/www/html && python3 app.py --perms
/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf

exit 0
