ENV=${NGINX_ENV:-development}

if [ "$ENV" = "production" ]; then
    # Wait for Nginx to start
    while ! curl -s localhost:443 > /dev/null; do
        echo "Waiting for Nginx to start..."
        sleep 1
    done

    echo "Nginx started successfully."

    apt-get update
    apt-get install certbot python3-certbot-nginx

    certbot --nginx -d ${DOMAIN} \
    --email ${CERT_EMAIL} --agree-tos --no-eff-email \
    --keep-until-expiring --non-interactive

    nginx -s reload
fi