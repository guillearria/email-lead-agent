# Winncom Lead Agent

## Project Overview

The Winncom Lead Agent is an automated email processing system designed to monitor a Gmail inbox, classify incoming emails as leads or information requests, generate appropriate responses, and forward them to human agents for review before sending.

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
   cd winncom-lead-agent
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

## Documentation Structure

This project's documentation is organized into the following files:

1. **[README.md](README.md)** (this file): Project overview, quick start guide, and documentation structure
2. **[docs/SETUP.md](docs/SETUP.md)**: Detailed installation and configuration instructions
3. **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**: System architecture and component design
4. **[docs/API.md](docs/API.md)**: API endpoint specifications and data formats
5. **[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)**: Development workflow, coding standards, and best practices

## Current Implementation Status

The following components have been implemented:

1. **Project Structure**: Basic FastAPI application structure
2. **Database Models**: User, Gmail account, Email, Classification, and Information extraction
3. **Authentication**: JWT-based authentication system
4. **Gmail Integration**: OAuth flow and email fetching
5. **API Endpoints**: Auth and Gmail endpoints

## Next Development Steps

1. **Email Classification**: Implement the classification engine
2. **Information Extraction**: Develop the information extraction service
3. **Response Generation**: Create the response generation system
4. **Frontend Development**: Build the web interface for human review

## Glossary

**Lead**: A potential sales opportunity identified from an email, typically from a new or existing customer expressing interest in Winncom's computer products or services.

**Information Request**: An email inquiry seeking specific information about products, services, or company details, but not necessarily indicating immediate purchase intent.

**Classification**: The process of categorizing incoming emails as leads, information requests, or other categories based on content analysis.

**Information Extraction**: The process of identifying and extracting structured data (like contact information, product interests, etc.) from unstructured email text.