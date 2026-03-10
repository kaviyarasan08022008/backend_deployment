from pydantic import BaseModel
from typing import Optional

class ActionBase(BaseModel):
    status: str          # pending / in_progress / resolved
    remarks: str

class ActionCreate(ActionBase):
    complaint_id: int
    collector_id: Optional[int] = None

class ActionResponse(ActionBase):
    id: int
    complaint_id: int
    collector_id: Optional[int] = None

    class Config:
        from_attributes = True