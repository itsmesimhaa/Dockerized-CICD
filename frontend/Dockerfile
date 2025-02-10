# Use official Nginx base image
FROM nginx:alpine

# Create necessary directory for static files
RUN mkdir -p /usr/share/nginx/html/kasturihealthcare

# Copy static files
COPY index.html appointments.html styles.css /usr/share/nginx/html/kasturihealthcare/
COPY kasturihealthcare /usr/share/nginx/html/kasturihealthcare/

# Set correct permissions
RUN chmod -R 755 /usr/share/nginx/html/kasturihealthcare/

# Expose port 80
EXPOSE 80

# Remove nginx.conf from the image, since it's now provided via ConfigMap
RUN rm /etc/nginx/nginx.conf

# Start Nginx
CMD ["sh", "-c", "while [ ! -f /etc/nginx/nginx.conf ]; do echo 'Waiting for config...'; sleep 2; done; nginx -g 'daemon off;'"]

