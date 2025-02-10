#!/bin/sh

# Substitute environment variables in nginx.conf.template and save as nginx.conf
envsubst '$BACKEND_SERVICE_HOST $BACKEND_SERVICE_PORT' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Validate Nginx configuration
nginx -t || exit 1

# Start Nginx in the foreground
exec nginx -g "daemon off;"
