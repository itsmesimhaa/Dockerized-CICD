# Use official Nginx base image
FROM nginx:alpine

# Install envsubst for variable substitution
RUN apk add --no-cache gettext

# Copy custom Nginx configuration template
COPY nginx.conf.template /etc/nginx/nginx.conf.template

# Create necessary directory for static files
RUN mkdir -p /usr/share/nginx/html/kasturihealthcare

# Copy static files
COPY index.html appointments.html styles.css /usr/share/nginx/html/kasturihealthcare/
COPY kasturihealthcare /usr/share/nginx/html/kasturihealthcare/

# Set correct permissions
RUN chmod -R 755 /usr/share/nginx/html/kasturihealthcare/

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port 80
EXPOSE 80

# Use entrypoint script to substitute environment variables and start Nginx
ENTRYPOINT ["/entrypoint.sh"]
