from sqlalchemy import Column, Integer, String, ForeignKey
from db.database import Base

class Actions(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"))
    collector_id = Column(Integer, ForeignKey("users.id"))

    status = Column(String)   # pending / in_progress / resolved
    remarks = Column(String)
