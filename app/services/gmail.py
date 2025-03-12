import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import google.oauth2.credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.gmail_account import GmailAccount
from app.models.user import User


def create_oauth_flow() -> Flow:
    """
    Create an OAuth 2.0 flow for Gmail API authorization.
    
    Returns:
        Flow: OAuth 2.0 flow
    """
    # Create flow instance
    flow = Flow.from_client_config(
        client_config={
            "web": {
                "client_id": settings.GMAIL_CLIENT_ID,
                "client_secret": settings.GMAIL_CLIENT_SECRET,
                "auth_uri": settings.GMAIL_AUTH_URI,
                "token_uri": settings.GMAIL_TOKEN_URI,
                "redirect_uris": [settings.GMAIL_REDIRECT_URI],
            }
        },
        scopes=[settings.GMAIL_SCOPES],
    )
    flow.redirect_uri = settings.GMAIL_REDIRECT_URI
    return flow


def get_authorization_url() -> str:
    """
    Get the authorization URL for Gmail API.
    
    Returns:
        str: Authorization URL
    """
    flow = create_oauth_flow()
    authorization_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    return authorization_url


def exchange_code_for_token(code: str) -> Dict[str, str]:
    """
    Exchange authorization code for access and refresh tokens.
    
    Args:
        code: Authorization code from OAuth callback
        
    Returns:
        Dict[str, str]: Token information
    """
    flow = create_oauth_flow()
    flow.fetch_token(code=code)
    
    credentials = flow.credentials
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "expiry": credentials.expiry.isoformat() if credentials.expiry else None,
    }


def get_gmail_service(gmail_account: GmailAccount) -> Optional[object]:
    """
    Get Gmail API service for a Gmail account.
    
    Args:
        gmail_account: Gmail account model
        
    Returns:
        object: Gmail API service
    """
    # Check if token is expired and refresh if needed
    token_expiry = gmail_account.token_expiry
    if token_expiry and token_expiry < datetime.utcnow():
        # Token is expired, refresh it
        credentials = google.oauth2.credentials.Credentials(
            token=None,
            refresh_token=gmail_account.refresh_token,
            token_uri=settings.GMAIL_TOKEN_URI,
            client_id=settings.GMAIL_CLIENT_ID,
            client_secret=settings.GMAIL_CLIENT_SECRET,
        )
        
        # Refresh the token
        credentials.refresh(Request())
        
        # Update the account with new token
        gmail_account.access_token = credentials.token
        gmail_account.token_expiry = credentials.expiry
    else:
        # Create credentials from stored token
        credentials = google.oauth2.credentials.Credentials(
            token=gmail_account.access_token,
            refresh_token=gmail_account.refresh_token,
            token_uri=settings.GMAIL_TOKEN_URI,
            client_id=settings.GMAIL_CLIENT_ID,
            client_secret=settings.GMAIL_CLIENT_SECRET,
        )
    
    # Build Gmail API service
    try:
        service = build("gmail", "v1", credentials=credentials)
        return service
    except Exception as e:
        print(f"Error building Gmail service: {e}")
        return None


