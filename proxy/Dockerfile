#FROM node:17-alpine as build
#WORKDIR /app
#COPY ./reposter-react/package.json .
#RUN npm i
#COPY ./reposter-react .
#RUN npm run build




FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="nycosborne.com"
#COPY --from=build ./reposter-react/dist /usr/share/nginx/html
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