from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base


class Email(Base):
    """Model for storing email information."""
    
    __tablename__ = "emails"
    
    id = Column(Integer, primary_key=True, index=True)
    gmail_id = Column(String, index=True, nullable=False)
    thread_id = Column(String, index=True, nullable=False)
    subject = Column(String, nullable=True)
    sender_name = Column(String, nullable=True)
    sender_email = Column(String, nullable=False)
    received_at = Column(DateTime, nullable=False)
    body_text = Column(Text, nullable=True)
    body_html = Column(Text, nullable=True)
    status = Column(String, default="unprocessed")  # unprocessed, classified, reviewed, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    has_attachments = Column(Boolean, default=False)
    
    # Foreign key to gmail account
    account_id = Column(Integer, ForeignKey("gmail_accounts.id"))
    
    # Relationships
    account = relationship("GmailAccount", back_populates="emails")
    classification = relationship("EmailClassification", back_populates="email", uselist=False)
    extracted_info = relationship("ExtractedInformation", back_populates="email", uselist=False)
    # attachments = relationship("Attachment", back_populates="email")
    
    def __repr__(self):
        return f"<Email {self.gmail_id}: {self.subject}>" 