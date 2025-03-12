from app.db.base import Base
from app.models.user import User
from app.models.gmail_account import GmailAccount
from app.models.email import Email
from app.models.email_classification import EmailClassification
from app.models.extracted_information import ExtractedInformation

# Import all models here for Alembic to detect them
__all__ = [
    "Base",
    "User",
    "GmailAccount",
    "Email",
    "EmailClassification",
    "ExtractedInformation",
] 