#!/bin/bash
ENV=${NGINX_ENV:-development}

if [ "$ENV" = "production" ]; then
    apt-get update
    apt-get install -y software-properties-common
    add-apt-repository ppa:certbot/certbot
    apt-get update
    apt-get install -y nginx certbot python3-certbot-nginx
    certbot --nginx -d ${DOMAIN} \
    --email ${CERT_EMAIL} --agree-tos --no-eff-email \
    --keep-until-expiring --non-interactive
    SSL="ssl"
    SSL_CERTIFICATE="ssl_certificate /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;"
    SSL_CERTIFICATE_KEY="ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem;"
else
    SSL=""
    SSL_CERTIFICATE=""
    SSL_CERTIFICATE_KEY=""
fi

envsubst '${FRONTEND_CONTAINER_PORT} ${BACKEND_CONTAINER_PORT} ${NGINX_CONTAINER_PORT} ${SSL} ${SSL_CERTIFICATE} ${SSL_CERTIFICATE_KEY}' < /etc/nginx/conf.d/nginx.conf.template > /etc/nginx/conf.d/default.conf