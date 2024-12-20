# Backend Internship Project

# Flask Backend with OpenAI Integration

## Requirements
- Docker & Docker Compose
- Python 3.10+

## Setup
1. Clone the repository:
    git clone <repo-url> cd backend-internship
2. Set up environment variables:
    cp .env.example .env
3. Build and run the containers:
    docker-compose up --build
4. Run tests:

## API
- **POST** `/ask`  
**Payload**: `{ "question": "Your question" }`  
**Response**: `{ "question": "...", "answer": "..." }`

## Deployment
- Use `gunicorn` and a reverse proxy like Nginx for production.
- Add CI/CD pipelines for automated testing and deployment.




# flask-api
