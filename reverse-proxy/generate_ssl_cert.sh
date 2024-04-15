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
    nginx -s reload
fi