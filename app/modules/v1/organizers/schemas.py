from datetime import datetime
from typing import List, Optional

from core.schemas import EmailStr, PhoneStr, UrlStr
from pydantic import BaseModel, Field


class CreateRequest(BaseModel):
    name: str
    email: EmailStr
    logo: Optional[UrlStr] = None
    phone: Optional[PhoneStr] = None
    description: Optional[str] = None
    # Location
    country: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    ward: Optional[str] = None
    # Social
    facebook: Optional[UrlStr] = None
    twitter: Optional[UrlStr] = None
    linkedin: Optional[UrlStr] = None
    instagram: Optional[UrlStr] = None


class Response(BaseModel):
    id: str = Field(alias="_id")
    name: str
    email: str
    logo: Optional[str] = None
    phone: Optional[str] = None
    description: Optional[str] = None
    # Location
    country: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    ward: Optional[str] = None
    # Social
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    linkedin: Optional[str] = None
    instagram: Optional[str] = None

    created_at: datetime
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None


class ListResponse(BaseModel):
    total_items: int
    total_page: int
    records_per_page: int
    results: List[Response]


class EditRequest(BaseModel):
    name: Optional[str] = None
    logo: Optional[UrlStr] = None
    email: Optional[EmailStr] = None
    phone: Optional[PhoneStr] = None
    description: Optional[str] = None
    # location
    country: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    ward: Optional[str] = None
    # social
    facebook: Optional[UrlStr] = None
    twitter: Optional[UrlStr] = None
    linkedin: Optional[UrlStr] = None
    instagram: Optional[UrlStr] = None
