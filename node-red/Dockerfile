FROM nodered/node-red-docker:v8

USER root

RUN usermod -u 114 node-red && groupmod -g 118 node-red \
    && chown -R node-red:node-red /data \
    && chown -R node-red:node-red /usr/src/node-red

USER node-red

CMD ["npm", "start", "--", "--userDir", "/data"]
