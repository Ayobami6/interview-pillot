from application.services.question_service import QuestionService, IQuestionService
from infrastructure.adapters.adk_adapter import AdkAdapter
from domain.ports.ai_service import IAiService

def get_ai_service() -> IAiService:
    """Provides a singleton-like instance of the AI service."""
    # In a more complex app, you might want to cache this or use a DI container
    return AdkAdapter()

def get_question_service() -> IQuestionService:
    """Provides the question application service."""
    ai_service = get_ai_service()
    return QuestionService(ai_service=ai_service)
