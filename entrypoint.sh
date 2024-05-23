#!/bin/bash

set -ex

echo -e "127.0.0.1\tredis" >> /etc/hosts
echo -e "::1\tredis" >> /etc/hosts


/usr/bin/supervisord -c /etc/supervisor/supervisord.conf -n

