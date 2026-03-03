from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class ComplaintBase(BaseModel):
    category: Optional[str] = None
    officer_name: Optional[str] = None
    village: Optional[str] = None
    district: Optional[str] = None
    incident_date: Optional[date] = None
    description: Optional[str] = None
    is_anonymous: bool = False
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None

class ComplaintCreate(ComplaintBase):
    people_id: int
    collector_id: Optional[int] = None



class ComplaintResponse(BaseModel):
    id: int
    category: Optional[str] = None
    officer_name: Optional[str] = None
    designation: Optional[str] = None
    village: Optional[str] = None
    district: Optional[str] = None
    incident_date: Optional[date] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[str] = "Not approved"
    is_anonymous: bool = False
    people_id: Optional[int] = None
    collector_id: Optional[int] = None

    class Config:
        from_attributes = True  # Pydantic v2 (orm_mode for v1)