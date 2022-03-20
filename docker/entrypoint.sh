#!/bin/bash
set -eo pipefail
/var/www/html/setup.sh
/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf

exit 0
