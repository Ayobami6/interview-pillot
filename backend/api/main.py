from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from api.routes import questions
from api.middlewares.exceptions import exception_handler
from api.schemas.service_response import ServiceException

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Interview Pillot API",
    description="Backend for AI Interview Question Generator",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handler
app.add_exception_handler(ServiceException, exception_handler)

# Include routers
app.include_router(questions.router, prefix="/api/v1")

@app.get("/")
async def health_check():
    return {"status": "healthy", "service": "interview-pillot-backend"}
