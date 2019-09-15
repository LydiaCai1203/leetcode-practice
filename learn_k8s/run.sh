#!/bin/bash
# supervisord服务端启动
supervisord -c /etc/supervisor/supervisord.conf
# 要有这句话 将服务挂住才行
tail -f /project/run.sh
# cd /project && celery -A celery_tasks worker -l info
