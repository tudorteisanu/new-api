#!/bin/bash
set -eo pipefail

/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
su-exec nginx:nginx supervisorctl start flask

exit 0
