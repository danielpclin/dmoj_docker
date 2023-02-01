FROM debian:bullseye-slim

RUN apt-get update && \
    apt-get install -y \
        inotify-tools curl && \
    rm -rf /var/lib/apt/lists/*

COPY .docker/watchdog/watchdog.sh /code/

WORKDIR /code

RUN chmod +x /code/watchdog.sh

ENTRYPOINT ./watchdog.sh
