#!/bin/bash
set -eo pipefail
cd /var/www/html && python3 permissions.py
/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf

exit 0
