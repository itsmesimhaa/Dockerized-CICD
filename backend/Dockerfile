# Use a minimal Python image
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Copy application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask default port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
