# API Documentation

## Executive Summary

The Winncom Lead Agent exposes a RESTful API that enables secure access to email processing, classification, and management features. The API follows modern best practices with JWT authentication, consistent error handling, and clear request/response formats.

## API Overview

The API is organized into the following categories:
1. **Authentication**: User login, logout, and token management
2. **Gmail Integration**: Connect Gmail accounts and fetch emails
3. **Email Processing**: Process and manage emails
4. **Classification**: Classify emails as leads or information requests
5. **Information Extraction**: Extract structured data from emails

## Base URL

- **Development**: `http://localhost:8000/api`
- **Production**: `https://your-domain.com/api`

## Authentication

All API endpoints (except authentication endpoints) require a valid JWT token in the Authorization header:

```
Authorization: Bearer <your_token>
```

### Authentication Endpoints

#### POST /auth/login

Authenticates a user and returns a JWT token.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user123",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "reviewer"
  }
}
```

#### POST /auth/logout

Logs out the current user by invalidating their token.

**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "message": "Successfully logged out"
}
```

#### POST /auth/refresh

Refreshes an expired access token.

**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### GET /auth/me

Returns the current authenticated user's information.

**Response (200 OK):**
```json
{
  "id": "user123",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "reviewer",
  "created_at": "2023-01-01T00:00:00Z",
  "last_login": "2023-01-02T00:00:00Z"
}
```

## Gmail Integration

### Gmail Integration Endpoints

#### POST /gmail/authorize

Initiates the OAuth 2.0 flow for Gmail authorization.

**Response (200 OK):**
```json
{
  "authorization_url": "https://accounts.google.com/o/oauth2/auth?..."
}
```

#### POST /gmail/callback

Handles the OAuth 2.0 callback from Google.

**Request:**
```json
{
  "code": "4/0AY0e-g6..."
}
```

**Response (200 OK):**
```json
{
  "message": "Gmail account successfully connected",
  "account_info": {
    "email": "company@example.com",
    "connected_at": "2023-01-01T00:00:00Z"
  }
}
```

#### GET /gmail/accounts

Lists all connected Gmail accounts.

**Response (200 OK):**
```json
{
  "accounts": [
    {
      "id": "gmail123",
      "email": "company@example.com",
      "connected_at": "2023-01-01T00:00:00Z",
      "last_sync": "2023-01-02T00:00:00Z",
      "status": "active"
    }
  ]
}
```

#### DELETE /gmail/accounts/{account_id}

Disconnects a Gmail account.

**Response (200 OK):**
```json
{
  "message": "Gmail account successfully disconnected"
}
```

#### POST /gmail/emails/fetch

Triggers the email fetching process for connected Gmail accounts.

**Request:**
```json
{
  "account_id": "gmail123",
  "max_emails": 50,
  "since_date": "2023-01-01T00:00:00Z"
}
```

**Response (202 Accepted):**
```json
{
  "message": "Email fetch process started",
  "task_id": "task123",
  "estimated_completion_time": "2023-01-02T00:05:00Z"
}
```

## Email Management

### Email Endpoints

#### GET /emails

Retrieves a paginated list of processed emails.

**Query Parameters:**
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20)
- `status`: Filter by status (e.g., "unprocessed", "classified", "reviewed")
- `classification`: Filter by classification (e.g., "lead", "information_request")
- `from_date`: Filter by date range start
- `to_date`: Filter by date range end
- `search`: Search term for email content or sender

**Response (200 OK):**
```json
{
  "emails": [
    {
      "id": "email123",
      "account_id": "gmail123",
      "gmail_id": "17e9a7d94b3",
      "subject": "Product Inquiry",
      "sender": {
        "name": "Jane Smith",
        "email": "jane@company.com"
      },
      "received_at": "2023-01-01T10:30:00Z",
      "status": "classified",
      "classification": {
        "category": "lead",
        "confidence": 0.92,
        "subcategory": "new_customer"
      },
      "has_attachments": true
    }
  ],
  "pagination": {
    "total": 152,
    "page": 1,
    "per_page": 20,
    "total_pages": 8
  }
}
```

#### GET /emails/{email_id}

Retrieves detailed information about a specific email.

