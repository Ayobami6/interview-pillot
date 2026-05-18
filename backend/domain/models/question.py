from pydantic import BaseModel
from typing import List


class InterviewQuestion(BaseModel):
    """Domain model for an interview question.

    Attributes:
        text (str): The question text.
        category (str): The category of the question (e.g., technical, behavioral).
        difficulty (str): The difficulty level (e.g., easy, medium, hard).
    """

    text: str
    category: str
    difficulty: str


class GenerationRequest(BaseModel):
    """Domain model for a question generation request.

    Attributes:
        role (str): The job role to generate questions for.
        count (int): The number of questions to generate.
    """

    role: str
    count: int = 3
