"""
Tests for the GmailAccount model.
"""
import pytest
from datetime import datetime, timedelta

from app.models.gmail_account import GmailAccount


def test_gmail_account_creation(db_session, test_user):
    """Test that a Gmail account can be created with the required fields."""
    # Arrange & Act
    gmail_account = GmailAccount(
        email="test_gmail@example.com",
        access_token="access_token_123",
        refresh_token="refresh_token_456",
        token_expiry=datetime.utcnow() + timedelta(hours=1),
        user_id=test_user.id
    )
    db_session.add(gmail_account)
    db_session.commit()
    db_session.refresh(gmail_account)
    
    # Assert
    assert gmail_account.id is not None
    assert gmail_account.email == "test_gmail@example.com"
    assert gmail_account.access_token == "access_token_123"
    assert gmail_account.refresh_token == "refresh_token_456"
    assert isinstance(gmail_account.token_expiry, datetime)
    assert isinstance(gmail_account.connected_at, datetime)
    assert gmail_account.last_sync is None
    assert gmail_account.status == "active"  # Default value
    assert gmail_account.user_id == test_user.id


def test_gmail_account_representation(db_session):
    """Test the string representation of a Gmail account."""
    # Arrange
    gmail_account = GmailAccount(
        email="repr_gmail@example.com",
        access_token="token",
        refresh_token="refresh",
        user_id=1
    )
    
    # Act & Assert
    assert str(gmail_account) == "<GmailAccount repr_gmail@example.com>"


def test_gmail_account_unique_email_constraint(db_session, test_user):
    """Test that Gmail accounts must have unique email addresses."""
    # Arrange
    gmail1 = GmailAccount(
        email="unique_test@example.com",
        access_token="token1",
        refresh_token="refresh1",
        user_id=test_user.id
    )
    db_session.add(gmail1)
    db_session.commit()
    
    gmail2 = GmailAccount(
        email="unique_test@example.com",  # Same email
        access_token="token2",
        refresh_token="refresh2",
        user_id=test_user.id
    )
    
    # Act & Assert
    db_session.add(gmail2)
    with pytest.raises(Exception):  # SQLite will raise an IntegrityError
        db_session.commit()
    db_session.rollback()


def test_gmail_account_user_relationship(db_session, test_user):
    """Test the relationship between User and GmailAccount."""
    # Arrange & Act
    gmail_account = GmailAccount(
        email="relationship_test@example.com",
        access_token="token",
        refresh_token="refresh",
        user_id=test_user.id
    )
    db_session.add(gmail_account)
    db_session.commit()
    db_session.refresh(gmail_account)
    db_session.refresh(test_user)
    
    # Assert
    assert gmail_account.user.id == test_user.id
    assert gmail_account.user.email == test_user.email
    assert len(test_user.gmail_accounts) >= 1
    assert any(account.email == "relationship_test@example.com" for account in test_user.gmail_accounts)


def test_gmail_account_default_values(db_session, test_user):
    """Test default values for GmailAccount model fields."""
    # Arrange & Act
    gmail_account = GmailAccount(
        email="defaults_gmail@example.com",
        access_token="token",
        refresh_token="refresh",
        user_id=test_user.id
    )
    db_session.add(gmail_account)
    db_session.commit()
    db_session.refresh(gmail_account)
    
    # Assert
    assert gmail_account.status == "active"
    assert isinstance(gmail_account.connected_at, datetime)
    assert gmail_account.last_sync is None 