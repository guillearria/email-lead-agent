# Winncom Lead Agent - Requirements Documentation

## Environment Requirements

- **Python**: Version 3.11 is recommended and confirmed working
  - Python 3.13 has compatibility issues with some dependencies (psycopg2-binary and pydantic-core)
  - Python 3.8+ should work but 3.11 is tested and confirmed

- **Database**:
  - **Development**: SQLite (included in the `.env` file)
  - **Production**: PostgreSQL recommended

- **Redis** (optional for development):
  - Required for production for caching and Celery task queue
  - Can be skipped during initial development

## Dependencies

The project relies on the following key dependencies:

### Web Framework
- **FastAPI** (0.104.1): Modern, high-performance web framework
- **Uvicorn** (0.23.2): ASGI server for running the application
- **Pydantic** (2.4.2): Data validation and settings management

### Database
- **SQLAlchemy** (2.0.23): SQL toolkit and ORM
- **Alembic** (1.12.1): Database migration tool
- **psycopg2-binary** (2.9.9): PostgreSQL adapter (optional for development)

### Authentication
- **python-jose** (3.3.0): JWT token handling
- **passlib** (1.7.4): Password hashing
- **bcrypt** (4.0.1): Password hashing algorithm

### Gmail API
- **google-api-python-client** (2.108.0): Google API client
- **google-auth** (2.23.4): Google authentication
- **google-auth-oauthlib** (1.1.0): OAuth 2.0 for Google APIs
- **google-auth-httplib2** (0.1.1): HTTP client for Google Auth

### Background Tasks
- **Celery** (5.3.4): Distributed task queue

### Testing
- **pytest** (7.4.3): Testing framework
- **httpx** (0.25.1): HTTP client for testing

### Utilities
- **email-validator** (2.1.0): Email validation
- **python-dateutil** (2.8.2): Date utilities
- **python-dotenv** (1.0.0): Environment variable management
- **python-multipart** (0.0.6): Form data parsing

## Installation Instructions

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   If you encounter issues with psycopg2-binary and are using SQLite for development:
   ```bash
   # Install all requirements except psycopg2-binary
   pip install $(grep -v "psycopg2-binary" requirements.txt)
   ```

## Configuration

1. **Environment Variables**:
   - Copy `.env.example` to `.env` (or use the existing `.env` file)
   - Update the values as needed
   - For development, the SQLite configuration is already set up

2. **Gmail API Setup**:
   - Create a project in the [Google Cloud Console](https://console.cloud.google.com/)
   - Enable the Gmail API
   - Create OAuth 2.0 credentials (Web application type)
   - Set the authorized redirect URI to match `GMAIL_REDIRECT_URI` in your `.env` file
   - Update the `.env` file with your credentials

## Database Setup

1. **Initialize the database**:
   ```bash
   python -m app.db.init_db
   ```

   This will:
   - Create all database tables
   - Create a default admin user (email: admin@example.com, password: admin123)

2. **Run migrations** (when needed):
   ```bash
   alembic upgrade head
   ```

## Running the Application

1. **Start the application**:
   ```bash
   python run.py
   ```

2. **Access the API documentation**:
   - Open your browser and navigate to `http://localhost:8000/docs`

## Known Issues and Workarounds

1. **psycopg2-binary installation issues**:
   - For development, you can use SQLite instead (already configured in `.env`)
   - For production, ensure PostgreSQL development files are installed on your system

2. **Python 3.13 compatibility**:
   - Some dependencies (psycopg2-binary, pydantic-core) have issues with Python 3.13
   - Use Python 3.11 for best compatibility

## Next Development Steps

1. **Email Classification**: Implement the classification engine
2. **Information Extraction**: Develop the information extraction service
3. **Response Generation**: Create the response generation system
4. **Frontend Development**: Build the web interface for human review 