**Response (200 OK):**
```json
{
  "id": "email123",
  "account_id": "gmail123",
  "gmail_id": "17e9a7d94b3",
  "subject": "Product Inquiry",
  "sender": {
    "name": "Jane Smith",
    "email": "jane@company.com"
  },
  "recipients": [
    {
      "name": "Winncom Sales",
      "email": "sales@winncom.com",
      "type": "to"
    }
  ],
  "received_at": "2023-01-01T10:30:00Z",
  "body": {
    "text": "Hello, I'm interested in learning more about your networking products...",
    "html": "<div>Hello, I'm interested in learning more about your networking products...</div>"
  },
  "status": "classified",
  "classification": {
    "category": "lead",
    "confidence": 0.92,
    "subcategory": "new_customer",
    "classified_at": "2023-01-01T10:35:00Z"
  },
  "extracted_information": {
    "contact_info": {
      "name": "Jane Smith",
      "email": "jane@company.com",
      "phone": "+1 555-123-4567",
      "company": "ABC Corp"
    },
    "product_interests": ["networking", "routers"],
    "questions": ["Do you offer enterprise-grade solutions?"],
    "urgency": "medium"
  },
  "attachments": [
    {
      "id": "attach123",
      "filename": "requirements.pdf",
      "mime_type": "application/pdf",
      "size": 256000
    }
  ],
  "thread_id": "thread123",
  "is_reply": false
}
```

#### PUT /emails/{email_id}/status

Updates the status of an email.

**Request:**
```json
{
  "status": "reviewed"
}
```

**Response (200 OK):**
```json
{
  "id": "email123",
  "status": "reviewed",
  "updated_at": "2023-01-02T11:45:00Z"
}
```

## Classification

### Classification Endpoints

#### POST /classification/classify

Submits an email for classification.

**Request:**
```json
{
  "email_id": "email123"
}
```

**Response (202 Accepted):**
```json
{
  "message": "Classification process started",
  "task_id": "task456"
}
```

#### GET /classification/{email_id}

Retrieves classification results for an email.

**Response (200 OK):**
```json
{
  "email_id": "email123",
  "classification": {
    "category": "lead",
    "confidence": 0.92,
    "subcategory": "new_customer",
    "classified_at": "2023-01-01T10:35:00Z"
  },
  "features": {
    "keywords": ["product", "inquiry", "pricing"],
    "intent_signals": ["purchase intent", "information gathering"],
    "email_structure": {
      "has_greeting": true,
      "has_signature": true,
      "question_count": 3
    }
  }
}
```

#### POST /classification/{email_id}/feedback

Submits feedback on a classification result.

**Request:**
```json
{
  "correct": false,
  "correct_category": "information_request",
  "notes": "This is a general inquiry, not a sales lead"
}
```

**Response (200 OK):**
```json
{
  "message": "Feedback recorded successfully",
  "email_id": "email123",
  "feedback_id": "feedback123"
}
```

## Information Extraction

### Information Extraction Endpoints

#### POST /extraction/extract

Submits an email for information extraction.

**Request:**
```json
{
  "email_id": "email123"
}
```

**Response (202 Accepted):**
```json
{
  "message": "Information extraction process started",
  "task_id": "task789"
}
```

#### GET /extraction/{email_id}

Retrieves extracted information for an email.

**Response (200 OK):**
```json
{
  "email_id": "email123",
  "extracted_at": "2023-01-01T10:40:00Z",
  "contact_info": {
    "name": "Jane Smith",
    "email": "jane@company.com",
    "phone": "+1 555-123-4567",
    "company": "ABC Corp"
  },
  "product_interests": [
    {
      "product_type": "networking",
      "confidence": 0.85
    },
    {
      "product_type": "routers",
      "confidence": 0.78
    }
  ],
  "questions": [
    "Do you offer enterprise-grade solutions?",
    "What is your pricing structure?"
  ],
  "urgency": {
    "level": "medium",
    "indicators": ["need information soon", "upcoming project"]
  },
  "preferred_contact_method": "email"
}
```

## Error Handling

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

### Common Error Codes

- `AUTHENTICATION_FAILED`: Authentication credentials are invalid
- `AUTHORIZATION_FAILED`: User does not have permission for the requested operation
- `VALIDATION_ERROR`: Request data failed validation
- `RESOURCE_NOT_FOUND`: Requested resource does not exist
- `RESOURCE_CONFLICT`: Resource state conflicts with the requested operation
- `RATE_LIMIT_EXCEEDED`: API rate limit has been exceeded
- `INTERNAL_SERVER_ERROR`: Unexpected server error

### HTTP Status Codes

- 200 OK: Successful operation
- 201 Created: Resource successfully created
- 202 Accepted: Request accepted for processing
- 400 Bad Request: Invalid request parameters
- 401 Unauthorized: Authentication required or failed
- 403 Forbidden: Authenticated but not authorized
- 404 Not Found: Resource not found
- 409 Conflict: Request conflicts with current state
- 422 Unprocessable Entity: Validation error
- 429 Too Many Requests: Rate limit exceeded
- 500 Internal Server Error: Unexpected server error

## Implementation Status

- ✅ Authentication API
- ✅ Gmail Integration API (basic functionality)
- ⏳ Email Management API (partially implemented)
- ⏳ Classification API (not yet implemented)
- ⏳ Information Extraction API (not yet implemented) 