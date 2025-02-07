# Use a minimal Python image
FROM python:3.9-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency file first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the Flask default port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
