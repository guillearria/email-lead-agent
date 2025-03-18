from app.db.base import Base

# Import all models here for Alembic to detect them
# Order matters due to relationships - models with fewer dependencies first

# First, import User since everything depends on it
from app.models.user import User

# Then, import models that directly relate to User
from app.models.gmail_account import GmailAccount

# Finally, import the rest in dependency order
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