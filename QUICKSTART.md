# Winncom Lead Agent - Quick Start Guide

This guide will help you get the Winncom Lead Agent application up and running quickly for development.

## Prerequisites

- Python 3.11 (recommended)
- Git

## Setup Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd winncom-lead-agent
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt

# If you have issues with psycopg2-binary:
# On Windows:
pip install $(findstr /v "psycopg2-binary" requirements.txt)
# On macOS/Linux:
pip install $(grep -v "psycopg2-binary" requirements.txt)
```

### 4. Initialize the Database

```bash
python -m app.db.init_db
```

This creates a SQLite database with a default admin user:
- Email: admin@example.com
- Password: admin123

### 5. Run the Application

```bash
python run.py
```

The application will be available at:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs to see available endpoints
2. **Set up Gmail API**: Create credentials in Google Cloud Console and update `.env`
3. **Review the code**: Familiarize yourself with the project structure
4. **Check documentation**: See DEVELOPMENT.md for more detailed information

## Common Issues

- **Database errors**: Make sure the SQLite file is writable
- **Gmail API errors**: Verify your credentials in the `.env` file
- **Dependency issues**: Ensure you're using Python 3.11

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Gmail API Documentation](https://developers.google.com/gmail/api/guides) 