#!/bin/bash
set -eo pipefail
/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf

exit 0
