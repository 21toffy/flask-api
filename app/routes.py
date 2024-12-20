# app/routes/question_routes.py
from flask import Blueprint, request, jsonify, current_app
from pydantic import ValidationError
from app.dal.question_dal import save_question_answer, get_all_questions
from app.services.openai_service import get_openai_answer
from app.schemas import (
    QuestionRequest, 
    QuestionResponse, 
    PaginationParams, 
    QuestionListResponse,
    ErrorResponse
)
from app.utils.validators import validate_request_json
from app.handlers import APIError
import logging
from typing import Dict, Any

question_blueprint = Blueprint('questions', __name__)



@question_blueprint.route('/api/v1/ask', methods=['POST'])
def ask_question():
    """
    Submit a question and get an AI-generated answer.
    ---
    post:
      summary: Ask a question
      requestBody:
        required: true
        content:
          application/json:
            schema: QuestionRequest
      responses:
        200:
          description: Success
          content:
            application/json:
              schema: QuestionResponse
        422:
          description: Validation Error
          content:
            application/json:
              schema: ErrorResponse
    """
    try:
        # Validate input
        request_data = validate_request_json(request.get_json() or {}, QuestionRequest)    
        if not request.json or 'question' not in request.json:
            return {'error': 'Validation Error', 'details': 'Question is required'}, 422 
        current_app.logger.info(f"Processing question request: {request_data.question[:50]}...")
        # Get answer from OpenAI
        answer = get_openai_answer(request_data.question)
        qa_record = save_question_answer(request_data.question, answer)
        if qa_record is None:
            return {'error': 'Processing Error', 'details': 'Failed to save to database'}, 500
        current_app.logger.info(f"Successfully processed question ID: {qa_record}")
        
        # Create and validate response
        response = QuestionResponse(
            id=qa_record.id,
            question=qa_record.question,
            answer=qa_record.answer,
            created_at=qa_record.created_at
        )
        
        return response.dict(), 200
    except ValidationError as ve:
        current_app.logger.error(f"Validation error in ask_question: {str(ve)}")
        return {"error": "Validation Error", "details": str(ve)}, 422
    except ValueError as ve:
        current_app.logger.error(f"Value error in ask_question: {str(ve)}")
        return {"error": "Processing Error", "details": str(ve)}, 500
    except Exception as e:
        current_app.logger.error(f"Unexpected error in ask_question: {str(e)}")
        return {"error": "Unexpected Error", "details": str(e)}, 500




@question_blueprint.route('/api/v1/questions', methods=['GET'])
def list_questions():
    """
    Get a paginated list of questions and answers.
    ---
    get:
      summary: List questions
      parameters:
        - in: query
          schema: PaginationParams
      responses:
        200:
          description: Success
          content:
            application/json:
              schema: QuestionListResponse
        422:
          description: Validation Error
          content:
            application/json:
              schema: ErrorResponse
    """
    try:
        # Validate pagination parameters
        params = validate_request_json(request.args, PaginationParams)
        
        current_app.logger.info(f"Fetching questions page {params.page}, per_page {params.per_page}")
        
        questions, total = get_all_questions(params.page, params.per_page)
        
        if not questions and params.page > 1:
            raise APIError("Page not found", status_code=404)
        
        # Create and validate response
        response = QuestionListResponse(
            questions=[
                QuestionResponse(
                    id=q.id,
                    question=q.question,
                    answer=q.answer,
                    created_at=q.created_at
                ) for q in questions
            ],
            total=total,
            page=params.page,
            per_page=params.per_page,
            total_pages=(total + params.per_page - 1) // params.per_page
        )
        
        current_app.logger.info(f"Successfully returned {len(questions)} questions")
        return response.model_dump(), 200  # Updated

    except ValidationError as ve:
        current_app.logger.error(f"Validation error in list_questions: {str(ve)}")
        return {"error": "Validation Error", "details": str(ve)}, 422
    except ValueError as ve:
        current_app.logger.error(f"Value error in list_questions: {str(ve)}")
        return {"error": "Processing Error", "details": str(ve)}, 404
    except Exception as e:
        current_app.logger.error(f"Unexpected error in list_questions: {str(e)}")
        return {"error": "Unexpected Error", "details": str(e)}, 500




# @question_blueprint.route('/api/v1/questions', methods=['GET'])
# def list_questions():
#     """
#     Get a paginated list of questions and answers.
#     ---
#     get:
#       summary: List questions
#       parameters:
#         - in: query
#           schema: PaginationParams
#       responses:
#         200:
#           description: Success
#           content:
#             application/json:
#               schema: QuestionListResponse
#         422:
#           description: Validation Error
#           content:
#             application/json:
#               schema: ErrorResponse
#     """
#     try:
#         # Validate pagination parameters
#         params = validate_request_json(request.args, PaginationParams)
        
#         current_app.logger.info(f"Fetching questions page {params.page}, per_page {params.per_page}")
        
#         questions, total = get_all_questions(params.page, params.per_page)
        
#         if not questions and params.page > 1:
#             raise APIError("Page not found", status_code=404)
        
#         # Create and validate response
#         response = QuestionListResponse(
#             questions=[
#                 QuestionResponse(
#                     id=q.id,
#                     question=q.question,
#                     answer=q.answer,
#                     created_at=q.created_at
#                 ) for q in questions
#             ],
#             total=total,
#             page=params.page,
#             per_page=params.per_page,
#             total_pages=(total + params.per_page - 1) // params.per_page
#         )
        
#         current_app.logger.info(f"Successfully returned {len(questions)} questions")
#         return response.dict()

#     except ValidationError as ve:
#         current_app.logger.error(f"Validation error in list_questions: {str(ve)}")
#         return {"error": "Validation Error", "details": str(ve)}, 422
#     except ValueError as ve:
#         current_app.logger.error(f"Value error in list_questions: {str(ve)}")
#         return {"error": "Processing Error", "details": str(ve)}, 404
#     except Exception as e:
#         current_app.logger.error(f"Unexpected error in list_questions: {str(e)}")
#         return {"error": "Unexpected Error", "details": str(e)}, 500