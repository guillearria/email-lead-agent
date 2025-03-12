from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# Token schemas
class Token(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    user: Optional[dict] = None


class TokenPayload(BaseModel):
    """Schema for token payload."""
    sub: Optional[str] = None
    exp: Optional[int] = None


# User schemas
class UserBase(BaseModel):
    """Base schema for user data."""
    email: EmailStr
    name: str
    is_active: bool = True
    role: str = "reviewer"


class UserCreate(UserBase):
    """Schema for user creation."""
    password: str


class UserUpdate(UserBase):
    """Schema for user update."""
    password: Optional[str] = None


class UserInDB(UserBase):
    """Schema for user in database."""
    id: int
    password_hash: str
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        """Pydantic config."""
        from_attributes = True


class User(UserBase):
    """Schema for user response."""
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        """Pydantic config."""
        from_attributes = True 