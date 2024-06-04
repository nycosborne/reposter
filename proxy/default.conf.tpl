server {
    listen ${LISTEN_PORT};

   root /usr/share/nginx/html;
   index index.html index.htm;

    location / {
            try_files $uri /index.html =404;
   }


    location /static {
        alias /vol/static;
    }

    location /api {
        uwsgi_pass              ${APP_HOST}:${APP_PORT};
        include                 /etc/nginx/uwsgi_params;
        client_max_body_size    10M;
    }

    location /admin {
        uwsgi_pass              ${APP_HOST}:${APP_PORT};
        include                 /etc/nginx/uwsgi_params;
        client_max_body_size    10M;
    }

}