# Email Lead Agent

![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.106.0-lightblue.svg)

## Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Quick Start Guide](#quick-start-guide)
- [Testing](#testing)
- [Development Guide](#development-guide)
- [Architecture](#architecture)
- [API Documentation](#api-documentation)
- [Database Management](#database-management)
- [Troubleshooting](#troubleshooting)
- [Current Implementation Status](#current-implementation-status)
- [Next Development Steps](#next-development-steps)
- [Glossary](#glossary)

## Project Overview

The Email Lead Agent is an automated email processing system designed to monitor a Gmail inbox, classify incoming emails as leads or information requests, generate appropriate responses, and forward them to human agents for review before sending.

## Key Features

- **Gmail Integration**: Seamlessly connects with Gmail to monitor and process incoming emails
- **Email Classification**: Automatically categorizes emails as sales leads or information requests
- **Information Extraction**: Identifies and extracts key details from incoming emails
- **Response Generation**: Creates tailored responses based on email content and available knowledge base
- **Human Review Interface**: Provides an easy-to-use interface for reviewing and approving generated responses
- **Web-Based Access**: Accessible via browser tab or potentially as a browser extension

## Quick Start Guide

### Prerequisites

- Python 3.11 (recommended)
- Git

### Setup Steps

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd email-lead-agent
   ```

2. **Set Up Python Environment**:
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   
   # If you have issues with psycopg2-binary:
   # On Windows:
   pip install $(findstr /v "psycopg2-binary" requirements.txt)
   # On macOS/Linux:
   pip install $(grep -v "psycopg2-binary" requirements.txt)
   ```

4. **Initialize the Database**:
   ```bash
   python -m app.db.init_db
   ```

5. **Run the Application**:
   ```bash
   python run.py
   ```

The application will be available at:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

Default admin credentials:
- Email: admin@example.com
- Password: admin123

## Testing

The Email Lead Agent follows test-driven development (TDD) principles with a comprehensive test suite. The tests are organized by component type and ensure reliability and stability of the application.

### Running Tests

To run the test suite, make sure you have the testing dependencies installed:

```bash
pip install pytest pytest-cov
```

Then, you can run the tests with:

```bash
# Run all tests
python -m pytest

# Run tests with verbose output
python -m pytest -v

# Run tests for a specific module
python -m pytest app/tests/test_models -v
```

### Test Coverage

To check test coverage, use the pytest-cov plugin:

```bash
# Run tests with coverage report
python -m pytest --cov=app

# Generate a more detailed coverage report
python -m pytest --cov=app --cov-report=term-missing

# Generate HTML coverage report
python -m pytest --cov=app --cov-report=html
# Then open htmlcov/index.html in your browser
```

### Test Structure

The tests are organized to mirror the application structure:

- **Model Tests** (`app/tests/test_models/`): Tests for database models and their relationships
- **Service Tests** (`app/tests/test_services/`): Tests for business logic services
- **API Tests** (`app/tests/test_api/`): Tests for API endpoints
- **Integration Tests** (`app/tests/test_integration/`): Tests for end-to-end workflows

### Writing New Tests

When contributing new code to the project, please follow these guidelines for writing tests:

1. **Follow the TDD Approach**:
   - Write tests before implementing features
   - Ensure all tests pass after implementation
   - Refactor while keeping tests passing

2. **Test Organization**:
   - Place tests in the appropriate directory based on what they test
   - Name test files as `test_*.py` and test functions as `test_*`
   - Group related tests in classes when appropriate

3. **Test Structure**:
   - Use the Arrange-Act-Assert pattern for clear test structure
   - Include descriptive docstrings explaining what each test verifies
   - Keep tests independent and idempotent

4. **Test Coverage**:
   - Aim for high test coverage (ideally 90%+ for critical components)
   - Test both success and failure scenarios
   - Test edge cases and boundary conditions

### Example Test

```python
def test_user_creation(db_session):
    """Test that a user can be created with the required fields."""
    # Arrange & Act
    user = User(
        email="test@example.com",
        name="Test User",
        password_hash="hashed_password",
        role="reviewer"
    )
    db_session.add(user)
    db_session.commit()
    
    # Assert
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.role == "reviewer"
```

## Development Guide

### Environment Requirements

- **Python**: 3.11 is recommended (compatibility issues exist with Python 3.13)
- **Database**: 
  - Development: SQLite (included)
  - Production: PostgreSQL recommended
- **Redis**: 
  - Development: Optional, can be skipped
  - Production: Required for caching and Celery task queue

### Project Structure

```
email-lead-agent/
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
├── .env.example              # Example environment variables
├── .gitignore                # Git ignore file
├── alembic.ini               # Alembic configuration
├── requirements.txt          # Python dependencies
└── run.py                    # Application entry point
```

### Configuration

#### Environment Variables

The application uses environment variables for configuration. These are stored in the `.env` file. A sample `.env.example` file is provided.

Key environment variables:

```
# Application settings
APP_NAME=Email Lead Agent
ENVIRONMENT=development  # or production
DEBUG=True  # False in production
LOG_LEVEL=INFO

# Server settings
HOST=0.0.0.0
PORT=8000

# Database settings
DATABASE_URL=sqlite:///./test.db  # For development
# DATABASE_URL=postgresql://user:password@localhost:5432/email_lead_agent  # For production
REDIS_URL=redis://localhost:6379/0

# Authentication
SECRET_KEY=your-secret-key-here  # Change this in production!
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Gmail API
GMAIL_CLIENT_ID=your-client-id-here
GMAIL_CLIENT_SECRET=your-client-secret-here
GMAIL_REDIRECT_URI=http://localhost:8000/api/gmail/callback
GMAIL_TOKEN_URI=https://oauth2.googleapis.com/token
GMAIL_AUTH_URI=https://accounts.google.com/o/oauth2/auth
GMAIL_SCOPES=https://www.googleapis.com/auth/gmail.readonly
```

### Coding Standards

- **Python Style Guide**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) 
- **Formatter**: Use [Black](https://black.readthedocs.io/) with default settings
- **Line Length**: 88 characters (Black default)
- **Indentation**: 4 spaces (no tabs)
- **Docstrings**: Google style docstrings for all modules, classes, and functions
- **Type Hints**: Use type hints for all function parameters and return values

#### Naming Conventions
- **Files**: lowercase with underscores (snake_case)
- **Classes**: CamelCase
- **Functions/Methods**: lowercase with underscores (snake_case)
- **Variables**: lowercase with underscores (snake_case)
- **Constants**: UPPERCASE with underscores

### Gmail API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Gmail API for your project
4. Create OAuth 2.0 Client ID credentials (Web application type)
5. Add authorized redirect URIs:
   - For development: `http://localhost:8000/api/gmail/callback`
   - For production: `https://your-domain.com/api/gmail/callback`
6. Update environment variables with your credentials

### Development Workflow

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

## Architecture

### System Overview

The Email Lead Agent consists of six major components:
1. **Email Processing Service**: Connects to Gmail and manages the email processing pipeline
2. **Classification Engine**: Analyzes email content to determine if it's a lead or information request
3. **Information Extraction Service**: Extracts structured data from emails
4. **Data Storage Layer**: Stores all system data securely and efficiently
5. **Web Frontend**: Provides the user interface for human reviewers
6. **Authentication & Authorization Service**: Manages user authentication and access control

### Architecture Diagram (Text Representation)

```
┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │
│  Gmail Server   │◄────┤  Human Reviewer │
│                 │     │                 │
└────────┬────────┘     └────────▲────────┘
         │                       │
         │                       │
         ▼                       │
┌─────────────────┐     ┌────────┴────────┐
│                 │     │                 │
│ Email Processing│     │  Web Frontend   │
│    Service      │     │                 │
│                 │     │                 │
└────────┬────────┘     └────────▲────────┘
         │                       │
         │                       │
         ▼                       │
┌─────────────────┐     ┌────────┴────────┐
│                 │     │                 │
│ Classification  │     │    API Layer    │
│    Engine       │─────►                 │
│                 │     │                 │
└────────┬────────┘     └────────▲────────┘
         │                       │
         │                       │
         ▼                       │
┌─────────────────┐     ┌────────┴────────┐
│                 │     │                 │
│  Information    │     │ Authentication  │
│  Extraction     │     │ & Authorization │
│                 │     │                 │
└────────┬────────┘     └────────▲────────┘
         │                       │
         │                       │
         ▼                       │
┌─────────────────────────────────────────┐
│                                         │
│              Data Storage               │
│     (PostgreSQL + Redis Cache)          │
│                                         │
└─────────────────────────────────────────┘
```

### Database Schema (Core Tables)

1. **users**
   - id (PK)
   - email
   - name
   - password_hash
   - role
   - created_at
   - last_login

2. **gmail_accounts**
   - id (PK)
   - email
   - access_token (encrypted)
   - refresh_token (encrypted)
   - connected_at
   - last_sync
   - status

3. **emails**
   - id (PK)
   - account_id (FK to gmail_accounts)
   - gmail_id
   - thread_id
   - subject
   - sender_name
   - sender_email
   - received_at
   - body_text
   - body_html
   - status
   - created_at
   - updated_at

4. **email_classifications**
   - id (PK)
   - email_id (FK to emails)
   - category
   - subcategory
   - confidence
   - classified_at
   - classified_by (algorithm or user_id)

5. **extracted_information**
   - id (PK)
   - email_id (FK to emails)
   - contact_info (JSONB)
   - product_interests (JSONB)
   - questions (JSONB)
   - urgency
   - extracted_at

## API Documentation

The Email Lead Agent exposes a RESTful API for accessing email processing, classification, and management features. The API uses JWT authentication, consistent error handling, and clear request/response formats.

### Base URL

- **Development**: `http://localhost:8000/api`
- **Production**: `https://your-domain.com/api`

### Authentication

All API endpoints (except authentication endpoints) require a valid JWT token:

```
Authorization: Bearer <your_token>
```

### API Categories

1. **Authentication**: User login, logout, and token management
2. **Gmail Integration**: Connect Gmail accounts and fetch emails
3. **Email Processing**: Process and manage emails
4. **Classification**: Classify emails as leads or information requests
5. **Information Extraction**: Extract structured data from emails

### Key API Endpoints

#### Authentication

- `POST /auth/login`: Authenticates a user and returns a JWT token
- `POST /auth/logout`: Logs out a user by invalidating their token
- `POST /auth/refresh`: Refreshes an expired access token
- `GET /auth/me`: Returns the current authenticated user's information

#### Gmail Integration

- `POST /gmail/authorize`: Initiates the OAuth 2.0 flow for Gmail authorization
- `POST /gmail/callback`: Handles the OAuth 2.0 callback from Google
- `GET /gmail/accounts`: Lists all connected Gmail accounts
- `DELETE /gmail/accounts/{account_id}`: Disconnects a Gmail account
- `POST /gmail/emails/fetch`: Triggers the email fetching process

#### Email Management

- `GET /emails`: Retrieves a paginated list of processed emails
- `GET /emails/{email_id}`: Retrieves detailed information about a specific email
- `PUT /emails/{email_id}/status`: Updates the status of an email

#### Classification

- `POST /classification/classify`: Submits an email for classification
- `GET /classification/{email_id}`: Retrieves classification results
- `POST /classification/{email_id}/feedback`: Submits feedback on classification

#### Information Extraction

- `POST /extraction/extract`: Submits an email for information extraction
- `GET /extraction/{email_id}`: Retrieves extracted information

### API Documentation

For detailed API documentation, access the Swagger UI at:
```
http://localhost:8000/docs
```

### Error Handling

All API errors follow a consistent format:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested resource was not found",
    "details": {
      "resource_type": "email",
      "resource_id": "email123"
    }
  }
}
```

Common HTTP status codes:
- 200 OK: Successful operation
- 400 Bad Request: Invalid request parameters
- 401 Unauthorized: Authentication required or failed
- 403 Forbidden: Authenticated but not authorized
- 404 Not Found: Resource not found
- 422 Unprocessable Entity: Validation error
- 500 Internal Server Error: Unexpected server error

## Database Management

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

## Troubleshooting

### Common Issues

#### Installation Issues
- **psycopg2-binary error**: `pg_config executable not found`
  - For development, use SQLite instead
  - For production, install PostgreSQL development files
  
#### Database Issues
- **Connection errors**: 
  - Check that the database URL in `.env` is correct
  - Ensure the database server is running
  - Verify database user permissions

#### Gmail API Issues
- **Authentication errors**: 
  - Verify credentials in `.env` file
  - Ensure redirect URI matches exactly what's in Google Cloud Console
  - Check that required scopes are enabled

#### Python Version Compatibility
- Dependency errors with Python 3.13
  - Use Python 3.11 for best compatibility

### Debugging Tips

1. **Enable Debug Mode**:
   - Set `DEBUG=True` in `.env` file
   - Use FastAPI's automatic reload feature

2. **Check Logs**:
   - Use the logging module to add debug information
   - Check logs for error messages and stack traces

3. **API Testing**:
   - Use the Swagger UI at `/docs` to test endpoints
   - Check request/response data in the browser developer tools

## Current Implementation Status

The following components have been implemented:

1. **Project Structure**: Basic FastAPI application structure
2. **Database Models**: User, Gmail account, Email, Classification, and Information extraction
3. **Authentication**: JWT-based authentication system
4. **Gmail Integration**: OAuth flow and email fetching
5. **API Endpoints**: Auth and Gmail endpoints
6. **Testing**: Comprehensive test suite for database models

## Next Development Steps

1. **Email Classification**: Implement the classification engine
2. **Information Extraction**: Develop the information extraction service
3. **Response Generation**: Create the response generation system
4. **Frontend Development**: Build the web interface for human review
5. **Additional Testing**: Expand test coverage to services and API endpoints

## Glossary

**Lead**: A potential sales opportunity identified from an email, typically from a new or existing customer expressing interest in products or services.

**Information Request**: An email inquiry seeking specific information about products, services, or company details, but not necessarily indicating immediate purchase intent.

**Classification**: The process of categorizing incoming emails as leads, information requests, or other categories based on content analysis.

**Information Extraction**: The process of identifying and extracting structured data (like contact information, product interests, etc.) from unstructured email text.