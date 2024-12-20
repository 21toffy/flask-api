# app/models/schemas.py
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import List, Optional

class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        description="The question to be answered",
        example="What is the capital of France?"
    )

    @field_validator('question')
    def validate_question(cls, v):
        if not 1 <= len(v) <= 1000:
            raise ValueError('Question must be between 1 and 1000 characters')
        return v

class QuestionResponse(BaseModel):
    id: int = Field(..., description="Unique identifier of the question")
    question: str = Field(..., description="The question that was asked")
    answer: str = Field(..., description="The AI-generated answer")
    created_at: datetime = Field(..., description="When the QA pair was created")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class PaginationParams(BaseModel):
    page: int = Field(default=1, description="Page number")
    per_page: int = Field(default=10, description="Items per page")

    @field_validator('page')
    def validate_page(cls, v):
        if v < 1:
            raise ValueError('Page must be greater than 0')
        return v

    @field_validator('per_page')
    def validate_per_page(cls, v):
        if not 1 <= v <= 100:
            raise ValueError('Items per page must be between 1 and 100')
        return v

class QuestionListResponse(BaseModel):
    questions: List[QuestionResponse] = Field(..., description="List of questions and answers")
    total: int = Field(..., description="Total number of records")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    details: Optional[dict] = Field(None, description="Additional error details")
    status_code: int = Field(..., description="HTTP status code")
    
# # app/docs/api_docs.py
# from flask import Blueprint
# from flask_swagger import swagger
# from flask_swagger_ui import get_swaggerui_blueprint
# from app.schemas import (
#     QuestionRequest,
#     QuestionResponse,
#     PaginationParams,
#     QuestionListResponse,
#     ErrorResponse
# )

# docs_blueprint = Blueprint('', __name__)

# def create_swagger_spec(app):
#     """Create Swagger specification using Pydantic models"""
#     swag = swagger(app)
    
#     # Basic API info
#     swag['info'] = {
#         'version': "1.0",
#         'title': "Question Answer API",
#         'description': "API for submitting questions and retrieving answers"
#     }
    
#     # Add schemas from Pydantic models
#     swag['components'] = {
#         'schemas': {
#             'QuestionRequest': QuestionRequest.schema(),
#             'QuestionResponse': QuestionResponse.schema(),
#             'PaginationParams': PaginationParams.schema(),
#             'QuestionListResponse': QuestionListResponse.schema(),
#             'ErrorResponse': ErrorResponse.schema()
#         }
#     }
    
#     return swag

# def setup_swagger(app):
#     """Configure Swagger documentation"""
#     SWAGGER_URL = '/api/docs'
#     API_URL = '/api/swagger.json'
    
#     swaggerui_blueprint = get_swaggerui_blueprint(
#         SWAGGER_URL,
#         API_URL,
#         config={
#             'app_name': "Question Answer API",
#             'validatorUrl': None
#         }
#     )
    
#     app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
#     app.register_blueprint(docs_blueprint)
    
#     @docs_blueprint.route("/api/swagger.json")
#     def get_swagger_spec():
#         return create_swagger_spec(app)