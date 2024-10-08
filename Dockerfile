FROM python:3.12-slim-bookworm
WORKDIR /notifier

COPY dualis_notifier.py config.py requirements.txt entrypoint.sh /notifier/
RUN chmod 0755 /notifier/entrypoint.sh

RUN pip install --no-cache-dir --compile -r requirements.txt

RUN apt update
# Upgrade all packages until a more minimal base image is used
RUN apt upgrade -y
RUN apt install cron -y

RUN echo "*/15 * * * * /usr/local/bin/python3 /notifier/dualis_notifier.py >> /var/log/cron.log 2>&1" | crontab -
CMD ["/notifier/entrypoint.sh"]
