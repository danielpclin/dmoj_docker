FROM node:alpine

COPY dmoj /app/
COPY .docker/wsevent/config.js /app/websocket/

WORKDIR /app/

RUN npm install qu ws simplesets

EXPOSE 15100
EXPOSE 15101
EXPOSE 15102

ENTRYPOINT node /app/websocket/daemon.js
