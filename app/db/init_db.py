import logging
from sqlalchemy.orm import Session

# Import base to ensure all models are loaded
from app.db.base_class import Base as BaseClass
from app.db.base import Base, engine, SessionLocal
from app.models.user import User
from app.services.auth import get_password_hash

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    """
    Initialize database with default data.
    
    Args:
        db: Database session
    """
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create default admin user if it doesn't exist
    user = db.query(User).filter(User.email == "admin@example.com").first()
    if not user:
        user = User(
            email="admin@example.com",
            name="Admin User",
            password_hash=get_password_hash("admin123"),  # Change this in production!
            role="admin",
            is_active=True,
        )
        db.add(user)
        db.commit()
        logger.info("Created default admin user")
    else:
        logger.info("Default admin user already exists")


def main() -> None:
    """
    Run database initialization.
    """
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
    logger.info("Database initialized") 