# Development Rules & Standards

### 1. Coding Style (Python)
- **Type Hinting:** Mandatory for all function signatures and class attributes.
- **Docstrings:** Use Google-style docstrings for any public-facing method.
- **Imports:** Use absolute imports for all modules and always put imports at the top of the file.

### 2. API Standards (DRF)
- always use the `exception_before_advice` decorator to handle exceptions  and return consistent service responses `ServiceResponse`. check the `auth_service_api` repository for the full implementation of the `exception_before_advice` decorator and `ServiceResponse` schema.
```
@routes.post("/register", response_model=ServiceResponse)
@exception_before_advice
async def register(
    user_payload: CreateUserSchema,
    user_service: UserService = Depends(get_user_service),
) -> ServiceResponse:
    user: UserSchema = await user_service.create_user(user_payload)
    response: ServiceResponse = ServiceResponse(
        message="User created successfully",
        success=True,
        status_code=201,
        data=user.model_dump(exclude_none=True),
    )
    return response
```
- Always use the idea of hexagonal architecture and orthogonality for implementation of the services and repositories, this ensures that the business logic is decoupled from the infrastructure concerns, which makes the code easier to test, maintain, and scale, use ABC from abstract base class to define the interfaces/contracts for the services and repositories, for example:

```python
from abc import ABC, abstractmethod

class IUserService(ABC):
    @abstractmethod
    async def create_user(self, user_payload: CreateUserSchema) -> UserSchema:
        pass

class IUserRepository(ABC):
    @abstractmethod
    async def create_user(self, user_payload: CreateUserSchema) -> UserSchema:
        pass

# Implementation
class UserService(IUserService):
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def create_user(self, user_payload: CreateUserSchema) -> UserSchema:
        return await self.user_repo.create_user(user_payload)
```

### Testing Standards (pytest)
- all new endpoints must have unit tests and integration tests.
- unit tests should be in the `tests/unit/` directory and integration tests should be in the `tests/integration/` directory.
- unit tests should use the `MockService` to mock the service layer and integration tests should use the `TestClient` to test the endpoint.

