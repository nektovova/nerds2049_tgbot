# Channel Reposter V2

### Supervisor conf

```
[program:channel-reposter-v2-telegram-bot]
command=/usr/bin/python3 /root/channel-reposter-v2/tg_bot.py
stdout_logfile=/root/channel-reposter-v2/tg_bot.log
stderr_logfile=/root/channel-reposter-v2/tg_bot_log.log
user=root
autostart=true
autorestart=true
numprocs=1
```
