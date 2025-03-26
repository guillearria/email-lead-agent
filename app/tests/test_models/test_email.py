"""
Tests for the Email model.
"""
import pytest
from datetime import datetime

from app.models.email import Email
from app.models.gmail_account import GmailAccount


@pytest.fixture
def test_gmail_account(db_session, test_user):
    """Fixture to create a test Gmail account."""
    gmail_account = GmailAccount(
        email="test_gmail_for_email@example.com",
        access_token="access_token_123",
        refresh_token="refresh_token_456",
        user_id=test_user.id
    )
    db_session.add(gmail_account)
    db_session.commit()
    db_session.refresh(gmail_account)
    return gmail_account


def test_email_creation(db_session, test_gmail_account):
    """Test that an email can be created with the required fields."""
    # Arrange & Act
    email = Email(
        gmail_id="msg123",
        thread_id="thread123",
        subject="Test Subject",
        sender_name="Sender Name",
        sender_email="sender@example.com",
        received_at=datetime.utcnow(),
        body_text="This is a test email body.",
        body_html="<p>This is a test email body.</p>",
        account_id=test_gmail_account.id
    )
    db_session.add(email)
    db_session.commit()
    db_session.refresh(email)
    
    # Assert
    assert email.id is not None
    assert email.gmail_id == "msg123"
    assert email.thread_id == "thread123"
    assert email.subject == "Test Subject"
    assert email.sender_name == "Sender Name"
    assert email.sender_email == "sender@example.com"
    assert isinstance(email.received_at, datetime)
    assert email.body_text == "This is a test email body."
    assert email.body_html == "<p>This is a test email body.</p>"
    assert email.status == "unprocessed"  # Default value
    assert isinstance(email.created_at, datetime)
    assert isinstance(email.updated_at, datetime)
    assert email.has_attachments == False  # Default value
    assert email.account_id == test_gmail_account.id


def test_email_representation(db_session, test_gmail_account):
    """Test the string representation of an email."""
    # Arrange
    email = Email(
        gmail_id="msg123",
        thread_id="thread123",
        subject="Representation Test",
        sender_email="sender@example.com",
        received_at=datetime.utcnow(),
        account_id=test_gmail_account.id
    )
    
    # Act & Assert
    assert str(email) == "<Email msg123: Representation Test>"


def test_email_gmail_account_relationship(db_session, test_gmail_account):
    """Test the relationship between Email and GmailAccount."""
    # Arrange & Act
    email = Email(
        gmail_id="relationship_msg",
        thread_id="relationship_thread",
        subject="Relationship Test",
        sender_email="sender@example.com",
        received_at=datetime.utcnow(),
        account_id=test_gmail_account.id
    )
    db_session.add(email)
    db_session.commit()
    db_session.refresh(email)
    db_session.refresh(test_gmail_account)
    
    # Assert
    assert email.account.id == test_gmail_account.id
    assert email.account.email == test_gmail_account.email
    assert len(test_gmail_account.emails) >= 1
    assert any(e.gmail_id == "relationship_msg" for e in test_gmail_account.emails)


def test_email_default_values(db_session, test_gmail_account):
    """Test default values for Email model fields."""
    # Arrange & Act
    email = Email(
        gmail_id="defaults_msg",
        thread_id="defaults_thread",
        sender_email="sender@example.com",
        received_at=datetime.utcnow(),
        account_id=test_gmail_account.id
    )
    db_session.add(email)
    db_session.commit()
    db_session.refresh(email)
    
    # Assert
    assert email.status == "unprocessed"
    assert isinstance(email.created_at, datetime)
    assert isinstance(email.updated_at, datetime)
    assert email.has_attachments == False
    assert email.subject is None  # Optional field
    assert email.sender_name is None  # Optional field
    assert email.body_text is None  # Optional field
    assert email.body_html is None  # Optional field 