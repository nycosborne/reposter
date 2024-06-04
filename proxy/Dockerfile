## Use an official Node.js runtime as the base image
#FROM node:16-alpine AS build
#
## Set the working directory in the Docker image to /app
#WORKDIR /apps/reposter-react
#
## Copy package.json and package-lock.json into the image
#COPY ./reposter-react .
#
## Install the application's dependencies inside the Docker image
#RUN npm install
#
## Copy the rest of the application code into the image
## Expose port 3000 in the Docker image
##EXPOSE 3000
#RUN npm run build
## Define the command that should be executed when the Docker image is run
##CMD [ "npm", "run", "build" ]


FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="nycosborne.com"

COPY ./reposter-react/dist /usr/share/nginx/html

COPY ./proxy/default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./proxy/uwsgi_params /etc/nginx/uwsgi_params
COPY ./proxy/run.sh /run.sh

ENV LISTEN_PORT=8000
# TODO: Change this to frontend
ENV APP_HOST=app
ENV APP_PORT=9000

USER root

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /usr/share/nginx/html && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

VOLUME /vol/static

USER nginx

CMD ["/run.sh"]