import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.base_class import Base as BaseClass  # Import all models
from app.core.config import settings
from app.services.auth import get_password_hash
from app.models.user import User

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///./test_temp.db"

@pytest.fixture(scope="session")
def db_engine():
    """
    Create an engine for the test database.
    Returns the engine and handles cleanup of the test database.
    """
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    """
    Creates a new database session for each test function.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    
    DBSession = sessionmaker(bind=connection)
    session = DBSession()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def test_user(db_session):
    """
    Create a test user for testing.
    """
    user = User(
        email="test@example.com",
        name="Test User",
        password_hash=get_password_hash("password123"),
        role="reviewer",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_admin(db_session):
    """
    Create a test admin for testing.
    """
    admin = User(
        email="admin@example.com",
        name="Admin User",
        password_hash=get_password_hash("admin123"),
        role="admin",
        is_active=True
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin 