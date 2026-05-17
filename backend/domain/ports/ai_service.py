from abc import ABC, abstractmethod
from typing import List
from domain.models.question import InterviewQuestion


class IAiService(ABC):
    """Interface for AI-based question generation service."""

    @abstractmethod
    async def generate_questions(
        self, role: str, count: int
    ) -> List[InterviewQuestion]:
        """Generates a list of interview questions based on the role.

        Args:
            role (str): The job role to generate questions for.
            count (int): The number of questions to generate.

        Returns:
            List[InterviewQuestion]: A list of generated questions.
        """
        pass
