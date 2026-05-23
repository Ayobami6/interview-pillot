# 🐍 Interview Pillot Backend API

A highly structured, production-ready FastAPI application built using **Hexagonal Architecture (Ports and Adapters)**. This service powers the AI generation of custom interview questions, utilizing the **Google Antigravity SDK (ADK)**.

---

## 🛠️ Technology Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Asynchronous ASGI API framework)
- **Runtime**: Python `3.14+`
- **Package Manager**: [uv](https://github.com/astral-sh/uv) (Fast, modern Python packaging)
- **Validation**: [Pydantic v2](https://docs.pydantic.dev/latest/) (Data validation and settings)
- **AI Core**: [Google Antigravity SDK (ADK)](https://github.com) (Agent framework with state/sessions management)
- **Testing**: [pytest](https://docs.pytest.org/) with `pytest-asyncio` for asynchronous test runners

---

## 🏛️ Hexagonal Architecture Breakdown

This backend relies on decoupling the application's core logic from delivery mechanisms and infrastructure adapters.

```
backend/
├── api/                       # API Delivery Layer (FastAPI controllers, schemas, & middlewares)
│   ├── middlewares/           # Custom middlewares & advice handlers
│   ├── routes/                # FastAPI Routers (HTTP endpoint controllers)
│   ├── schemas/               # API Response & Error JSON models
│   ├── dependencies.py        # Dependency Injection (Wiring Ports with concrete Adapters)
│   └── main.py                # FastAPI Application initialisation
├── application/               # Application Service Layer
│   └── services/              # Orchestration of business use-cases
├── domain/                    # Core Domain Layer (100% abstract & independent)
│   ├── models/                # Business Domain models
│   └── ports/                 # Interface contracts (ports) defined using ABC
├── infrastructure/            # Infrastructure Adapters (External systems, frameworks, & tools)
│   └── adapters/              # Concrete implementations of core domain ports
└── tests/                     # Unit and Integration test suites
```

### 1. The Core Domain (`domain/`)
The core domain is completely isolated. It doesn't import from FastAPI, Pydantic settings, or any third-party framework (except Pydantic for simple serialization).
* **Models (`domain/models/question.py`)**: Defines `InterviewQuestion` and `GenerationRequest` types.
* **Ports (`domain/ports/ai_service.py`)**: Defines `IAiService(ABC)`, which sets the contract for generating role-based questions.

### 2. The Application Layer (`application/`)
Orchestrates domain models and ports to execute workflows.
* **Services (`application/services/question_service.py`)**: Implements `IQuestionService` as `QuestionService` which is initialized with `ai_service: IAiService` and directs generation tasks.

### 3. Concrete Adapters (`infrastructure/`)
Contains technology-specific details.
* **Adapters (`infrastructure/adapters/adk_adapter.py`)**: Implements `IAiService` using the `google.adk` libraries. It constructs an AI Agent, manages sessions asynchronously with `InMemorySessionService`, and interacts with LLMs via `Runner.run_async`.

### 4. Dependency Injection (`api/dependencies.py`)
Decoupled interfaces are wired dynamically at runtime using FastAPI dependencies:
```python
def get_ai_service() -> IAiService:
    return AdkAdapter()

def get_question_service() -> IQuestionService:
    ai_service = get_ai_service()
    return QuestionService(ai_service=ai_service)
```

---

## 📡 API Reference

### Generate Interview Questions

* **Endpoint**: `POST /api/v1/questions/generate`
* **Content-Type**: `application/json`
* **Request Body**:
  ```json
  {
    "role": "Senior Python Backend Engineer",
    "count": 3
  }
  ```

* **Standard Success Response (`200 OK`)**:
  ```json
  {
    "message": "Questions generated successfully",
    "success": true,
    "status_code": 200,
    "data": [
      {
        "text": "Explain how you would handle race conditions in an async FastAPI service using Redis.",
        "category": "Technical",
        "difficulty": "Hard"
      },
      {
        "text": "Describe a scenario where you had to redesign an API to satisfy Hexagonal design patterns.",
        "category": "System Design",
        "difficulty": "Medium"
      }
    ]
  }
  ```

* **Standard Error Response (`500 Internal Server Error`)**:
  ```json
  {
    "message": "Don't panic, this is from us!",
    "success": false,
    "status_code": 500
  }
  ```

---

## 🛡️ Exception Handling & Advice Pattern

All controllers are decorated with `@exception_before_advice` located in `api/middlewares/exceptions.py`. This wrapper guarantees that any unhandled runtime exceptions are intercepted, logged, and mapped to a uniform `ServiceException`, preventing internal server tracebacks from leaking to API consumers.

---

## 🧪 Running Tests

Tests are organized inside `tests/` into `unit/` and `integration/` suites.

To run the full test suite with coverage:
```bash
# Run pytest directly inside uv environment
uv run pytest
```
