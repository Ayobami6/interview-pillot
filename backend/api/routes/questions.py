from fastapi import APIRouter, Depends
from api.schemas.service_response import ServiceResponse
from api.middlewares.exceptions import exception_before_advice
from api.dependencies import get_question_service
from application.services.question_service import IQuestionService
from domain.models.question import GenerationRequest

router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("/generate", response_model=ServiceResponse)
@exception_before_advice
async def generate_questions(
    payload: GenerationRequest,
    question_service: IQuestionService = Depends(get_question_service),
) -> ServiceResponse:
    """Generates interview questions based on the job role.

    Args:
        payload (GenerationRequest): Request body with role and count.
        question_service (IQuestionService): Injected service.

    Returns:
        ServiceResponse: Standardized service response.
    """
    questions = await question_service.generate_interview_questions(
        role=payload.role, count=payload.count
    )

    return ServiceResponse(
        message="Questions generated successfully",
        success=True,
        status_code=200,
        data=[q.model_dump() for q in questions],
    )