def connect_gmail_account(db: Session, user: User, code: str) -> GmailAccount:
    """
    Connect a Gmail account for a user.
    
    Args:
        db: Database session
        user: User model
        code: Authorization code from OAuth callback
        
    Returns:
        GmailAccount: Connected Gmail account
    """
    # Exchange code for token
    token_info = exchange_code_for_token(code)
    
    # Get user email from Gmail API
    credentials = google.oauth2.credentials.Credentials(
        token=token_info["token"],
        refresh_token=token_info["refresh_token"],
        token_uri=token_info["token_uri"],
        client_id=token_info["client_id"],
        client_secret=token_info["client_secret"],
    )
    
    service = build("gmail", "v1", credentials=credentials)
    profile = service.users().getProfile(userId="me").execute()
    email = profile["emailAddress"]
    
    # Check if account already exists
    gmail_account = db.query(GmailAccount).filter(GmailAccount.email == email).first()
    if gmail_account:
        # Update existing account
        gmail_account.access_token = token_info["token"]
        gmail_account.refresh_token = token_info["refresh_token"]
        gmail_account.token_expiry = datetime.fromisoformat(token_info["expiry"]) if token_info["expiry"] else None
        gmail_account.status = "active"
        gmail_account.user_id = user.id
    else:
        # Create new account
        gmail_account = GmailAccount(
            email=email,
            access_token=token_info["token"],
            refresh_token=token_info["refresh_token"],
            token_expiry=datetime.fromisoformat(token_info["expiry"]) if token_info["expiry"] else None,
            status="active",
            user_id=user.id,
        )
        db.add(gmail_account)
    
    db.commit()
    db.refresh(gmail_account)
    
    return gmail_account


def fetch_emails(
    db: Session,
    gmail_account: GmailAccount,
    max_results: int = 10,
    query: str = "is:unread",
    since_date: Optional[datetime] = None,
) -> List[Dict]:
    """
    Fetch emails from a Gmail account.
    
    Args:
        db: Database session
        gmail_account: Gmail account model
        max_results: Maximum number of emails to fetch
        query: Gmail search query
        since_date: Only fetch emails after this date
        
    Returns:
        List[Dict]: List of email data
    """
    # Get Gmail API service
    service = get_gmail_service(gmail_account)
    if not service:
        return []
    
    # Build query
    if since_date:
        date_str = since_date.strftime("%Y/%m/%d")
        query = f"{query} after:{date_str}"
    
    # Fetch email list
    try:
        results = service.users().messages().list(
            userId="me", q=query, maxResults=max_results
        ).execute()
        
        messages = results.get("messages", [])
        emails = []
        
        for message in messages:
            # Fetch full message
            msg = service.users().messages().get(
                userId="me", id=message["id"], format="full"
            ).execute()
            
            # Extract headers
            headers = msg["payload"]["headers"]
            subject = next((h["value"] for h in headers if h["name"].lower() == "subject"), "")
            from_header = next((h["value"] for h in headers if h["name"].lower() == "from"), "")
            
            # Parse sender
            sender_name = ""
            sender_email = from_header
            if "<" in from_header and ">" in from_header:
                parts = from_header.split("<")
                sender_name = parts[0].strip()
                sender_email = parts[1].strip(">")
            
            # Extract body
            body_text = ""
            body_html = ""
            
            if "parts" in msg["payload"]:
                for part in msg["payload"]["parts"]:
                    if part["mimeType"] == "text/plain":
                        body_text = part["body"]["data"]
                    elif part["mimeType"] == "text/html":
                        body_html = part["body"]["data"]
            elif "body" in msg["payload"]:
                if msg["payload"]["mimeType"] == "text/plain":
                    body_text = msg["payload"]["body"]["data"]
                elif msg["payload"]["mimeType"] == "text/html":
                    body_html = msg["payload"]["body"]["data"]
            
            # Check for attachments
            has_attachments = False
            if "parts" in msg["payload"]:
                for part in msg["payload"]["parts"]:
                    if "filename" in part and part["filename"]:
                        has_attachments = True
                        break
            
            # Create email data
            email_data = {
                "gmail_id": msg["id"],
                "thread_id": msg["threadId"],
                "subject": subject,
                "sender_name": sender_name,
                "sender_email": sender_email,
                "received_at": datetime.fromtimestamp(int(msg["internalDate"]) / 1000),
                "body_text": body_text,
                "body_html": body_html,
                "has_attachments": has_attachments,
            }
            
            emails.append(email_data)
        
        # Update last sync time
        gmail_account.last_sync = datetime.utcnow()
        db.commit()
        
        return emails
    
    except Exception as e:
        print(f"Error fetching emails: {e}")
        return [] 