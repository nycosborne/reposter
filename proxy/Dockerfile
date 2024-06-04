# Use an official Node.js runtime as the base image
FROM node:alpine as build

# Set the working directory in the Docker image to /app
WORKDIR /app

# Copy package.json and package-lock.json into the image
#COPY ./reposter-backend/package.json .
#COPY ./reposter-backend/package-lock.json .


# Install the application's dependencies inside the Docker image

# Copy the rest of the application code into the image
COPY ./reposter-react .

RUN npm install

# Build the React application
RUN npm run build


FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="nycosborne.com"

# Copy the build output to the Nginx HTML directory
COPY --from=build /app/dist /usr/share/nginx/html

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
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

VOLUME /vol/static

USER nginx

CMD ["/run.sh"]