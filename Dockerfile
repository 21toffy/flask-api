FROM python:3.10-slim

WORKDIR /app

# Install postgresql-client
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Make the entrypoint script executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP="app:create_app()"
ENV FLASK_ENV=development

CMD ["/entrypoint.sh"]