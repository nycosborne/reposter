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

    # Serve JavaScript files with the correct MIME type
    location ~* \.js$ {
        add_header Content-Type application/javascript;
    }

    # Serve CSS files with the correct MIME type
    location ~* \.css$ {
        add_header Content-Type text/css;
    }

    # Serve SVG files with the correct MIME type
    location ~* \.svg$ {
        add_header Content-Type image/svg+xml;
    }

    # Enable gzip compression for text-based resources
    gzip on;
    gzip_types text/plain application/javascript text/css application/json application/xml text/xml;
    gzip_proxied any;
    gzip_min_length 1000;

}


