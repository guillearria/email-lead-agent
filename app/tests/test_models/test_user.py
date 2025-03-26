"""
Tests for the User model.
"""
import pytest
from datetime import datetime

from app.models.user import User
from app.services.auth import get_password_hash, verify_password


def test_user_creation(db_session):
    """Test that a user can be created with the required fields."""
    # Arrange & Act
    user = User(
        email="new_user@example.com",
        name="New User",
        password_hash=get_password_hash("password123"),
        role="reviewer"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    # Assert
    assert user.id is not None
    assert user.email == "new_user@example.com"
    assert user.name == "New User"
    assert user.role == "reviewer"
    assert user.is_active == True  # Default value
    assert isinstance(user.created_at, datetime)
    assert user.last_login is None


def test_user_representation(db_session):
    """Test the string representation of a user."""
    # Arrange
    user = User(
        email="repr_test@example.com",
        name="Repr Test",
        password_hash="hash",
        role="reviewer"
    )
    
    # Act & Assert
    assert str(user) == "<User repr_test@example.com>"


def test_user_unique_email_constraint(db_session, test_user):
    """Test that users must have unique email addresses."""
    # Arrange
    duplicate_user = User(
        email=test_user.email,  # Same email as test_user
        name="Duplicate User",
        password_hash="hash",
        role="reviewer"
    )
    
    # Act & Assert
    db_session.add(duplicate_user)
    with pytest.raises(Exception):  # SQLite will raise an IntegrityError
        db_session.commit()
    db_session.rollback()


def test_user_password_hashing():
    """Test that passwords are properly hashed and can be verified."""
    # Arrange
    plain_password = "secure_password123"
    
    # Act
    hashed = get_password_hash(plain_password)
    
    # Assert
    assert hashed != plain_password
    assert verify_password(plain_password, hashed)
    assert not verify_password("wrong_password", hashed)


def test_user_default_values(db_session):
    """Test default values for User model fields."""
    # Arrange & Act
    user = User(
        email="defaults@example.com",
        name="Default User",
        password_hash="hash",
        # role not specified - should default to "reviewer"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    # Assert
    assert user.role == "reviewer"
    assert user.is_active == True
    assert isinstance(user.created_at, datetime)
    assert user.last_login is None 