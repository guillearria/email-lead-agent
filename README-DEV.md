# Winncom Lead Agent - Developer Guide

This guide provides instructions for setting up and running the Winncom Lead Agent application for development.

## Project Overview

The Winncom Lead Agent is an automated email processing system designed to monitor a Gmail inbox, classify incoming emails as leads or information requests, generate appropriate responses, and forward them to human agents for review before sending.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- PostgreSQL (optional, SQLite can be used for development)
- Redis (optional, can be skipped for basic development)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd winncom-lead-agent
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Update the values in `.env` as needed
   - For Gmail API integration, you'll need to create a project in the Google Cloud Console and obtain OAuth 2.0 credentials

5. Initialize the database:
   ```bash
   python -m app.db.init_db
   ```

### Running the Application

1. Start the application:
   ```bash
   python run.py
   ```

2. Access the API documentation:
   - Open your browser and navigate to `http://localhost:8000/docs`

### Development Workflow

1. Make changes to the code
2. Run tests (when implemented)
3. Start the application to test your changes

## API Endpoints

### Authentication

- `POST /api/auth/login`: Login and get access token
- `POST /api/auth/refresh`: Refresh access token
- `POST /api/auth/logout`: Logout
- `GET /api/auth/me`: Get current user information
- `POST /api/auth/register`: Register a new user

### Gmail Integration

- `POST /api/gmail/authorize`: Get authorization URL for Gmail API
- `POST /api/gmail/callback`: Handle OAuth callback from Gmail API
- `GET /api/gmail/accounts`: List connected Gmail accounts
- `DELETE /api/gmail/accounts/{account_id}`: Disconnect a Gmail account
- `POST /api/gmail/emails/fetch`: Fetch emails from a Gmail account

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
├── .env.example              # Example environment variables
├── .gitignore                # Git ignore file
├── alembic.ini               # Alembic configuration
├── requirements.txt          # Python dependencies
└── run.py                    # Application entry point
```

## Default Credentials

For development, a default admin user is created:
- Email: admin@example.com
- Password: admin123

**Note**: Change these credentials in production!

## Next Steps

1. Implement email classification
2. Implement information extraction
3. Implement response generation
4. Develop the frontend interface 