[program:amazon_crawler_uwsgi]
# 确保uwsgi命令的路径是对的
command=/home/ubuntu/.pyenv/versions/3.6.0/envs/venv360/bin/uwsgi --ini /config/uwsgi.ini
directory=/home/ubuntu/myprojects/amazon_crawler
umask=022
# 以ripple用户运行
user=ubuntu
startsecs=0
stopwaitsecs=0
autostart=true
autorestart=true
# 注意确保路径存在
stdout_logfile=/var/log/uwsgi/amazon-crawler-uwsgi.stdout.log
stderr_logfile=/var/log/uwsgi/amazon-crawler-uwsgi.stderr.log
stopsignal=QUIT
killasgroup=true

[supervisord]

