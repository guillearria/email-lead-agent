from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship

from app.db.base import Base


class ExtractedInformation(Base):
    """Model for storing extracted information from emails."""
    
    __tablename__ = "extracted_information"
    
    id = Column(Integer, primary_key=True, index=True)
    contact_info = Column(JSON, nullable=True)  # name, email, phone, company
    product_interests = Column(JSON, nullable=True)  # list of products with confidence
    questions = Column(JSON, nullable=True)  # list of questions extracted
    urgency = Column(String, nullable=True)  # low, medium, high
    preferred_contact_method = Column(String, nullable=True)  # email, phone, etc.
    extracted_at = Column(DateTime, default=datetime.utcnow)
    
    # Foreign key to email
    email_id = Column(Integer, ForeignKey("emails.id"), unique=True)
    
    # Relationships
    email = relationship("Email", back_populates="extracted_info")
    
    def __repr__(self):
        return f"<ExtractedInformation for email {self.email_id}>" 