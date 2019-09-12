#!/bin/bash
# supervisord服务端启动
supervisord -c /etc/supervisor/supervisord.conf
tail -f /project/run.sh
# cd /project && celery -A celery_tasks worker -l info
