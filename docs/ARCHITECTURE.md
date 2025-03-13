# System Architecture

## Executive Summary

The Winncom Lead Agent is designed as a modular, scalable system that processes emails from Gmail, classifies them, extracts relevant information, and facilitates human review. The architecture follows modern best practices with clear separation of concerns, API-driven interactions, and a focus on maintainability and extensibility.

## Overview

The system consists of six major components:
1. **Email Processing Service**: Connects to Gmail and manages the email processing pipeline
2. **Classification Engine**: Analyzes email content to determine if it's a lead or information request
3. **Information Extraction Service**: Extracts structured data from emails
4. **Data Storage Layer**: Stores all system data securely and efficiently
5. **Web Frontend**: Provides the user interface for human reviewers
6. **Authentication & Authorization Service**: Manages user authentication and access control

## Architecture Diagram (Text Representation)

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

## Component Details

### 1. Email Processing Service

**Purpose**: Connects to Gmail, retrieves emails, and manages the email processing pipeline.

**Key Functions**:
- OAuth 2.0 authentication with Gmail
- Scheduled email retrieval
- Email parsing and normalization
- Email metadata extraction
- Triggering the classification process
- Handling Gmail API rate limits and quotas

**Technologies**:
- Python FastAPI
- Gmail API client
- Background task processing (Celery)

**Implementation Status**: 
- ✅ OAuth 2.0 authentication flow
- ✅ Email fetching mechanism
- ⏳ Background task processing (planned)

### 2. Classification Engine

**Purpose**: Analyzes email content to determine if it's a lead or information request.

**Key Functions**:
- Email content analysis
- Classification into predefined categories
- Confidence score calculation
- Flagging emails that need human review
- Learning from human feedback (future enhancement)

**Technologies**:
- Rule-based classification system (initial MVP)
- Natural Language Processing libraries
- Hugging Face classification models (future enhancement)

**Implementation Status**: 
- ⏳ Not yet implemented

### 3. Information Extraction Service

**Purpose**: Extracts structured data from emails to facilitate response generation.

**Key Functions**:
- Contact information extraction
- Product interest identification
- Question/request extraction
- Entity recognition (companies, products, etc.)
- Urgency detection

**Technologies**:
- Named Entity Recognition (NER)
- Regular expressions for pattern matching
- Structured data extraction libraries

**Implementation Status**: 
- ⏳ Not yet implemented

### 4. Data Storage Layer

**Purpose**: Stores all system data securely and efficiently.

**Components**:
- **PostgreSQL Database**:
  - Email metadata and content
  - Classification results
  - Extracted information
  - User accounts and permissions
  - Audit logs

- **Redis Cache**:
  - Frequently accessed information
  - Session data
  - Processing queue

**Key Considerations**:
- Data encryption at rest
- Backup and recovery procedures
- Data retention policies
- Performance optimization

**Database Schema (Core Tables)**:

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

**Implementation Status**: 
- ✅ Database models defined
- ✅ SQLAlchemy ORM setup
- ✅ Alembic migrations configured
- ⏳ Redis caching (planned)

### 5. Web Frontend

**Purpose**: Provides the user interface for human reviewers.

**Key Functions**:
- Email review dashboard
- Classification result visualization
- Response editing interface
- User management
- System configuration
- Analytics and reporting

**Technologies**:
- React.js
- Material UI components
- Responsive design for mobile access
- Real-time updates (WebSockets)

**Key Screens**:
1. Login/Authentication
2. Email Dashboard
3. Email Detail View
4. Classification Review
5. Account Management
6. System Configuration

**Implementation Status**: 
- ⏳ Not yet implemented

### 6. Authentication & Authorization Service

**Purpose**: Manages user authentication and access control.

**Key Functions**:
- User authentication
- Role-based access control
- Session management
- Security policy enforcement
- OAuth integration for Gmail access

**Technologies**:
- JWT (JSON Web Tokens)
- OAuth 2.0
- Role-based permission system

**Implementation Status**: 
- ✅ JWT authentication
- ✅ Password hashing
- ✅ User model and API
- ⏳ Role-based permissions (basic implementation)

## Data Flow

1. **Email Ingestion Flow**:
   ```
   Gmail → Email Processing Service → Classification Engine → 
   Information Extraction → Data Storage
   ```

2. **Review Flow**:
   ```
   Data Storage → API Layer → Web Frontend → Human Reviewer → 
   API Layer → Data Storage
   ```

3. **Authentication Flow**:
   ```
   User → Web Frontend → Authentication Service → 
   Data Storage → Web Frontend
   ```

## Deployment Architecture

The system will be deployed using Docker containers orchestrated with Docker Compose (development) and potentially Kubernetes (production):

```
┌─────────────────────────────────────────────────┐
│                Docker Environment                │
│                                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────────────┐  │
│  │ FastAPI │  │ React   │  │ PostgreSQL      │  │
│  │ Backend │  │ Frontend│  │ Database        │  │
│  └─────────┘  └─────────┘  └─────────────────┘  │
│                                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────────────┐  │
│  │ Celery  │  │ Redis   │  │ Nginx           │  │
│  │ Worker  │  │ Cache   │  │ Web Server      │  │
│  └─────────┘  └─────────┘  └─────────────────┘  │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Scalability Considerations

- Horizontal scaling of the Email Processing Service to handle increased email volume
- Read replicas for the database to handle increased query load
- Caching frequently accessed data in Redis
- Stateless design of API services to allow for load balancing
- Containerization to facilitate easy scaling and deployment

## Security Considerations

- All API endpoints secured with authentication
- HTTPS for all communications
- Encrypted storage of sensitive data
- Regular security audits and updates
- Rate limiting to prevent abuse
- Input validation to prevent injection attacks
- Principle of least privilege for all components

## Future Expansion

The modular architecture allows for future enhancements:

1. **Machine Learning Pipeline**: Add a feedback loop to improve classification accuracy
2. **Multi-channel Support**: Expand beyond Gmail to other communication channels
3. **Advanced Analytics**: Add business intelligence features
4. **Integration Layer**: Connect with additional external systems
5. **Automated Response Generation**: Implement AI-powered response drafting 