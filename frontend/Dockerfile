# Use official Nginx base image
FROM nginx:alpine

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create the necessary directory inside the default Nginx web root
RUN mkdir -p /usr/share/nginx/html/kasturihealthcare

# Copy HTML, CSS, and other static files
COPY index.html appointments.html styles.css /usr/share/nginx/html/kasturihealthcare/

# Copy additional assets if needed
COPY kasturihealthcare /usr/share/nginx/html/kasturihealthcare/

# Set correct permissions
RUN chmod -R 755 /usr/share/nginx/html/kasturihealthcare/

# Expose port 80 for web traffic
EXPOSE 80

# Validate Nginx configuration before starting
RUN nginx -t

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
