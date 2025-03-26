"""
Tests for the EmailClassification model.
"""
import pytest
from datetime import datetime
import json

from app.models.email import Email
from app.models.email_classification import EmailClassification
from app.models.gmail_account import GmailAccount


@pytest.fixture
def test_gmail_account(db_session, test_user):
    """Fixture to create a test Gmail account."""
    gmail_account = GmailAccount(
        email="test_gmail_for_classification@example.com",
        access_token="access_token_123",
        refresh_token="refresh_token_456",
        user_id=test_user.id
    )
    db_session.add(gmail_account)
    db_session.commit()
    db_session.refresh(gmail_account)
    return gmail_account


@pytest.fixture
def test_email(db_session, test_gmail_account):
    """Fixture to create a test email for classification."""
    email = Email(
        gmail_id="classification_msg",
        thread_id="classification_thread",
        subject="Classification Test",
        sender_email="sender@example.com",
        received_at=datetime.utcnow(),
        account_id=test_gmail_account.id
    )
    db_session.add(email)
    db_session.commit()
    db_session.refresh(email)
    return email


def test_email_classification_creation(db_session, test_email):
    """Test that an email classification can be created with the required fields."""
    # Arrange & Act
    classification = EmailClassification(
        category="lead",
        subcategory="new_customer",
        confidence=0.85,
        features={"keywords": ["buy", "product", "interested"]},
        email_id=test_email.id
    )
    db_session.add(classification)
    db_session.commit()
    db_session.refresh(classification)
    
    # Assert
    assert classification.id is not None
    assert classification.category == "lead"
    assert classification.subcategory == "new_customer"
    assert classification.confidence == 0.85
    assert classification.features == {"keywords": ["buy", "product", "interested"]}
    assert isinstance(classification.classified_at, datetime)
    assert classification.classified_by == "algorithm"  # Default value
    assert classification.email_id == test_email.id


def test_email_classification_representation(db_session, test_email):
    """Test the string representation of an email classification."""
    # Arrange
    classification = EmailClassification(
        category="information_request",
        confidence=0.75,
        email_id=test_email.id
    )
    
    # Act & Assert
    assert str(classification) == "<EmailClassification information_request (0.75)>"


def test_email_classification_email_relationship(db_session, test_email):
    """Test the relationship between EmailClassification and Email."""
    # Arrange & Act
    classification = EmailClassification(
        category="lead",
        confidence=0.9,
        email_id=test_email.id
    )
    db_session.add(classification)
    db_session.commit()
    db_session.refresh(classification)
    db_session.refresh(test_email)
    
    # Assert
    assert classification.email.id == test_email.id
    assert test_email.classification.id == classification.id
    assert test_email.classification.category == "lead"


def test_email_classification_unique_constraint(db_session, test_email):
    """Test that an email can only have one classification."""
    # Arrange
    classification1 = EmailClassification(
        category="lead",
        confidence=0.9,
        email_id=test_email.id
    )
    db_session.add(classification1)
    db_session.commit()
    
    classification2 = EmailClassification(
        category="information_request",  # Different category
        confidence=0.8,
        email_id=test_email.id  # Same email_id
    )
    
    # Act & Assert
    db_session.add(classification2)
    with pytest.raises(Exception):  # SQLite will raise an IntegrityError
        db_session.commit()
    db_session.rollback()


def test_email_classification_json_support(db_session, test_email):
    """Test that the features field properly stores and retrieves JSON data."""
    # Arrange
    features_data = {
        "keywords": ["purchase", "quote", "price"],
        "sentiment": "positive",
        "urgency": 0.7,
        "extracted_products": ["laptop", "monitor"]
    }
    
    # Act
    classification = EmailClassification(
        category="lead",
        confidence=0.95,
        features=features_data,
        email_id=test_email.id
    )
    db_session.add(classification)
    db_session.commit()
    db_session.refresh(classification)
    
    # Assert
    assert classification.features == features_data
    assert classification.features["keywords"] == ["purchase", "quote", "price"]
    assert classification.features["sentiment"] == "positive"
    assert classification.features["urgency"] == 0.7
    assert classification.features["extracted_products"] == ["laptop", "monitor"] 