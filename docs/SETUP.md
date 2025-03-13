# Setup Guide

This guide provides detailed instructions for setting up the Winncom Lead Agent application for development and production environments.

## Table of Contents
- [Environment Requirements](#environment-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Gmail API Setup](#gmail-api-setup)
- [Running the Application](#running-the-application)
- [Troubleshooting](#troubleshooting)

## Environment Requirements

### Python
- **Version**: Python 3.11 is recommended and confirmed working
- **Compatibility Notes**:
  - Python 3.13 has compatibility issues with some dependencies (psycopg2-binary and pydantic-core)
  - Python 3.8+ should work but 3.11 is tested and confirmed

### Database
- **Development**: SQLite (included in the `.env` file)
- **Production**: PostgreSQL recommended

### Redis
- **Development**: Optional, can be skipped
- **Production**: Required for caching and Celery task queue

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd winncom-lead-agent
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
```

### 3. Activate the Virtual Environment
- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies

#### Standard Installation
```bash
pip install -r requirements.txt
```

#### Development Installation (SQLite only)
If you encounter issues with psycopg2-binary and are using SQLite for development:

- **Windows**:
  ```bash
  pip install $(findstr /v "psycopg2-binary" requirements.txt)
  ```
- **macOS/Linux**:
  ```bash
  pip install $(grep -v "psycopg2-binary" requirements.txt)
  ```

#### Production Installation
For production, ensure PostgreSQL development files are installed on your system before installing dependencies:

- **Ubuntu/Debian**:
  ```bash
  sudo apt-get install libpq-dev python3-dev
  pip install -r requirements.txt
  ```
- **Windows**:
  Install PostgreSQL from the [official website](https://www.postgresql.org/download/windows/)

## Configuration

### Environment Variables

1. **Development**:
   - Copy `.env.example` to `.env` or use the existing `.env` file
   - SQLite is configured by default for development

2. **Production**:
   - Create a secure `.env` file with production settings
   - Update database URL to use PostgreSQL
   - Set `DEBUG=False` and `ENVIRONMENT=production`
   - Generate a secure `SECRET_KEY`

### Key Environment Variables

```
# Application settings
APP_NAME=Winncom Lead Agent
ENVIRONMENT=development  # or production
DEBUG=True  # False in production
LOG_LEVEL=INFO

# Server settings
HOST=0.0.0.0
PORT=8000

# Database settings
DATABASE_URL=sqlite:///./test.db  # For development
# DATABASE_URL=postgresql://user:password@localhost:5432/winncom_lead_agent  # For production
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

## Database Setup

### Initialize the Database
```bash
python -m app.db.init_db
```

This will:
- Create all database tables
- Create a default admin user (email: admin@example.com, password: admin123)

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

## Gmail API Setup

### Create Google Cloud Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Gmail API for your project

### Create OAuth 2.0 Credentials
1. Go to "Credentials" in the Google Cloud Console
2. Create OAuth 2.0 Client ID credentials (Web application type)
3. Add authorized redirect URIs:
   - For development: `http://localhost:8000/api/gmail/callback`
   - For production: `https://your-domain.com/api/gmail/callback`

### Update Environment Variables
Update the following variables in your `.env` file:
```
GMAIL_CLIENT_ID=your-client-id-here
GMAIL_CLIENT_SECRET=your-client-secret-here
GMAIL_REDIRECT_URI=http://localhost:8000/api/gmail/callback  # Update for production
```

## Running the Application

### Development
```bash
python run.py
```

### Production
For production, it's recommended to use a production ASGI server like Uvicorn with Gunicorn:

1. **Install Gunicorn**:
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn**:
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
   ```

3. **With Nginx** (recommended):
   Set up Nginx as a reverse proxy to the Gunicorn server

## Troubleshooting

### Common Issues

#### psycopg2-binary Installation Issues
- **Error**: `pg_config executable not found`
- **Solution**: 
  - For development, use SQLite instead
  - For production, install PostgreSQL development files

#### Database Connection Issues
- **Error**: `Unable to connect to database`
- **Solutions**:
  - Check that the database URL in `.env` is correct
  - Ensure the database server is running
  - Verify database user permissions

#### Gmail API Authentication Issues
- **Error**: `Invalid client secret` or `Redirect URI mismatch`
- **Solutions**:
  - Verify credentials in `.env` file
  - Ensure redirect URI matches exactly what's in Google Cloud Console
  - Check that required scopes are enabled

#### Python Version Compatibility
- **Error**: Various dependency errors with Python 3.13
- **Solution**: Use Python 3.11 for best compatibility 