import pytest
from unittest.mock import AsyncMock
from application.services.question_service import QuestionService
from domain.models.question import InterviewQuestion
from domain.ports.ai_service import IAiService

@pytest.mark.asyncio
async def test_generate_interview_questions():
    # Arrange
    mock_ai_service = AsyncMock(spec=IAiService)
    mock_questions = [
        InterviewQuestion(text="What is DI?", category="Technical", difficulty="Easy"),
        InterviewQuestion(text="Tell me about yourself.", category="Behavioral", difficulty="Easy"),
    ]
    mock_ai_service.generate_questions.return_value = mock_questions
    
    service = QuestionService(ai_service=mock_ai_service)
    
    # Act
    result = await service.generate_interview_questions(role="Backend Developer", count=2)
    
    # Assert
    assert len(result) == 2
    assert result[0].text == "What is DI?"
    mock_ai_service.generate_questions.assert_called_once_with("Backend Developer", 2)
