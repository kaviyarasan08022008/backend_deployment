from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Date
from db.database import Base
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class Complaints(Base):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # people_id refers to the user who made the complaint
    people_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"),nullable=True)
    
    # collector_id is already pointing to users.id
    collector_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    category = Column(String)
    officer_name = Column(String)
    designation = Column(String)

    village = Column(String)
    district = Column(String)

    incident_date = Column(Date)

    description = Column(String)
    image_url = Column(String, nullable=True)
    status = Column(String, default="Not approved")

    is_anonymous = Column(Boolean, default=False)

    contact_name = Column(String, nullable=True)
    contact_phone = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)