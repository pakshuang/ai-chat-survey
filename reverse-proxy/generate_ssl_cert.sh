ENV=${NGINX_ENV:-development}

if [ "$ENV" = "production" ]; then
    # Wait for Nginx to start
    while ! nc -z localhost 443; do
        echo "Waiting for Nginx to start..."
        sleep 1
    done

    echo "Nginx started successfully."

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