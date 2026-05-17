from typing import List
from abc import ABC, abstractmethod
from domain.models.question import InterviewQuestion
from domain.ports.ai_service import IAiService


class IQuestionService(ABC):
    """Interface for the question application service."""

    @abstractmethod
    async def generate_interview_questions(
        self, role: str, count: int
    ) -> List[InterviewQuestion]:
        pass


class QuestionService(IQuestionService):
    """Application service for handling interview question logic."""

    def __init__(self, ai_service: IAiService):
        self.ai_service = ai_service

    async def generate_interview_questions(
        self, role: str, count: int
    ) -> List[InterviewQuestion]:
        """Orchestrates question generation using the AI port.

        Args:
            role (str): The job role.
            count (int): How many questions.

        Returns:
            List[InterviewQuestion]: Generated questions.
        """
        questions = await self.ai_service.generate_questions(role, count)
        return questions
