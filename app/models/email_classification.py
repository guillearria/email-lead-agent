from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship

from app.db.base import Base


class EmailClassification(Base):
    """Model for storing email classification results."""
    
    __tablename__ = "email_classifications"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)  # lead, information_request, etc.
    subcategory = Column(String, nullable=True)  # new_customer, existing_customer, etc.
    confidence = Column(Float, nullable=False)
    features = Column(JSON, nullable=True)  # Store features used for classification
    classified_at = Column(DateTime, default=datetime.utcnow)
    classified_by = Column(String, default="algorithm")  # algorithm or user ID
    
    # Foreign key to email
    email_id = Column(Integer, ForeignKey("emails.id"), unique=True)
    
    # Relationships
    email = relationship("Email", back_populates="classification")
    
    def __repr__(self):
        return f"<EmailClassification {self.category} ({self.confidence})>" 