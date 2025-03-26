"""
Tests for the ExtractedInformation model.
"""
import pytest
from datetime import datetime

from app.models.email import Email
from app.models.extracted_information import ExtractedInformation
from app.models.gmail_account import GmailAccount


@pytest.fixture
def test_gmail_account(db_session, test_user):
    """Fixture to create a test Gmail account."""
    gmail_account = GmailAccount(
        email="test_gmail_for_extraction@example.com",
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
    """Fixture to create a test email for information extraction."""
    email = Email(
        gmail_id="extraction_msg",
        thread_id="extraction_thread",
        subject="Information Extraction Test",
        sender_email="sender@example.com",
        received_at=datetime.utcnow(),
        account_id=test_gmail_account.id
    )
    db_session.add(email)
    db_session.commit()
    db_session.refresh(email)
    return email


def test_extracted_information_creation(db_session, test_email):
    """Test that extracted information can be created with the required fields."""
    # Arrange & Act
    extracted_info = ExtractedInformation(
        contact_info={
            "name": "John Smith",
            "email": "john@company.com",
            "phone": "555-123-4567",
            "company": "ABC Corp"
        },
        product_interests=[
            {"product": "laptop", "confidence": 0.95},
            {"product": "printer", "confidence": 0.7}
        ],
        questions=["What is the price?", "Do you offer delivery?"],
        urgency="high",
        preferred_contact_method="email",
        email_id=test_email.id
    )
    db_session.add(extracted_info)
    db_session.commit()
    db_session.refresh(extracted_info)
    
    # Assert
    assert extracted_info.id is not None
    assert extracted_info.contact_info == {
        "name": "John Smith",
        "email": "john@company.com",
        "phone": "555-123-4567",
        "company": "ABC Corp"
    }
    assert extracted_info.product_interests == [
        {"product": "laptop", "confidence": 0.95},
        {"product": "printer", "confidence": 0.7}
    ]
    assert extracted_info.questions == ["What is the price?", "Do you offer delivery?"]
    assert extracted_info.urgency == "high"
    assert extracted_info.preferred_contact_method == "email"
    assert isinstance(extracted_info.extracted_at, datetime)
    assert extracted_info.email_id == test_email.id


def test_extracted_information_representation(db_session, test_email):
    """Test the string representation of extracted information."""
    # Arrange
    extracted_info = ExtractedInformation(
        email_id=test_email.id
    )
    
    # Act & Assert
    assert str(extracted_info) == f"<ExtractedInformation for email {test_email.id}>"


def test_extracted_information_email_relationship(db_session, test_email):
    """Test the relationship between ExtractedInformation and Email."""
    # Arrange & Act
    extracted_info = ExtractedInformation(
        contact_info={"name": "Jane Doe", "email": "jane@example.com"},
        email_id=test_email.id
    )
    db_session.add(extracted_info)
    db_session.commit()
    db_session.refresh(extracted_info)
    db_session.refresh(test_email)
    
    # Assert
    assert extracted_info.email.id == test_email.id
    assert test_email.extracted_info.id == extracted_info.id
    assert test_email.extracted_info.contact_info["name"] == "Jane Doe"


def test_extracted_information_unique_constraint(db_session, test_email):
    """Test that an email can only have one set of extracted information."""
    # Arrange
    info1 = ExtractedInformation(
        contact_info={"name": "First Contact"},
        email_id=test_email.id
    )
    db_session.add(info1)
    db_session.commit()
    
    info2 = ExtractedInformation(
        contact_info={"name": "Second Contact"},  # Different data
        email_id=test_email.id  # Same email_id
    )
    
    # Act & Assert
    db_session.add(info2)
    with pytest.raises(Exception):  # SQLite will raise an IntegrityError
        db_session.commit()
    db_session.rollback()


def test_extracted_information_json_support(db_session, test_email):
    """Test that the JSON fields properly store and retrieve complex data."""
    # Arrange
    contact_info = {
        "name": "Complex Test",
        "email": "complex@example.com",
        "phone": "555-987-6543",
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "zip": "12345"
        },
        "social_media": ["LinkedIn", "Twitter"]
    }
    
    product_interests = [
        {"product": "server", "confidence": 0.9, "specifications": ["16GB RAM", "1TB SSD"]},
        {"product": "software", "confidence": 0.8, "licenses": 5},
    ]
    
    # Act
    extracted_info = ExtractedInformation(
        contact_info=contact_info,
        product_interests=product_interests,
        email_id=test_email.id
    )
    db_session.add(extracted_info)
    db_session.commit()
    db_session.refresh(extracted_info)
    
    # Assert
    assert extracted_info.contact_info == contact_info
    assert extracted_info.contact_info["address"]["city"] == "Anytown"
    assert extracted_info.contact_info["social_media"] == ["LinkedIn", "Twitter"]
    
    assert extracted_info.product_interests == product_interests
    assert extracted_info.product_interests[0]["specifications"] == ["16GB RAM", "1TB SSD"]
    assert extracted_info.product_interests[1]["licenses"] == 5


def test_extracted_information_nullable_fields(db_session, test_email):
    """Test that fields in ExtractedInformation can be null."""
    # Arrange & Act
    extracted_info = ExtractedInformation(
        email_id=test_email.id
        # All other fields left as None
    )
    db_session.add(extracted_info)
    db_session.commit()
    db_session.refresh(extracted_info)
    
    # Assert
    assert extracted_info.id is not None
    assert extracted_info.contact_info is None
    assert extracted_info.product_interests is None
    assert extracted_info.questions is None
    assert extracted_info.urgency is None
    assert extracted_info.preferred_contact_method is None
    assert isinstance(extracted_info.extracted_at, datetime)
    assert extracted_info.email_id == test_email.id 