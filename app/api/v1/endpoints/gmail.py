from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.gmail_account import GmailAccount
from app.models.user import User
from app.services.auth import get_current_active_user
from app.services.gmail import (
    connect_gmail_account,
    fetch_emails,
    get_authorization_url,
)

router = APIRouter()


# Request and response models
class AuthorizationResponse(BaseModel):
    authorization_url: str


class CallbackRequest(BaseModel):
    code: str


class GmailAccountResponse(BaseModel):
    id: int
    email: str
    connected_at: datetime
    last_sync: Optional[datetime] = None
    status: str

    class Config:
        from_attributes = True


class EmailFetchRequest(BaseModel):
    account_id: int
    max_emails: int = 10
    since_date: Optional[datetime] = None


class EmailFetchResponse(BaseModel):
    message: str
    task_id: str
    estimated_completion_time: datetime


@router.post("/authorize", response_model=AuthorizationResponse)
async def authorize_gmail(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get authorization URL for Gmail API.
    """
    authorization_url = get_authorization_url()
    return {"authorization_url": authorization_url}


@router.post("/callback", response_model=GmailAccountResponse)
async def gmail_callback(
    callback_data: CallbackRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Handle OAuth callback from Gmail API.
    """
    try:
        gmail_account = connect_gmail_account(db, current_user, callback_data.code)
        return gmail_account
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to connect Gmail account: {str(e)}",
        )


@router.get("/accounts", response_model=List[GmailAccountResponse])
async def list_gmail_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    List all connected Gmail accounts for the current user.
    """
    accounts = db.query(GmailAccount).filter(GmailAccount.user_id == current_user.id).all()
    return accounts


@router.delete("/accounts/{account_id}", response_model=Dict[str, str])
async def disconnect_gmail_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Disconnect a Gmail account.
    """
    account = db.query(GmailAccount).filter(
        GmailAccount.id == account_id,
        GmailAccount.user_id == current_user.id,
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gmail account not found",
        )
    
    # Mark as inactive instead of deleting
    account.status = "inactive"
    db.commit()
    
    return {"message": "Gmail account successfully disconnected"}


@router.post("/emails/fetch", response_model=EmailFetchResponse)
async def fetch_gmail_emails(
    fetch_data: EmailFetchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Fetch emails from a Gmail account.
    
    Note: In a production environment, this would be a background task.
    For simplicity, we're doing it synchronously here.
    """
    # Get Gmail account
    account = db.query(GmailAccount).filter(
        GmailAccount.id == fetch_data.account_id,
        GmailAccount.user_id == current_user.id,
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gmail account not found",
        )
    
    # In a real implementation, this would be a background task
    # For now, we'll just return a fake task ID
    task_id = f"task_{account.id}_{datetime.utcnow().timestamp()}"
    estimated_completion = datetime.utcnow()
    
    # For demonstration, fetch a few emails synchronously
    # In production, this would be done in a background task
    emails = fetch_emails(
        db=db,
        gmail_account=account,
        max_results=fetch_data.max_emails,
        since_date=fetch_data.since_date,
    )
    
    # Store emails in database (simplified for now)
    # In production, this would be done in the background task
    from app.models.email import Email
    
    for email_data in emails:
        # Check if email already exists
        existing_email = db.query(Email).filter(
            Email.gmail_id == email_data["gmail_id"],
            Email.account_id == account.id,
        ).first()
        
        if not existing_email:
            # Create new email
            email = Email(
                gmail_id=email_data["gmail_id"],
                thread_id=email_data["thread_id"],
                subject=email_data["subject"],
                sender_name=email_data["sender_name"],
                sender_email=email_data["sender_email"],
                received_at=email_data["received_at"],
                body_text=email_data["body_text"],
                body_html=email_data["body_html"],
                has_attachments=email_data["has_attachments"],
                account_id=account.id,
            )
            db.add(email)
    
    db.commit()
    
    return {
        "message": "Email fetch process started",
        "task_id": task_id,
        "estimated_completion_time": estimated_completion,
    } 