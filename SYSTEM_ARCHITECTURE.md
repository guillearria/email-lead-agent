# Winncom Lead Agent - System Architecture

## Overview

The Winncom Lead Agent is designed as a modular, scalable system that processes emails from Gmail, classifies them, extracts relevant information, and facilitates human review. This document outlines the system architecture, including components, interactions, and data flow.

## System Components

The system consists of the following major components:

1. **Email Processing Service**
2. **Classification Engine**
3. **Information Extraction Service**
4. **Data Storage Layer**
5. **Web Frontend**
6. **Authentication & Authorization Service**

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

### 2. Classification Engine

**Purpose**: Analyzes email content to determine if it's a lead or information request.

**Key Functions**:
- Email content analysis
- Classification into predefined categories
- Confidence score calculation
- Flagging emails that need human review
- Learning from human feedback (future enhancement)

**Technologies**:
- Hugging Face classification models
- Rule-based classification system (initial MVP)
- Natural Language Processing libraries

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

## API Interfaces

### Email Processing API

- `POST /api/emails/fetch`: Trigger email fetching process
- `GET /api/emails`: Retrieve processed emails with pagination
- `GET /api/emails/{id}`: Get specific email details
- `PUT /api/emails/{id}/status`: Update email processing status

### Classification API

- `POST /api/classify`: Submit email for classification
- `GET /api/classification/{id}`: Get classification results
- `POST /api/classification/{id}/feedback`: Submit feedback on classification

### User Management API

- `POST /api/auth/login`: User login
- `POST /api/auth/logout`: User logout
- `GET /api/users`: Get user list (admin only)
- `POST /api/users`: Create new user (admin only)
- `PUT /api/users/{id}`: Update user details

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

## Monitoring and Logging

- Centralized logging system
- Performance metrics collection
- Alerting for system issues
- Audit trail for all actions
- Error tracking and reporting

## Disaster Recovery

- Regular database backups
- Automated recovery procedures
- Redundancy for critical components
- Documented recovery process

## Future Expansion

The modular architecture allows for future enhancements:

1. **Machine Learning Pipeline**: Add a feedback loop to improve classification accuracy
2. **Multi-channel Support**: Expand beyond Gmail to other communication channels
3. **Advanced Analytics**: Add business intelligence features
4. **Integration Layer**: Connect with additional external systems
5. **Automated Response Generation**: Implement AI-powered response drafting 