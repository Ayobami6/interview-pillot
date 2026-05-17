import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.dependencies import get_question_service
from application.services.question_service import IQuestionService
from domain.models.question import InterviewQuestion
from unittest.mock import AsyncMock

# Mock Service
class MockQuestionService(IQuestionService):
    async def generate_interview_questions(self, role: str, count: int):
        return [
            InterviewQuestion(text="Mocked Question", category="General", difficulty="Medium")
        ]

@pytest.fixture
def client():
    # Override dependency
    app.dependency_overrides[get_question_service] = lambda: MockQuestionService()
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_generate_questions_endpoint(client):
    # Act
    response = client.post(
        "/api/v1/questions/generate",
        json={"role": "Manager", "count": 1}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Questions generated successfully"
    assert len(data["data"]) == 1
    assert data["data"][0]["text"] == "Mocked Question"
