# Winncom Lead Agent - Development Guide

This guide provides detailed information for developers working on the Winncom Lead Agent project.

## Development Environment Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd winncom-lead-agent
   ```

2. **Set up Python environment**:
   - Use Python 3.11 (recommended and tested)
   - Create and activate a virtual environment:
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
   ```
   
   If you encounter issues with psycopg2-binary:
   ```bash
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

### Adding New API Endpoints

1. Create a new file in `app/api/v1/endpoints/` for your endpoint group
2. Define your router and endpoints
3. Include your router in `app/api/v1/api.py`

Example:
```python
# app/api/v1/endpoints/classification.py
from fastapi import APIRouter, Depends
router = APIRouter()

@router.post("/classify")
async def classify_email():
    # Implementation
    pass

# In app/api/v1/api.py
from app.api.v1.endpoints import classification
api_router.include_router(classification.router, prefix="/classification", tags=["classification"])
```

### Adding New Models

1. Create a new file in `app/models/` for your SQLAlchemy model
2. Create corresponding Pydantic schemas in `app/models/schemas/`
3. Import your model in `app/db/base_class.py` for Alembic to detect it

### Testing

Run tests with pytest:
```bash
pytest
```

Write tests in the `app/tests/` directory following the existing patterns.

## Current Implementation Status

The following components have been implemented:

1. **Project Structure**: Basic FastAPI application structure
2. **Database Models**: User, Gmail account, Email, Classification, and Information extraction
3. **Authentication**: JWT-based authentication system
4. **Gmail Integration**: OAuth flow and email fetching
5. **API Endpoints**: Auth and Gmail endpoints

## Next Development Tasks

1. **Email Classification**:
   - Implement rule-based classification in `app/services/classification.py`
   - Create API endpoints in `app/api/v1/endpoints/classification.py`

2. **Information Extraction**:
   - Implement extraction logic in `app/services/extraction.py`
   - Create API endpoints in `app/api/v1/endpoints/extraction.py`

3. **Response Generation**:
   - Implement response templates and generation logic
   - Create API endpoints for response management

4. **Frontend Development**:
   - Set up a React application for the admin interface
   - Implement authentication and dashboard views

## Coding Standards

1. **Code Formatting**: Use Black for code formatting
2. **Type Hints**: Use type hints throughout the codebase
3. **Documentation**: Document all functions, classes, and modules
4. **Testing**: Write tests for all new functionality

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

### Getting Help

If you encounter issues not covered in this guide:

1. Check the project documentation
2. Review FastAPI documentation for API-related issues
3. Consult SQLAlchemy documentation for database issues
4. Reach out to the project maintainers 