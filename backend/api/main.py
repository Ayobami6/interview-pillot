from fastapi import FastAPI
from api.routes import questions
from api.middlewares.exceptions import exception_handler
from api.schemas.service_response import ServiceException

app = FastAPI(
    title="Interview Pillot API",
    description="Backend for AI Interview Question Generator",
    version="1.0.0",
)

# Register exception handler
app.add_exception_handler(ServiceException, exception_handler)

# Include routers
app.include_router(questions.router, prefix="/api/v1")

@app.get("/")
async def health_check():
    return {"status": "healthy", "service": "interview-pillot-backend"}
