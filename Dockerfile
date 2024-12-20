FROM python:3.10-slim

WORKDIR /app


COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP="app:create_app()"
ENV FLASK_ENV=development


EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
