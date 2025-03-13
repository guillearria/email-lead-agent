# Development Guide

This guide provides detailed information for developers working on the Winncom Lead Agent project.

## Table of Contents
- [Development Environment](#development-environment)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Database Management](#database-management)
- [API Development](#api-development)
- [Troubleshooting](#troubleshooting)

## Development Environment

### Prerequisites
- Python 3.11 (recommended)
- Git
- SQLite (for development)
- PostgreSQL (for production)
- Redis (optional for development, required for production)

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd winncom-lead-agent
   ```

2. **Set up Python environment**:
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   
   # If you encounter issues with psycopg2-binary:
   # On Windows:
   pip install $(findstr /v "psycopg2-binary" requirements.txt)
   # On macOS/Linux:
   pip install $(grep -v "psycopg2-binary" requirements.txt)
   ```

4. **Configure environment**:
   - Use the existing `.env` file or copy from `.env.example`
   - For development, SQLite is configured by default
   - Update Gmail API credentials when needed

5. **Initialize the database**:
   ```bash
   python -m app.db.init_db
   ```

### Recommended Development Tools
- **IDE**: Visual Studio Code with Python extension
- **API Testing**: Postman or Insomnia
- **Database Management**: DBeaver or SQLite Browser
- **Code Formatting**: Black
- **Linting**: Flake8
- **Type Checking**: mypy

## Project Structure

```
winncom-lead-agent/
├── alembic/                  # Database migration scripts
├── app/                      # Application code
│   ├── api/                  # API endpoints
│   │   └── v1/               # API version 1
│   │       ├── endpoints/    # API endpoint modules
│   │       └── api.py        # API router
│   ├── core/                 # Core functionality
│   │   └── config.py         # Application configuration
│   ├── db/                   # Database related code
│   │   ├── base.py           # Database setup
│   │   └── init_db.py        # Database initialization
│   ├── models/               # Database models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── user.py           # User model
│   │   ├── gmail_account.py  # Gmail account model
│   │   ├── email.py          # Email model
│   │   └── ...               # Other models
│   ├── services/             # Business logic
│   │   ├── auth.py           # Authentication service
│   │   ├── gmail.py          # Gmail service
│   │   └── ...               # Other services
│   ├── tests/                # Tests
│   └── main.py               # FastAPI application
├── docs/                     # Documentation
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
└── run.py                    # Application entry point
```

## Development Workflow

### Running the Application

```bash
python run.py
```

The application will be available at http://localhost:8000. API documentation is available at http://localhost:8000/docs.

### Development Cycle

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes and test locally**

3. **Run tests**:
   ```bash
   pytest
   ```

4. **Format code**:
   ```bash
   black app/
   ```

5. **Run linting**:
   ```bash
   flake8 app/
   ```

6. **Commit changes**:
   ```bash
   git add .
   git commit -m "Add your feature description"
   ```

7. **Push changes**:
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a pull request** for code review

### Database Migrations

When making changes to database models:

1. **Create a migration**:
   ```bash
   alembic revision --autogenerate -m "Description of changes"
   ```

2. **Apply migrations**:
   ```bash
   alembic upgrade head
   ```

3. **Downgrade if needed**:
   ```bash
   alembic downgrade -1  # Go back one revision
   ```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use [Black](https://black.readthedocs.io/) for code formatting
- Maximum line length: 88 characters (Black default)
- Use 4 spaces for indentation (not tabs)

### Naming Conventions

- **Files**: lowercase with underscores (snake_case)
- **Classes**: CamelCase
- **Functions/Methods**: lowercase with underscores (snake_case)
- **Variables**: lowercase with underscores (snake_case)
- **Constants**: UPPERCASE with underscores

### Documentation

- Document all modules, classes, and functions using docstrings
- Use [Google style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Keep documentation up-to-date with code changes

Example:
```python
def fetch_emails(db: Session, account_id: int, max_results: int = 10) -> List[Dict]:
    """
    Fetch emails from a Gmail account.
    
    Args:
        db: Database session
        account_id: ID of the Gmail account
        max_results: Maximum number of emails to fetch
        
    Returns:
        List of email data dictionaries
    
    Raises:
        ValueError: If account_id is invalid
    """
    # Implementation
```

### Type Hints

- Use type hints for all function parameters and return values
- Use `Optional[Type]` for parameters that can be None
- Use `Union[Type1, Type2]` for parameters that can be multiple types
- Use `List`, `Dict`, `Tuple`, etc. from the `typing` module

### Error Handling

- Use specific exception types
- Handle exceptions at the appropriate level
- Log exceptions with context information
- Return appropriate HTTP status codes in API endpoints

## Testing

### Test Structure

- Place tests in the `app/tests/` directory
- Mirror the application structure in the tests directory
- Use descriptive test names that explain what is being tested

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest app/tests/api/test_auth.py

# Run with coverage report
pytest --cov=app
```

### Test Types

1. **Unit Tests**: Test individual functions and methods
2. **Integration Tests**: Test interactions between components
3. **API Tests**: Test API endpoints using TestClient

### Test Example

```python
def test_authenticate_user_valid_credentials():
    """Test that a user can be authenticated with valid credentials."""
    # Arrange
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = User(
        email="test@example.com",
        password_hash=get_password_hash("password123")
    )
    
    # Act
    result = authenticate_user(db, "test@example.com", "password123")
    
    # Assert
    assert result is not None
    assert result.email == "test@example.com"
```

## Database Management

### SQLAlchemy Models

- Define models in separate files in the `app/models/` directory
- Use appropriate column types and constraints
- Define relationships between models
- Add models to `app/db/base_class.py` for Alembic to detect them

### Pydantic Schemas

- Define schemas in the `app/models/schemas/` directory
- Create separate schemas for different use cases (create, update, response)
- Use validation constraints where appropriate
- Use schema inheritance to reduce duplication

### Database Operations

- Use dependency injection to get database sessions
- Use context managers to ensure sessions are closed
- Use transactions for operations that need to be atomic
- Avoid N+1 query problems by using joins and eager loading

## API Development

### Adding New Endpoints

1. Create a new file in `app/api/v1/endpoints/` for your endpoint group
2. Define your router and endpoints
3. Include your router in `app/api/v1/api.py`

Example:
```python
# app/api/v1/endpoints/classification.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.schemas.classification import ClassificationCreate, ClassificationResponse
from app.services.classification import classify_email

router = APIRouter()

@router.post("/{email_id}", response_model=ClassificationResponse)
async def classify_email_endpoint(
    email_id: int,
    db: Session = Depends(get_db)
):
    """Classify an email."""
    # Implementation
    pass

# In app/api/v1/api.py
from app.api.v1.endpoints import classification
api_router.include_router(classification.router, prefix="/classification", tags=["classification"])
```

### API Design Principles

- Use appropriate HTTP methods (GET, POST, PUT, DELETE)
- Use consistent URL patterns
- Return appropriate status codes
- Validate input data using Pydantic models
- Document endpoints with docstrings and examples
- Handle errors consistently

### Authentication and Authorization

- Secure all endpoints that require authentication
- Use the `get_current_user` dependency for authenticated endpoints
- Implement role-based access control for sensitive operations

## Troubleshooting

### Common Issues

1. **Database Connection Issues**:
   - For development, ensure SQLite file is writable
   - For production, check PostgreSQL connection parameters

2. **Gmail API Authentication**:
   - Verify credentials in `.env` file
   - Ensure redirect URI matches the one in Google Cloud Console
   - Check that required scopes are enabled

3. **Dependency Issues**:
   - Use Python 3.11 for best compatibility
   - If using PostgreSQL, ensure development headers are installed

### Debugging Tips

1. **Enable Debug Mode**:
   - Set `DEBUG=True` in `.env` file
   - Use FastAPI's automatic reload feature

2. **Logging**:
   - Use the logging module to add debug information
   - Check logs for error messages and stack traces

3. **API Testing**:
   - Use the Swagger UI at `/docs` to test endpoints
   - Check request/response data in the browser developer tools

4. **Database Inspection**:
   - Use a database browser to inspect the database directly
   - Check that migrations have been applied correctly 