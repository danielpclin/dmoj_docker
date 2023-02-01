FROM danielpclin/dmoj-base:latest

COPY --chown=dmoj:dmoj .docker/uwsgi/uwsgi.ini /site/

EXPOSE 8000

ENTRYPOINT uwsgi --ini uwsgi.ini
