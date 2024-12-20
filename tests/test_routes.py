# tests/test_routes.py
import pytest
from unittest.mock import patch, MagicMock
from tests.factories import QuestionAnswerFactory
from app import create_app, db

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["OPENAI_API_KEY"] = "test-key"
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
        
    # Cleanup
    # with app.app_context():
    #     db.drop_all()




def test_ask_endpoint_success(client, mocker):
    """Test the /ask endpoint for a successful response."""
    # Create a mock OpenAI response structure
    mock_message = MagicMock()
    mock_message.content = "Mocked Answer"
    
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    
    # Mock the OpenAI client
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response
    
    # Mock the OpenAI client initialization
    mocker.patch('app.services.openai_service.OpenAI', return_value=mock_client)
    
    response = client.post('/api/v1/ask', json={'question': 'What is Flask?'})
    
    assert response.status_code == 200
    data = response.get_json()
    print(data)
    assert data['question'] == 'What is Flask?'
    assert data['answer'] == 'Mocked Answer'
    

def test_ask_endpoint_validation_error(client):
    """Test the /ask endpoint with missing question."""
    response = client.post('/api/v1/ask', json={})
    
    assert response.status_code == 500
    data = response.get_json()
    assert 'error' in data
    assert 'Unexpected Error' in data['error']

def test_ask_endpoint_openai_error(client, mocker):
    """Test the /ask endpoint when OpenAI service fails."""
    # Mock OpenAI to raise an exception
    mocker.patch(
        'app.services.openai_service.OpenAI',
        side_effect=Exception("OpenAI service error")
    )
    
    response = client.post('/api/v1/ask', json={'question': 'What is Flask?'})
    
    assert response.status_code == 500
    data = response.get_json()
    assert 'error' in data
    assert 'OpenAI service error' in str(data['details'])

def test_ask_endpoint_db(client, mocker):
    """Test the /ask endpoint when database save ."""
    # Mock OpenAI response
    mock_message = MagicMock()
    mock_message.content = "Mocked Answer"
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response
    mocker.patch('app.services.openai_service.OpenAI', return_value=mock_client)
    
    # Mock database save to fail
    mocker.patch(
        'app.dal.question_dal.save_question_answer',
        return_value=None
    )
    
    response = client.post('/api/v1/ask', json={'question': 'What is Flask?'})
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'error' not in data
    


# def test_list_questions_success(client):
#     """Test the /questions endpoint for successful response."""
#     # Use the factory to create mock data
#     with client.application.app_context():
#         QuestionAnswerFactory.create_batch(3)
    
#     response = client.get('/api/v1/questions?page=1&per_page=2')
#     assert response.status_code == 200
#     data = response.get_json()
#     print(data)
#     assert data['total'] == 3
#     assert len(data['questions']) == 2
#     assert "question" in data['questions'][0]
#     assert "answer" in data['questions'][0]
    