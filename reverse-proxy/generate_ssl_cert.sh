# if [ "${NGINX_ENV}" = "production" ]; then
# Wait for Nginx to start
while ! curl -s localhost:${NGINX_CONTAINER_PORT} > /dev/null; do
    echo "Waiting for Nginx to start..."
    sleep 1
done

echo "Nginx started successfully."

apt-get update
apt-get install -y certbot python3-certbot-nginx

certbot --nginx -d ${DOMAIN} \
--email ${CERT_EMAIL} --agree-tos --no-eff-email \
--keep-until-expiring --non-interactive

nginx -s reload
# fi