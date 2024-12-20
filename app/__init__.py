
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_openapi3 import OpenAPI
from flask_swagger_ui import get_swaggerui_blueprint
import os

import logging


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__, static_url_path='/static')  # Ensure static URL path is set correctly

    app.config.from_object("app.config.Config")
    
    db.init_app(app)
    migrate.init_app(app, db)

    # Register routes
    from app.routes import question_blueprint as routes_bp
    app.register_blueprint(routes_bp)

    # Configure Swagger UI
    SWAGGER_URL = '/api/docs'  # URL for the Swagger UI
    API_URL = '/static/swagger.json'

    # Setting up Swagger UI
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Test Application"
        },
    )
    app.register_blueprint(swaggerui_blueprint)
    app.config['DEBUG'] = True
    app.config['ENV'] = 'development'


    return app


# Create application instance
application = create_app()
app = application

# If you want to run the app directly
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)

