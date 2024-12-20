# Flask backend API

## About the Project

This project implements a robust question-answer system leveraging Flask, OpenAI, and PostgreSQL. The system is designed to receive user-submitted questions, process them using the OpenAI API, and store the question-answer pairs in a PostgreSQL database. The application is containerized using Docker and deployed to AWS ECS for scalable and reliable operation.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Environment Configuration](#environment-configuration)
3. [Running the Project Locally](#running-the-project-locally)
4. [Database Migrations](#database-migrations)
5. [OpenAPI Documentation](#openapi-documentation)
6. [Running Tests](#running-tests)
7. [Deployment to ECS](#deployment-to-ecs)
8. [Screenshots](#screenshots)

---

## Getting Started

To get a local copy of the project up and running, follow these steps.

### Prerequisites

- Docker
- Docker Compose
- Python 3.x (if not using Docker for the Python environment)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/21toffy/flask-api
    cd flask-api
    ```

2. Set up the environment variables:
    - Create a `.env` file in the root of the project and configure the following variables:

    ```env
    POSTGRES_USER=your_db_user
    POSTGRES_PASSWORD=your_db_password
    POSTGRES_DB=your_db_name
    SECRET_KEY=your_secret_key
    OPENAI_API_KEY=your_openai_api_key
    DATABASE_URL=postgresql://your_db_user:your_db_password@localhost:5435/your_db_name
    ```

3. Build and run the project with Docker Compose:
    ```bash
    docker-compose up --build
    ```

    This will start the web application and PostgreSQL database.

---

## Database Migrations

### Initial Migration

1. Ensure your application is running and the database is accessible via Docker.

2. Run the migrations with the following command:

```docker-compose exec web flask db upgrade```

### Creating New Migrations
If you need to create a new migration, use the following command:

```
docker-compose exec web flask db migrate -m "Migration message"
```

### After creating the migration, apply it using:

```docker-compose exec web flask db upgrade```


## Running the Project Locally / OpenAPI Documentation

### The OpenAPI documentation for the project is available at:

Once the Docker containers are up and running, you can access the application on the following URL:

- documentation [http://localhost:5001/api/docs](http://localhost:5001/api/docs)

This provides an interactive interface for exploring and testing the API endpoints.

## Running Tests

### To run the tests for the project, use the following command:

```docker-compose exec web pytest```

This will run the tests defined in your test files.



To stop the services, use:
```bash
docker-compose down
